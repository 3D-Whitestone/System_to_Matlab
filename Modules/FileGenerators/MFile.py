from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement
import os



class MFile(FileGenerator):
    def __init__(self, Filename:str, Path:str = None) -> None:
        if not Filename.endswith(".m"):
            Filename += ".m"
        super().__init__(Filename, Path)
        self._Elements = []
        
    def addText(self, text:str) -> None:
        self._Elements.append(StringElement(text))
        
    def addMathExpression(self, expression, name , use_cse = True) -> None:
        self._Elements.append(CodeElement(expression, name, use_cse))
    
    
    def generateFile(self, override = True) -> None:
        if not override and os.path.exists(self._Path + "\\" + self._Filename):
            return
        if self._Path is None or self._Path == "":
            path = self._Filename
        else:
            path = self._Path + "\\" + self._Filename
        with open(path, "w") as f:
            for element in self._Elements:
                f.write(element.generateCode())
                