from abc import ABC, abstractmethod
import symengine as se
import sympy as sp
from ...Symbols import DynamicSymbol

class MatlabElement(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def generateCode(self) -> str:
        pass
    
    
    
            
            
            
            
            
            