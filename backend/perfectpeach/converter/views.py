from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from .models import Version, Task

def get_versions(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    else:
        return JsonResponse(list(Version.objects.all().values("id", "name", "description")), safe=False)
    
@csrf_exempt
def upload_task(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    else:
        version_id = request.GET.get("version_id", None)
        input = request.FILES.get("file", None)
        if not version_id or not input:
            return HttpResponse(status=400)
        version = get_object_or_404(Version, pk=version_id)
        task = Task(version=version, input=input)
        task.save()
        task.start()
        return JsonResponse({ 'job_id': task.pk })

def get_task_output(request, task_id):
    if request.method != 'GET':
        return HttpResponse(status=405)
    else:
        task = get_object_or_404(Task, pk=task_id)
        if not task.done:
            return HttpResponse(status=102)
        else:
            return FileResponse(task.output)

