import os
from .FileGenerators import FileGenerator

import symengine as se
import sympy as sp
from Modules.Symbols.DynamicSymbols import DynamicSymbols

from typing import Union, Any, List, Tuple


class MFunction(FileGenerator):
    def __init__(self, filename:str, path:str = "") -> None:
        super().__init__(filename, path)
        if not filename.endswith(".m"):
            filename += ".m"
        
        self._Filename = filename
        self._Path = path
        
        self._inputs = []
        self._outputs = []
        self._params = []
        self._equations = []
        
    def addInput(self, input:Any, name:str) -> None:
        self._inputs.append((input, name))
        
    def addOutput(self, output:Any, name:str) -> None:
        self._outputs.append((output, name))
    
    def addParameters(self, parameters: Any) -> None:
        self._params.append(parameters)
    
    def addEquations(self, equations: Union[se.Eq, List[se.Eq]]):
        """adds equations to the MFunction

        Parameters
        ----------
        equations : Union[se.Eq, List[se.Eq]]
            Equation or list of equations to add to the MFunction,
            only use single line equations 
        """
        self._equations.append(equations)
        
    def generateMFunction(self, path: str = None, override = True):
        
        if not override and os.path.exists(path + "MFun" + self._filename):
            return

        with open(path + "\MFun" + self._filename, "w") as mfile:
            (sin, s_define) = self._matlab_input_string_generator(self._inputs)
            (sheader, sbody_top, sbody_bot) = self._matlab_output_string_generator(self._outputs)
            
            mfile.write("function [" + sheader + "] = " + self._filename.removesuffix(".m") + "(" + sin +") \n")
            mfile.write(s_define)
            mfile.write(sbody_top)
            
            #TODO use symengine cse when atan2 works
            
            #TODO use the equations structure
            f1, f2 = sp.cse(eqs[1].subs(DynamicSymbols._dict_of_variable_and_symbols))
            f2 = f2[0]
            for eq in f1:
                mfile.write(str(eq[0]) + " = " +sp.octave_code(eq[1]) + ";\n")
            
            for i in range(len(eqs[0])):
                mfile.write(sp.octave_code(eqs[0][i].subs(DynamicSymbols._dict_of_variable_and_symbols)) + " = " + sp.octave_code(f2[i]) + "; \n")
                
            mfile.write(sbody_bot)
            mfile.write("end")
            mfile.close()