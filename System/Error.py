

#Object to transport errors

class Error():

    def __init__(self, error):
        self._error = error
        pass

    def get(self):
        return self._error
    
    def print(self):
        print(self._error)
        return self
    pass