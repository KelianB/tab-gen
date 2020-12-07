from flask import Flask, request, jsonify
import uuid
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohxee6va6S'
app.config['MAX_CONTENT_LENGTH'] = 10 * (1000 * 1000) # 10 Mo
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/api/versions', methods=['GET'])
def get_api_versions():
    return jsonify({"key":"value"}) ## TODO
    
@app.route('/api/version/<int:version_id>', methods=['POST'])
def post_audio(version_id):
    f = request.files.get('file')
    if f:
        # TODO: check the file integrity with librosa (for instance)
        s_f = str(uuid.uuid4())
        f.save('static/uploads/' + s_f)
        return jsonify({ 'filename': s_f }) ## TODO: change
    return jsonify({}) ## TODO: Websocket ?

@app.route('/api/version/<int:version_id>/<int:job_id>/state', methods=['GET'])
def we_wont_implement_this_route(version_id, job_id):
    return jsonify({"TODO":"websocket", "etat": True}) ## TODO: deleting this route as it is
    
@app.route('/api/version/<int:version_id>/<int:job_id>', methods=['GET'])
@app.route('/api/version/<int:version_id>/<int:job_id>/result', methods=['GET'])
def get_tablature(version_id, job_id):
    return jsonify({}) ## TODO: We won't send a JSON, but a guitar tablature
    

if __name__ == '__main__':
    socketio.run(app)
