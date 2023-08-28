from abc import ABC, abstractmethod
from typing import Any


class System(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._Equations: list = []
        self._Parameters: list = []
        self._Inputs: list = []
        self._Outputs: list = []

        
    @abstractmethod 
    def addInput(self, input: Any, name:str) -> None:
        pass
        
    @abstractmethod  
    def addOutput(self, output: Any, name:str) -> None:
        pass
    
    