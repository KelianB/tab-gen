from flask_socketio import Namespace, emit

class SocketNamespace(Namespace):

    def on_connect(self):
        print('miam')

    def on_request_progress(self, data):
        job_id = data['job_id']
        if job_id:
            print(job_id)
            print(request.sid)
            progress = {
                done: False
            }
            status = {
                "job_id": job_id,
                "version_id": 0,
                "steps": [],
                "result_url": None,
                "progress": progress
            }
            emit('current_status', status)
            emit('current_progress', {"job_id": job_id, "progress": progress}, room=job_id)
            join_room(job_id)
