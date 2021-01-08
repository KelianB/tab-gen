class Job():

    def __init(self, id_, model, data):
        self.id = id_
        self.model = model
        self.current_data = data
        self.current_step = 0
        self.done = False
        
    """
        Effectue le traitement du modèle sur l'audio Librosa donné en paramètre. Envoie une sortie (qui dépend de la sortie de la dernière étape) ou None si le traitement a échoué. Est lancé dans un thread séparé.
    """
    def launch():
        if not self.done:
            while self.current_step < len(self.model.steps()) and self.current_data is not None:
                self.current_data = self.model.steps()[self.current_step].start(self.current_data)
                self.current_step += 1
            self.done = True
        return self.current_data

