from .System import System
from ..Symbols import StaticSymbol
from ..Symbols.Symbol import Symbol
from ..FileGenerators import MFile, MFunction

import symengine as se
import sympy as sp
from typing import Any, Union, List


class StaticSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self._Equations = []
        
    def addAdditionalEquation(self, rhs: se.Expr, name: Union[str, se.Symbol, List[str]]) -> None:
        """Adding an Equation to the System. Has to have the form name = rhs.
            name hast to be a Symbol or a string which can be converted to a Symbol

        Parameters
        ----------
        rhs : se.Expr
            The calculation to be added to the system.
        name : Union[str, se.Symbol, List[str]]
            The name of the variable calculated in the equation. Must be a Symbol or a string that can be converted to a Symbol.
        """
    
        self._Equations.append((rhs, name))
    
    def addInput(self, input: Any, name: str) -> None:
        """Adds an input to the system

        Parameters
        ----------
        input : Any
            The input to be added to the system. Must be an expression or a matrix of expressions.
        """
        # self._Inputs.append((input, StaticSymbol(name, len(input)).vars))
        self._Inputs.append((input, name))
    
    def addOutput(self, output: Union[se.Expr, se.Matrix], name: str) -> None:
        """Adds an output to the system y = f(x), this output can only use values defined as an input or as a parameter

        Parameters
        ----------
        output : Union[se.Expr, se.Matrix]
            The output to be added to the system. Must be an expression or a matrix of expressions.
        name : str
            The name of the output.
        """
        output = se.sympify(output)
        
        self._Outputs.append((output, name))
        # self._Outputs.append((output, StaticSymbol(name, len(output)).vars))
        
    def write_MFunctions(self, name:str, path:str = "", overwrite:bool = True):
        """ Writes the MFunction 

        Parameters
        ----------
        name : str:
            Name of the MFunction
        path : str, optional
            Path where the File should be saved . Defaults to "".
        overwrite : bool, optional
            If the File should be overwritten if it already exists. Defaults to True.
        """
        
        Fdyn = MFunction(name , path)
        for i in self._Inputs:
            Fdyn.addInput(i[0], i[1])
        
        #pars = []
        #for i in self._Parameters:
        #    pars.append(i[0])
        
        #Fdyn.addInput(pars, "params")
        
        for i in self._Outputs:
            Fdyn.addOutput(i[0], i[1])

        for i in self._Equations:
            Fdyn.addEquations(i[0], i[1])
            
        # Fdyn.addParameters(self._Parameters)
        Fdyn.generateFile()

    def write_init_File(self, name:str, path:str = "", overwrite:bool = True):
        """Writes the init File for the (Static System) MFunction

        Parameters
        ----------
        name : str
            The name of the init file.
        path : str, optional
            The path where the file should be saved. Defaults to "".
        overwrite : bool, optional
            If True, the file will be overwritten if it already exists. Defaults to True.
        """
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) for para in self._Parameters]) + "]; \n \n")
        File.addText(r"%% Initial conditions" + "\n")
        File.generateFile(overwrite)