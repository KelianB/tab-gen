from django.db import models
from django.core.validators import FileExtensionValidator

from .tasks import launch_task

"""
Represents a model version, including the name, description and file obtained from training.
"""
class Version(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    model = models.FileField(upload_to='models/')

"""
Represents a job. A Job has a model (version), an input file and, if the job is done, an output file.
"""
class Task(models.Model):
    version = models.ForeignKey('Version', on_delete=models.CASCADE)
    input = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'ogg', 'opus', 'flac'])])
    output = models.FileField(upload_to='results/', blank=True)
    _current = None
    
    @property
    def done(self):
        """
        Returns true if the job has an output (meaning it's done); returns false if the job isn't started or is currently happening.
        """
        return bool(self.output)
        
    def start(self):
        """
        Start the job asynchronously. Progress will be lost if the server is stopped.
        """
        if not self.done and self.input:
            self._current = launch_task.delay(self.pk)
        
    @property
    def status(self):
        """
            Returns the current progress of the job, whether it wasn't started, is currently happening or is done.
            If currently happening, notably returns the current step and progress.
            If done, notably returns the url by which the output can be accessed.
        """
        _id = self.pk
        version_id = self.version.pk
        done = self.done
        steps = ["Parsing", "Preprocessing", "Processing", "Saving"]
        result_url = "/api/job/{}/result".format(_id) if done else None
        progress = {
            'step': len(steps) if done else 0,
            'max_step': len(steps),
            'step_progress': 1,
            'total_progress': 1 if done else 0,
            'done': done
        }
        # If the job is happening, we need to obtain the async task's information
        if self._current and self._current.status == 'PROGRESS':
            step = self._current.info.step
            progress = {
                'step': step,
                'max_step': len(steps),
                'step_progress': 0,
                'total_progress': float(step) / float(len(steps)),
                'done': False
            }
        else:
            return {
                'job_id': _id,
                'version_id': version_id,
                'steps': steps,
                'result_url': result_url,
                'progress': progress
            }
