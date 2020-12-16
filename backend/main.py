from flask import Flask, request, jsonify
import uuid
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohxee6va6S'
app.config['MAX_CONTENT_LENGTH'] = 10 * (1000 * 1000) # 10 Mo
socketio = SocketIO(app)

import model_versions
from websocket import SocketNamespace

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
    
@app.route('/api/version/<int:version_id>', methods=['POST'])
def post_audio(version_id):
    f = request.files.get('file')
    if f:
        # TODO: check the file integrity with librosa (for instance)
        s_f = str(uuid.uuid4())
        f.save('static/uploads/' + s_f)
        return jsonify({ 'filename': s_f }) ## TODO: change
    return jsonify({}) ## TODO: Websocket ?
    
@app.route('/api/version/<int:version_id>/<int:job_id>', methods=['GET'])
@app.route('/api/version/<int:version_id>/<int:job_id>/result', methods=['GET'])
def get_tablature(version_id, job_id):
    return jsonify({}) ## TODO: We won't send a JSON, but a guitar tablature
    

socketio.on_namespace(SocketNamespace('/api/job'))
if __name__ == '__main__':
    socketio.run(app) 
