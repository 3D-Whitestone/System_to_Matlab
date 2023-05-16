from .System import System
from ..Symbols import DynamicSymbol, StaticSymbol
from ..FileGenerators import MFile, MFunction, SFunction

import symengine as se
import sympy as sp

from typing import Any, Union


class StaticSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self._number_of_inputs = 0
        self._number_of_outputs = 0
        
    def addEquation(self, equation: Any) -> None:
        self._Equations.append(equation)
    
    def addInput(self, input: Any) -> None:
        """Adds an input to the system

        Args:
            input (Any): input which should be added to the system, has to be an expressions or a Matrix of expressions
        """
        self._number_of_inputs += 1
        self._Inputs.append(input)
    
    def addOutput(self, output: Union[se.Expr, se.Matrix], name: str) -> None:
        """Adds an output to the system y = h(x,u)

        Args:
            output (Union[se.Expr, se.Matrix]): output which should be added to the system, has to be an expressions or a Matrix of expressions
            name (str): name of the output
        """
        output = se.sympify(output)
        self._number_of_outputs += 1
        
        if self._Equations[1] is None:
            if type(output) == se.Matrix:
                self._Equations[1] = output
            else:
                self._Equations[1] = se.Matrix([output])
        else:
            if type(output) == se.Matrix:
                self._Equations[1] = self._Equations[1].col_join(output)
            else:
                self._Equations[1] = self._Equations[1].col_join(se.Matrix([output]))
        
        self._Outputs.append((output, StaticSymbol(name, len(output)).vars))
        
    def write_MFunctions(self, name:str, path:str = ""):
        Fdyn = MFunction(name + "_dyn", path)
        Fdyn.addInput(self.x, "x")
        Fdyn.addInput(self.u, "u")
        Fdyn.addOutput(self.x_dot, "xdot")
        Fdyn.addEquations(self._Equations[0], self.x_dot)
        Fdyn.addParameters(self._Parameters)
        Fdyn.generateFile()
        
        Fout = MFunction(name + "_out", path)
        Fout.addInput(self.x, "x")
        Fout.addOutput(self.y, "y")
        Fout.addEquations(self._Equations[1], self.y)
        Fout.addParameters(self._Parameters)
        Fout.generateFile()

    def write_init_File(self, name:str, path:str = ""):
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(sp.octave_code(para[0].subs(DynamicSymbol._Symbol_to_printable_dict)) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([sp.octave_code(para[0].subs(DynamicSymbol._Symbol_to_printable_dict)) for para in self._Parameters]) + "]; \n \n")
        File.addText(r"%% Initial conditions" + "\n")
        File.addText("x_ic = "+ sp.octave_code(self._x * 0) + ";\n")
        File.generateFile()