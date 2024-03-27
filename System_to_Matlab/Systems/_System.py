from abc import ABC, abstractmethod
from typing import Any
from ..Calculation.Calculation import Calculation

class System(ABC):
    """Abstract base class for all systems.
    """
    def __init__(self) -> None:
        super().__init__()
        self._Parameters: list = []
        self._Inputs: list = []

        
    @abstractmethod 
    def addInput(self, input: Any, name:str) -> None:
        pass
        
    @abstractmethod  
    def addOutput(self, output: Any, name:str) -> None:
        pass
    
    