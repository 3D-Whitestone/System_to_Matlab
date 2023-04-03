from abc import ABC, abstractmethod
import symengine as se
import sympy as sp
from ...Symbols.DynamicSymbols import DynamicSymbols

class MatlabElement(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def generateCode(self) -> str:
        pass
    
    
    
            
            
            
            
            
            