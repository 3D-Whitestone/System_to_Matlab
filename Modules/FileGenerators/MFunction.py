import os
from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement

import symengine as se

from typing import Any


class MFunction(FileGenerator):
    def __init__(self, filename:str, path:str = "") -> None:
        if not filename.endswith(".m"):
            filename += ".m"
        super().__init__(filename, path)
        
        self._Inputs = []
        self._Outputs = []
        self._Parameters = []
        self._Equations = None
        
    def addInput(self, input:Any, name:str) -> None:
        self._Inputs.append((input, name))
        
    def addOutput(self, output:Any, name:str) -> None:
        self._Outputs.append((output, name))
    
    def addParameters(self, parameters: Any) -> None:
        self._Parameters.append(parameters)
    
    def addEquations(self, equations, name):
        """Adds equations to the function, the equations are represented in the following form. name = equation. 

        Args:
            equations (_type_): Expression, list of expressions or matrix of expressions.
            name (_type_): Symbol, list of symbols or matrix of symbols. or string, list of strings or matrix of strings.
        """  # noqa: E501
        equations = se.Matrix(equations)
        if type(name) == str:
            name = se.Symbol(name)
            name = se.Matrix([name])
        if type(name) == list:
            if type(name[0]) == str:
                l = []
                for na in name:
                    l.append(se.Symbol(na))
                name = se.Matrix(l)
        
        if self._Equations is None:
            self._Equations = [name, equations]
        else:
            self._Equations[0].col_join(name)
            self._Equations[1].col_join(equations)
        
    def generateFile(self, override = True) -> None:
        
        if not override and os.path.exists(self._Path + "\\" + self._Filename):
            return

        sin = ""
        s_define = ""
        for i in self._Inputs:
            (sin_temp, s_define_temp) = self._matlab_input_string_generator([i[0]],i[1])
            sin += sin_temp + ","
            s_define += s_define_temp
        sin = sin[:-1]
        
        sheader = ""
        sbody_top = ""
        sbody_bot = ""
        for o in self._Outputs:
            (sheader_temp, sbody_top_temp, sbody_bot_temp) = self._matlab_output_string_generator([o[0]],o[1])  # noqa: E501
            sheader += sheader_temp
            sbody_top += sbody_top_temp
            sbody_bot += sbody_bot_temp


        self._Elements.append(StringElement("function [" + sheader + "] = " + self._Filename.removesuffix(".m") + "(" + sin +") \n"))
        self._Elements.append(StringElement(s_define,1))
        self._Elements.append(StringElement(sbody_top,1))
        
        for i in range(self._Equations[1].shape[0]):
            self._Elements.append(CodeElement(self._Equations[1][i], self._Equations[0][i],1, True, False))
        
        self._Elements.append(StringElement(sbody_bot,1))
        self._Elements.append(StringElement("end"))

        
        if self._Path is None or self._Path == "":
            path = self._Filename
        else:
            path = self._Path + "\\" + self._Filename
        with open(path, "w") as f:
            for element in self._Elements:
                f.write(element.generateCode())