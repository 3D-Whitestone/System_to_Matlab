from .System import System

from typing import Any


class StaticSystem(System):
    def __init__(self) -> None:
        super().__init__()
        
    def addEquation(self, equation: Any) -> None:
        self._Equations.append(equation)
    
    def addInput(self, input: Any) -> None:
        self._Inputs.append(input)
    
    def addOutput(self, output: Any) -> None:
        self._Outputs.append(output)