from flask import Flask, request, abort, jsonify, g
import uuid
import random
import librosa
from flask_socketio import SocketIO
import threading

from job import Job, load_job_from_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohxee6va6S'
app.config['MAX_CONTENT_LENGTH'] = 10 * (1000 * 1000) # 10 Mo
socketio = SocketIO(app)

static_folder = 'static/'
database = static_folder + 'database.db'
schema = 'schema.sqlite'
uploads_folder = static_folder + 'uploads/'
processed_folder = static_folder + 'process/'

from database import query_db, execute_db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

import model_versions
from websocket import SocketNamespace

socket_namespace = SocketNamespace('/api/job')
socketio.on_namespace(socket_namespace)

jobs = dict()

def get_job(job_id):
    job = jobs.get(job_id)
    if job is None:
        job = load_job_from_db(job_id, database, app)
    return job

@app.route('/')
def test_socket(): # TODO : remove !
    return """
    <script src="https://cdn.socket.io/socket.io-3.0.1.min.js"></script>
    <script type="text/javascript" charset="utf-8">
        var socket = io("/api/job");
        socket.on('connect', () => socket.emit('request_progress', { "job_id":4 }));
        socket.on("current_status", (data) => console.log(data));
        socket.on("current_progress", (data) => console.log(data));
    </script>
    Does it work ?
"""

"""
    Returns the list of available model versions. This may change between server restarts - the client should not cache this.
"""
@app.route('/api/versions', methods=['GET'])
def get_model_versions():
    result = []
    for _id in model_versions.versions:
        version = {
            "id": _id,
            "name": model_versions.versions[_id].name(),
            "description": model_versions.versions[_id].description(),
            "steps": model_versions.versions[_id].steps()
        }
        result.append(version)
    return jsonify(result)
    
@app.route('/api/job', methods=['POST'])
def post_audio():
    version_id = request.args.get('version_id')
    version = model_versions.versions.get(version_id)
    f = request.files.get('file')
    if version is not None and f:
        s_f = str(uuid.uuid4())
        upload = uploads_folder + s_f
        f.save(upload)
        try:
            audio = librosa.load(upload)
        except:
            # The file is not an audio file that can be processed
            abort(415)
            return
        job_id = random.randint(1, 1000000) # TODO: Don't use random numbers (means random failures)
        job = Job(job_id, version, audio)
        jobs[job_id] = job
        execute_db('INSERT INTO "jobs" ("job_id", "version_id", "input") VALUES (?, ?, ?)', database, args=(job_id, version_id, upload))
        thread = threading.Thread(target=job.launch_and_save, args=(processed_folder, database, app))
        thread.start()
        return jsonify({ 'job_id': job_id })
    else:
        abort(400)
    
@app.route('/api/job/<int:job_id>/result', methods=['GET'])
def get_tablature(job_id):
    job = load_job_from_db(job_id, database, app) # We don't care about the current progress
    if job is not None and job.done:
        return job.current_data
    else:
        abort(404)

if __name__ == '__main__':
    socketio.run(app)

