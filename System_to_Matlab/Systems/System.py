from abc import ABC, abstractmethod
from typing import Any


class System(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._Equations: list = []
        self._Parameters: list = []
        self._Inputs: list = []
        self._Outputs: list = []

    def addParameter(self, parameter: Any, values = 0) -> None:
        """adds a parameter to the system

        Args:
            parameter (Any): parameter which should be added to the system, has to be a symbol or a Matrix of symbols
            
            values (Union[None, Any], optional): values for the parameter. Either a list or a column Matrix.
            Defaults to None.
        """
        parameter = list(parameter)
        if values == 0:
            values = list(0 for i in range(len(parameter)))
        if len(parameter) != len(values):
            raise ValueError("Number of parameters and values does not match")
        
        self._Parameters.extend(list(zip(parameter, values)))
        
    @abstractmethod 
    def addInput(self, input: Any, name:str) -> None:
        pass
        
    @abstractmethod  
    def addOutput(self, output: Any, name:str) -> None:
        pass
    
    