import uuid
import librosa

from database import query_db, execute_db

class Job():

    def __init__(self, id_, model, data):
        self.id = id_
        self.model = model
        self.current_data = data
        self.current_step = 0
        self.done = False
        
    """
        Effectue le traitement du modèle sur l'audio Librosa donné en paramètre. Envoie une sortie (qui dépend de la sortie de la dernière étape) ou None si le traitement a échoué. Est lancé dans un thread séparé.
    """
    def launch(self):
        if not self.done:
            while self.current_step < len(self.model.steps()) and self.current_data is not None:
                self.current_data = self.model.steps()[self.current_step].start(self.current_data)
                self.current_step += 1
            self.done = True
        return self.current_data
        
    def launch_and_save(self, processed_folder, database, app):
        with app.app_context():
            self.launch()
            s_f = str(uuid.uuid4())
            processed = processed_folder + s_f
            with open(processed, 'w') as f:
                if self.current_data is not None:
                    f.write(str(self.current_data))
                else:
                    f.write(b'')
            execute_db('UPDATE "jobs" SET "output" = ? WHERE "job_id" = ?', database, args=(processed, self.id))
            
    def to_dict(self):
        result = dict()
        return result

import model_versions
    
def load_job_from_db(job_id, database, app):
    with app.app_context():
        job = query_db('SELECT * FROM "jobs" WHERE "job_id" = ?', database, args=(job_id,), one=True)
        if job is not None:
            version = model_versions.versions[job[1]]
            output = job[3]
            if output is not None:
                with open(output, 'rb') as f:
                    job = Job(job_id, version, f.read())
                    job.current_step = len(version.steps())-1
                    job.done = True
                    return job
            else:
                audio = librosa.load(job[2])
                return Job(job_id, version, audio)
        else:
            return None

