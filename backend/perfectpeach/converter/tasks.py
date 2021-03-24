from django.core.files.base import ContentFile
from celery import shared_task
import uuid
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .ml.use_model import *
from .atex.generator import generate_atex

@shared_task(bind=True)
def launch_task(self, task_id):
    """
    Processes the input file through multiple steps. The last steps returns an output, which is then saved.
    This function is called asynchronously.
    On each step change, an internal message is sent to send the new status to all subscribed clients.
    """
    from .models import Task
    task = Task.objects.get(pk=task_id)
    _set_step_task(self, task, 1)
    # 1) Prepare audio file
    # This will fail if the file is not a valid audio file, which is intended.
    data, sr = librosa.load(task.input.path, sr=AUDIO_SAMPLE_RATE, mono=True)
    _set_step_task(self, task, 2)
    # 2) Apply model
    print("." + task.version.model.url)
    model = load_model("." + task.version.model.url)
    max_duration = 30 # Arbitrary
    chords = [infer(model, img) for img in cqt_image_generator(data, max_duration)]
    _set_step_task(self, task, 3)
    # 3) Convert to output format
    atex = generate_atex(chords)
    _set_step_task(self, task, 4)
    # 4) Save result
    task.output.save(str(uuid.uuid4()) + ".atex", ContentFile(atex))
    self.update_state(state='SUCCESS')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(str(task.pk), { 'type': 'current_progress', 'message': task.status })
    task._current = None
    task.save()

def _set_step_task(celeri_task, task, step):
    """
    Sends an internal message to send the new status to all subscribed clients.
    """
    celeri_task.update_state(state='PROGRESS', meta={ step: step })
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(str(task.pk), { 'type': 'current_progress', 'message': task.status })
