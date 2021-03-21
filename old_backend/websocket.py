from flask_socketio import Namespace, emit, join_room, leave_room
from main import get_job

class SocketNamespace(Namespace):

    def on_request_progress(self, data):
        job_id = data['job_id']
        job = get_job(job_id)
        if job_id and job is not None:
            step = job.current_step
            max_step = len(job.model.steps())-1
            progress = {
                "step": step
                "max_step": max_step
                "step_progress": 0,
                "total_progress": float(step) / max_step
                "done": job.done
            }
            status = {
                "job_id": job_id,
                "version_id": job.model.id(),
                "steps": job.model.steps(),
                "result_url": None,
                "progress": progress
            }
            if job.done:
                status["result_url"] = "/api/job/" + job_id + "/result"
            emit('current_status', status)
            emit('current_progress', {"job_id": job_id, "progress": progress}, room=job_id)
            join_room(job_id)

