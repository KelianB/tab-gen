from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
    
@app.route('/api/versions', methods=['GET'])
def get_api_versions():
    return jsonify({"key":"value"}) ## TODO
    
@app.route('/api/version/<int:version_id>', methods=['POST'])
def post_audio(version_id):
    return jsonify({}) ## TODO: Websocket ?

@app.route('/api/version/<int:version_id>/<int:job_id>/state', methods=['GET'])
def we_wont_implement_this_route(version_id, job_id):
    return jsonify({"TODO":"websocket", "etat": True}) ## TODO: deleting this route as it is
    
@app.route('/api/version/<int:version_id>/<int:job_id>', methods=['GET'])
@app.route('/api/version/<int:version_id>/<int:job_id>/result', methods=['GET'])
def get_tablature(version_id, job_id):
    return jsonify({}) ## TODO: We won't send a JSON, but a guitar tablature
    

if __name__ == '__main__':
    app.run()
