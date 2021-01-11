from flask import Flask, request, abort, jsonify, g
import uuid
import sqlite3
import librosa
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohxee6va6S'
app.config['MAX_CONTENT_LENGTH'] = 10 * (1000 * 1000) # 10 Mo
socketio = SocketIO(app)

static_folder = 'static/'
database = static_folder + 'database.db'
schema = 'schema.sqlite'
uploads_folder = static_folder + 'uploads/'
processed_folder = static_folder + 'process/'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db
    
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(schema, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

import model_versions
from websocket import SocketNamespace

socket_namespace = SocketNamespace('/api/job')

@app.route('/')
def test_socket(): # TODO : remove !
    return """
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
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
    f = request.files.get('file')
    if version_id and f:
        s_f = str(uuid.uuid4())
        upload = uploads_folder + s_f
        f.save(upload)
        try:
            audio = librosa.load(upload)
            ## TODO : Launch the job
            return jsonify({ 'filename': s_f }) ## TODO: change
        except:
            # The file is not an audio file that can be processed
            abort(415)
    else:
        abort(400)
    
@app.route('/api/job/<int:job_id>/result', methods=['GET'])
def get_tablature(job_id):
    abort(404) # TODO

socketio.on_namespace(socket_namespace)
if __name__ == '__main__':
    socketio.run(app) 
