from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from .models import Version, Task

def get_versions(request):
    """
    Returns the list of all model versions known to the server.
    """
    if request.method != 'GET':
        return HttpResponse(status=405)
    else:
        return JsonResponse(list(Version.objects.all().values("id", "name", "description")), safe=False)
    
# CSRF exemption is needed because this is a POST method.
# An alternative would be to disable the CSRF middleware entirely.
@csrf_exempt
def upload_task(request):
    """
    Sends a new job on the uploaded file based on the specified version.
    Uploaded file integrity (as an audio file) is not checked, as the job will do so at the start because it has to extract the audio information, and checking twice audio integrity slows down significantly the whole process.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)
    else:
        version_id = request.GET.get("version_id", None)
        input = request.FILES.get("file", None)
        if not version_id or not input:
            return HttpResponse(status=400)
        version = get_object_or_404(Version, pk=version_id)
        task = Task(version=version, input=input)
        task.save() # We have to save before we start, since the job relies on the job object existing in the database, as it cannot be serialized by pickle
        task.start()
        return JsonResponse({ 'job_id': task.pk })

def get_task_output(request, task_id):
    """
    Returns the task output file if done; returns an error otherwise.
    """
    if request.method != 'GET':
        return HttpResponse(status=405)
    else:
        task = get_object_or_404(Task, pk=task_id)
        if not task.done:
            return HttpResponse(status=102)
        else:
            return FileResponse(task.output)

