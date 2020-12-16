class MockModel():

    def name(self):
        return "MockModel"
        
    def description(self):
        return "Mock model that does not processes uploaded files."
        
    def steps(self):
        return [];
        
    def processFile(self, _file):
        print("Mock processing launched : " + _file.name)
        
