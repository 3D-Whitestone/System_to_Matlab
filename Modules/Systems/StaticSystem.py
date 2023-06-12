from .System import System
from ..Symbols import DynamicSymbol, StaticSymbol
from ..Symbols.Symbol import Symbol
from ..FileGenerators import MFile, MFunction, SFunction

import symengine as se
import sympy as sp

from typing import Any, Union


class StaticSystem(System):
    """Adding an Equation to the System. Has to have the form name = rhs.
            name hast to be a Symbol or a string which can be converted to a Symbol

        Args:
            rhs (se.Expr): calculation which should be added to the system
            name (Union[str, se.Symbol]): name of the variable calculated in the equation
    """
    def __init__(self) -> None:
        super().__init__()
        self._Equations = []
        
    def addAdditionalEquation(self, rhs: se.Expr, name: Union[str, se.Symbol]) -> None:
        """Adding an Equation to the System. Has to have the form name = rhs.
            name hast to be a Symbol or a string which can be converted to a Symbol

        Args:
            rhs (se.Expr): calculation which should be added to the system
            name (Union[str, se.Symbol]): name of the variable calculated in the equation
        """
        if type(name) == str:
            name = StaticSymbol(name).vars
        
        self._Equations.append((rhs, name))
    
    def addInput(self, input: Any, name: str) -> None:
        """Adds an input to the system

        Args:
            input (Any): input which should be added to the system, has to be an expressions or a Matrix of expressions
        """
        # self._Inputs.append((input, StaticSymbol(name, len(input)).vars))
        self._Inputs.append((input, name))
    
    def addOutput(self, output: Union[se.Expr, se.Matrix], name: str) -> None:
        """Adds an output to the system y = f(x), this output can only use values defined as an input or as a parameter

        Args:
            output (Union[se.Expr, se.Matrix]): output which should be added to the system, has to be an expressions or a Matrix of expressions
            name (str): name of the output
        """
        output = se.sympify(output)
        
        #if self._Equations[1] is None:
        #    if type(output) == se.Matrix:
        #        self._Equations[1] = output
        #    else:
        #        self._Equations[1] = se.Matrix([output])
        #else:
        #    if type(output) == se.Matrix:
        #        self._Equations[1] = self._Equations[1].col_join(output)
        #    else:
        #        self._Equations[1] = self._Equations[1].col_join(se.Matrix([output]))
        
        self._Outputs.append((output, name))
        # self._Outputs.append((output, StaticSymbol(name, len(output)).vars))
        
    def write_MFunctions(self, name:str, path:str = ""):
        Fdyn = MFunction(name , path)
        for i in self._Inputs:
            Fdyn.addInput(i[0], i[1])
        for i in self._Outputs:
            Fdyn.addOutput(i[0], i[1])

        for i in self._Equations:
            Fdyn.addEquations(i[0], i[1])
            
        # Fdyn.addParameters(self._Parameters)
        Fdyn.generateFile()

    def write_init_File(self, name:str, path:str = ""):
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) for para in self._Parameters]) + "]; \n \n")
        File.addText(r"%% Initial conditions" + "\n")
        File.generateFile()