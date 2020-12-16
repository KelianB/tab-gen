from flask import Flask, request, abort, jsonify
import uuid
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohxee6va6S'
app.config['MAX_CONTENT_LENGTH'] = 10 * (1000 * 1000) # 10 Mo
socketio = SocketIO(app)

import model_versions
from websocket import SocketNamespace

socket_namespace = SocketNamespace('/api/job')

@app.route('/')
def test_socket(): # TODO : remove !
    return """
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
    <script type="text/javascript" charset="utf-8">
        var socket = io("/api/job");
        socket.on('connect', function() {
            socket.emit('request_progress', { "job_id":4 });
        });
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
            "description": model_versions.versions[_id].description()
        }
        result.append(version)
    return jsonify(result)
    
@app.route('/api/job', methods=['POST'])
def post_audio():
    version_id = request.args.get('version_id')
    f = request.files.get('file')
    if version_id and f:
        # TODO: check the file integrity with librosa (for instance)
        s_f = str(uuid.uuid4())
        f.save('static/uploads/' + s_f)
        return jsonify({ 'filename': s_f }) ## TODO: change
    else:
        abort(400)
    
@app.route('/api/job/<int:job_id>/result', methods=['GET'])
def get_tablature(job_id):
    abort(404) # TODO

socketio.on_namespace(socket_namespace)
if __name__ == '__main__':
    socketio.run(app) 
