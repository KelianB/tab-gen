import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Task

known_channels = {}

class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        """
        Called when a client disconnects from the websocket.
        When that happens, we need to remove all the channels to which the client subscribed to avoid sending information to a closed connection (this uses unnecessary resources).
        """
        global known_channels
        rooms = known_channels.get(self.channel_name, None)
        if rooms:
            for room in rooms:
                async_to_sync(self.channel_layer.group_discard)(room, self.channel_name)
        del known_channels[self.channel_name]

    def receive(self, text_data):
        """
        Called when a client sends a message to the server.
        The only message in the specification that the client can send is "request_progress" : this subscribes the client to a channel specific to the requested job, which allows it to receive any future updates regarding this job.
        """
        global known_channels
        text_data_json = json.loads(text_data)
        _type = text_data_json.get('type', None)
        job_id = text_data_json.get('job_id', None)
        if _type == 'request_progress' and job_id:
            task = Task.objects.get(pk=job_id)
            if task:
                async_to_sync(self.channel_layer.group_add)(str(job_id), self.channel_name)
                # We need to remember the client subscribed to this channel for closure on disconnect
                if known_channels.get(self.channel_name):
                    known_channels[self.channel_name].append(job_id)
                else:
                    known_channels[self.channel_name] = [job_id]
                self.send(text_data=json.dumps({
                    'type': 'current_progress',
                    'data': task.status
                }))
                
    def current_progress(self, event):
        """
        Called when the server wishes to send a message to all clients subscribed to a job regarding this job's status.
        """
        data = event['message']
        self.send(text_data=json.dumps({
            'type': 'current_progress',
            'data': data
        }))
                
