from .MatlabElement import MatlabElement
from ...Symbols import DynamicSymbol


import symengine as se
import sympy as sp

from typing import Union, Any

class CodeElement(MatlabElement):
    def __init__(self, code, name: str, indent:int = 0 ,  use_cse:bool = True, clear:bool = True):
        MatlabElement.__init__(self)
        if type(code) == list:
            code = se.Matrix(code)
        self._code = code.subs(DynamicSymbol._Symbol_to_printable_dict)
        self._name = name
        self._use_cse = use_cse
        self._Indentation = indent
        self._Clear = clear

    def generateCode(self) -> str:
        s = ""
        if self._use_cse:
            s += self._generate_cse(self._code, self._name)
        else:
            s += self._name + " = " + sp.octave_code(self._code) + ";\n"
        return s
    
    def _generate_cse(self, code: Union[Any, se.Matrix], name:str) -> str:
        #TODO allow cse for list of Matrices to maybe enhance the performance
        # But this code in the File generator to make use cse on the whole code no only on each block individually
        shape = None
        s = ""
        
        if type(code) == se.Matrix:
            shape = code.shape
            
        f1, f2 = se.cse(code)
        for temp in f1:
            s += self._Indentation *"\t" + sp.octave_code(temp[0]) + " = " + sp.octave_code(temp[1]) + ";\n"
        s += "\n"
        
        if shape is None:
            s += self._Indentation *"\t" + name + " = " + sp.octave_code(f2) + ";\n"
        else:
            s += self._Indentation *"\t" + name + " = " + sp.octave_code(se.Matrix(f2).reshape(shape[0], shape[1])) + ";\n"
        s += "\n"
        if self._Clear:
            s += self._Indentation *"\t" + "clear "
            for temp in f1:
                s += sp.octave_code(temp[0]) + ", "
            s = s[-2]
            s += "; \n \n"
        return s