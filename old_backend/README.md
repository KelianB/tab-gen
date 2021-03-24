**Back-end (Flask)**

Pour l'utiliser, il faut d'abord créer un environnement virtuel (voir instruction sur le site de Python). A titre indicatif, sur Linux :

    python -m venv venv
    . venv/bin/activate
    pip install flask
    pip install flask-socketio gevent gevent-websocket
    pip install librosa soundfile
    
On peut alors soit lancer le serveur en lançant le fichier `main.py`, soit écrire un script (ce qui permet alors d'utiliser le débuggeur).
