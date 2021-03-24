from django.urls import path, re_path

from . import consumers
from . import views

urlpatterns = [
    path('versions', views.get_versions, name='get_versions'),
    path('job', views.upload_task, name='upload_task'),
    path('job/<int:task_id>/result', views.get_task_output, name='get_task_output'),
]

websocket_urlpatterns = [
    re_path(r'api/job$', consumers.TaskConsumer.as_asgi()),
    re_path(r'api/job/$', consumers.TaskConsumer.as_asgi()),
]
