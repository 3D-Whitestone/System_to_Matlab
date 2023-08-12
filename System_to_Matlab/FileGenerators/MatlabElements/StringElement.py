from .MatlabElement import MatlabElement

class StringElement(MatlabElement):
    def __init__(self, value:str , indent:int = 0 ):
        MatlabElement.__init__(self)
        self._value = value
        self._Indentation = indent
        
    def generateCode(self) -> str:
        self._value = self._Indentation * "\t" + self._value.replace("\n","\n" + self._Indentation * "\t")
        while self._value.endswith("\t"):
            self._value = self._value[:-1]
        return self._value