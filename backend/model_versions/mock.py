class MockModel():

    def name(self):
        return "MockModel"
        
    def description(self):
        return "Mock model that does not processes uploaded files."
        
    def steps(self):
        return [];
    
    """
        Effectue le traitement du modèle sur l'audio Librosa donné en paramètre. Envoie un lien vers le fichier résultat ou None si le traitement a échoué. Est lancé dans un thread séparé.
    """
    def process_audio(self, audio):
        print("Mock processing launched")
        return None
        
