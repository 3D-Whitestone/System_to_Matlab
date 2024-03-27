#from .System import System
from ..Symbols import StaticSymbol, StaticSymbols
from ..Symbols.Symbol import Symbol
from ..FileGenerators import MFile, MFunction
from ..Calculation.Calculation import Calculation

import symengine as se
import sympy as sp
from typing import Any, Union


class StaticSystem():
    def __init__(self) -> None:
        self._Equations: Calculation = Calculation()
        self._Outputs: list[se.Symbols | se.Function] = []
        self._Outputs_Calcs: Calculation = Calculation()
        self._Inputs: list[se.Symbols | se.Function] = []
        self._Input_Calcs: Calculation = Calculation()
    
    def addCalculation(self, name: Union[str, se.Symbol, list[str], Calculation], rhs: se.Expr = None) -> None:
        """Adding an Calculation to the System. Has to have the form name = rhs.
            name hast to be a Symbol or a string which can be converted to a Symbol
        Parameters
        ----------
        name : Union[str, se.Symbol, list[str]]
            Can be an Calculation object or,
            the name of the variable calculated in the equation. Must be a Symbol or a string that can be converted to a Symbol. 
        rhs : se.Expr, optional
            The calculation to be added to the system. Defaults to None.
        """

        if isinstance(name, Calculation):
            self._Equations.append_Calculation(name)
        else:
            calc = Calculation()
            calc.addCalculation(name, rhs)
            self._Equations.addCalculation(name, rhs)

        #self._Equations.append((rhs, name))
    
    def addInput(self, input: se.Symbol | se.Function | se.Matrix, name: str | se.Symbol = "") -> None:
        """Adds an input to the System.
        When a name is given the given Symbol/Matrix will be outputed with the given name.
        ----------
        input : se.Symbol | se.Function | se.Matrix
            The input to be added.
        name : str, optional
            The name of the input. If non is given the name of the Symbol itself is used. Defaults to "".
        """
        
        if isinstance(input, se.Matrix):
            if name == "":
                raise ValueError("Matrix inputs have to have a name")
            is_input_matrix = True
        else:
            is_input_matrix = False
        
        if name == "":
            self._Inputs.append(input)
        else:
            self._Inputs.append(se.Symbol(name))
            self._Input_Calcs.addCalculation(input, se.Symbol(name),is_matrix_input=is_input_matrix)
    
    def addOutput(self, output: se.Symbol | se.Function, name: str = "") -> None:
        """Adds an output to the System.
        When a name is given the given Symbol will be outputed with the given name.
        ----------
        output : se.Symbol | se.Function
            The output to be added.
        name : str, optional
            The name of the output. Defaults to "".
        """
        if name == "":
            self._Outputs.append(output)
        else:
            self._Outputs.append(se.Symbol(name))
            self._Outputs_Calcs.addCalculation(se.Symbol(name), output)

    
    # def addOutput(self, name: Union[str, se.Symbol, list[str], Calculation], rhs: se.Expr = None) -> None:
    #     """Adding an Output to the System. Has to have the form name = rhs.
    #     --------
    #     name : Union[str, se.Symbol, list[str]]
    #         Can be an Calculation object or,
    #         the name of the variable calculated in the equation. Must be a Symbol or a string that can be converted to a Symbol.
    #     rhs : se.Expr, optional
    #         The calculation to be added to the system. Defaults to None.
    #     """
    #     if isinstance(name, Calculation):
    #         self._Outputs.append_Calculation(name)
    #     else:
    #         calc = Calculation()
    #         calc.addCalculation(name, rhs)
    #         self._Outputs.addCalculation(name, rhs)
        
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
        Fdyn._Inputs = self._Inputs
        Fdyn._Outputs = self._Outputs
        Fdyn._Calculations.append_Calculation(self._Input_Calcs).append_Calculation(self._Equations).append_Calculation(self._Outputs_Calcs)
        
        Fdyn.generateFile()

    # def write_init_File(self, name:str, path:str = "", overwrite:bool = True):
    #     """Writes the init File for the (Static System) MFunction

    #     Parameters
    #     ----------
    #     name : str
    #         The name of the init file.
    #     path : str, optional
    #         The path where the file should be saved. Defaults to "".
    #     overwrite : bool, optional
    #         If True, the file will be overwritten if it already exists. Defaults to True.
    #     """
    #     File = MFile(name, path)
    #     File.addText(r"%% System parameters")
    #     File.addText("\n")
    #     for para in self._Parameters:
    #         File.addText(str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) + " = " + str(para[1]) + ";\n")
            
            
    #     File.addText(r"params = [" + ", ".join([str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) for para in self._Parameters]) + "]; \n \n")
    #     File.addText(r"%% Initial conditions" + "\n")
    #     File.generateFile(overwrite)