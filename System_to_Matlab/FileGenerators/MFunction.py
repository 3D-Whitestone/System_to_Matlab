import os
from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement
from ..Calculation.Calculation import Calculation
from ..Symbols.Symbol import Symbol

import symengine as se

from typing import Any


class MFunction(FileGenerator):
    """
    A class representing a mathematical function.

    Attributes:
        _Path (str): The path to the file where the function is stored.
        _Filename (str): The name of the file where the function is stored.
        _Inputs (list[Tuple[Any, str]]): A list of tuples representing the inputs of the function.
        _Outputs (list[Tuple[Any, str]]): A list of tuples representing the outputs of the function.
        _Equations (Tuple[se.Matrix, se.Matrix]): A tuple representing the equations of the function.
    """

    def __init__(self, filename: str, path: str = "") -> None:
        """Generates an instance of the MFunction class.

        Parameters
        ----------
        filename : str
            The name of the file to be generated. If the file does not end with .m, it will be added.
        path : str, optional
            Path in which the file should be saved , by default ""
        """
        if not filename.endswith(".m"):
            filename += ".m"
        super().__init__(filename, path)

        self._Outputs: list[se.Symbols | se.Function] = []
        self._Outputs_Calcs: Calculation = Calculation()
        self._Inputs: list[se.Symbols | se.Function] = []
        self._Input_Calcs: Calculation = Calculation()
        self._Calculations: Calculation = Calculation()

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

    def addCalculation(self, calc: Calculation) -> None:
        """Adds a calculation to the function.

        Parameters
        ----------
        calc : Calculation
            The calculation to be added.            
        """  # noqa: E501
        # if not isinstance(equations, (se.Expr, list, se.Matrix)):
        #     raise TypeError("The equations have to be a list, a matrix or a single expression")
        # if isinstance(equations, se.Expr):
        #     equations = se.Matrix([equations])
        # if isinstance(equations, list):
        #     equations = se.Matrix(equations)

        # if isinstance(name, str):
        #     name = se.Symbol(name)
        #     name = se.Matrix([name])
        # elif isinstance(name, se.Symbol):
        #     name = se.Matrix([name])
        # elif isinstance(name, list) and isinstance(name[0], str):
        #     name = se.Matrix([se.Symbol(na) for na in name])
        # elif isinstance(name, list) and isinstance(name[0], se.Symbol):
        #     name = se.Matrix([name])
        # elif isinstance(name, se.Matrix):
        #     pass
        # else:
        #     raise TypeError("The name has to be a list of strings, a list of symbols, a matrix of symbols or a single symbol")

        # if self._Calculations is None:
        #     self._Calculations = [name, equations]
        # else:
        #     self._Calculations[0].col_join(name)
        #     self._Calculations[1].col_join(equations)
        if not isinstance(calc, Calculation):
            raise TypeError(f"The calculation has to be a Calculation but {type(calc)} was given")
        self._Calculations.append_Calculation(calc)

    def generateFile(self, overwrite: bool = True) -> None:
        """Generates the file with the given name and path. If the file already exists, it will be overwritten (if you don't want this to happen set the overwrite to false).

        Parameters
        ----------
        overwrite : bool, optional
            Defines if the file should be overwritten , by default True
        """
        # if not overwrite and os.path.exists(self._Path + "\\" + self._Filename):
        if not overwrite and os.path.exists(os.path.join(self.path, self.filename)):
            print("File already exists")
            return
        
        sin = ""
        for i in self._Inputs:
            sin += str(i.subs(Symbol._Symbol_to_printable_dict)) + ", "
        sin = sin[:-2]
        sout  = ""
        for o in self._Outputs:
            sout += str(o.subs(Symbol._Symbol_to_printable_dict)) + ", "
        sout = sout[:-2]
        
        self._Elements.append(StringElement(
            "function [" + sout + "] = " + self._Filename.removesuffix(".m") + "(" + sin + ") \n"))

        self._Elements.append(CodeElement(self._Input_Calcs.append_Calculation(self._Calculations).append_Calculation(self._Outputs_Calcs), 1, True, False))
        

        # sin = ""
        # s_define = ""
        # for i in self._Inputs:
        #     (sin_temp, s_define_temp) = self._matlab_input_string_generator([i[0]], i[1])
        #     sin += sin_temp + ","
        #     s_define += s_define_temp
        # sin = sin[:-1]

        # sheader = ""
        # sbody_top = ""
        # sbody_bot = ""
        # for o in self._Outputs:
        #     (sheader_temp, sbody_top_temp, sbody_bot_temp) = self._matlab_output_string_generator([o[0]],
        #                                                                                           o[1])  # noqa: E501
        #     sheader += sheader_temp + ","
        #     sbody_top += sbody_top_temp
        #     sbody_bot += sbody_bot_temp

        # self._Elements.append(StringElement(
        #     "function [" + sheader[:-1] + "] = " + self._Filename.removesuffix(".m") + "(" + sin + ") \n"))
        # self._Elements.append(StringElement(s_define, 1))
        # self._Elements.append(StringElement(sbody_top, 1))

        # if self._Calculations is not []:
        #     for i in self._Calculations:
        #         # if i

        #         if self._Calculations[1].shape[0] == 1:
        #             self._Elements.append(CodeElement(self._Calculations[1], self._Calculations[0], 1, True, False))
        #         else:
        #             self._Elements.append(
        #                 CodeElement(self._Calculations[1][i], self._Calculations[0][i], 1, True, False))

        # self._Elements.append(StringElement(sbody_bot, 1))
        self._Elements.append(StringElement("end"))

        if self._Path is None or self._Path == "":
            path = self._Filename
        else:
            if self._Path.endswith("\\"):
                path = self._Path + self._Filename
            else:
                path = self._Path + "\\" + self._Filename
        with open(path, "w") as f:
            for element in self._Elements:
                f.write(element.generateCode())
