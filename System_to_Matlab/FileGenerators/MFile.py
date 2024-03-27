from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement
from ..Calculation.Calculation import Calculation
import os



class MFile(FileGenerator):
    def __init__(self, Filename:str, Path:str = None) -> None:  # type: ignore
        """Generates a .m file with the given name and path. The file will be empty until the generateFile method is called.

        Parameters
        ----------
        Filename : str
            The name of the file to be generated. If the file does not end with .m, it will be added.
        Path : str, optional
            The path where the file will be generated.  , by default None
        """
        if not Filename.endswith(".m"):
            Filename += ".m"
        super().__init__(Filename, Path)
        self._Elements = []
        
    def addText(self, text:str) -> None:
        """Adds a string to the file.

        Parameters
        ----------
        text : str
            The string to be added.
        """
        self._Elements.append(StringElement(text))
        
    def addCalculation(self, calculation: Calculation, use_cse: bool = True) -> None:
        """Adds a math expression to the file.

        Parameters
        ----------
       calculation: Calculation
            calculation to be added
        use_cse : bool, optional
            Whether to use common subexpression elimination, by default True
        """
        self._Elements.append(CodeElement(calculation, use_cse))
    
    def generateFile(self, overwrite: bool = True) -> None:
        """Generates the file with the given name and path. If the file already exists, it will be overwritten.

        Parameters
        ----------
        overwrite : bool, optional
            Whether to overwrite the file if it already exists, by default True
        """
        if not overwrite and os.path.exists(self._Path + "\\" + self._Filename):
            return
        if self._Path is None or self._Path == "":
            path = self._Filename
        else:
            if self._Path.endswith("\\"):
                path = self._Path + self._Filename
            else:
                path = self._Path + "\\" + self._Filename
        with open(path, "w") as f:
            for element in self._Elements:
                f.write(element.generateCode())
                