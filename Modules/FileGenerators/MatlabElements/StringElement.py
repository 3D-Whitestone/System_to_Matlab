from .MatlabElement import MatlabElement

class StringElement(MatlabElement):
    def __init__(self, value:str):
        MatlabElement.__init__(self)
        self._value = value
        
    def generateCode(self) -> str:
        return self._value