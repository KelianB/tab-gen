from .mock import MockModel

versions = {
    0: MockModel()
}

class Step():
    def __init__(self, name, func):
        self.name = name
        self.__func__ = func
        
    def start(self, input_):
        return self.__func__(input_)

