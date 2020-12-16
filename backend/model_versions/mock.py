class MockModel():

    def name(self):
        return "MockModel"
        
    def description(self):
        return "Mock model that does not processes uploaded files."
        
    def processFile(self, _file):
        print("Mock processing launched : " + _file.name)
        
