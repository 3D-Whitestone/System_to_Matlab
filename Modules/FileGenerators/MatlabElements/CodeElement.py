from .MatlabElement import MatlabElement
from ...Symbols import DynamicSymbol


import symengine as se
import sympy as sp

from typing import Union, Any

class CodeElement(MatlabElement):
    def __init__(self, code, name: str, indent:int = 0 ,  use_cse:bool = True, clear:bool = True):
        MatlabElement.__init__(self)
        
        if type(code) != list or type(code) != se.Matrix:
            code = se.Matrix([code])
        else:
            code = se.Matrix(code)
        if type(name) == str:
            name = se.Symbol(name)
            name = se.Matrix([name])
        if type(name) == list:
            if type(name[0]) == str:
                l = []
                for na in name:
                    l.append(se.Symbol(na))
                name = se.Matrix(l)
        
        self._code = code.subs(DynamicSymbol._Symbol_to_printable_dict)
        self._name = name.subs(DynamicSymbol._Symbol_to_printable_dict)
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
    
    def _generate_cse(self, code: se.Matrix, name:str) -> str:
        #TODO allow cse for list of Matrices to maybe enhance the performance
        # But this code in the File generator to make use cse on the whole code no only on each block individually
        s = ""
        
        shape = code.shape
        
        f1, f2 = se.cse(code)
        for temp in f1:
            s += self._Indentation *"\t" + sp.octave_code(temp[0]) + " = " + sp.octave_code(temp[1]) + ";\n"
        s += "\n"
        
        if shape is (1,1):
            s += self._Indentation *"\t" + sp.octave_code(name[1,1]) + " = " + sp.octave_code(f2) + ";\n"
        else:
            s += self._Indentation *"\t" + sp.octave_code(name) + " = " + sp.octave_code(se.Matrix(f2).reshape(shape[0], shape[1])) + ";\n"
        s += "\n"
        if self._Clear:
            s += self._Indentation *"\t" + "clear "
            for temp in f1:
                s += sp.octave_code(temp[0]) + ", "
            s = s[:-2]
            s += "; \n \n"
        return s