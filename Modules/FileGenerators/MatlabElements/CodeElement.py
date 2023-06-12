from .MatlabElement import MatlabElement
from ...Symbols import DynamicSymbol
from ...Symbols.Symbol import Symbol


import symengine as se
from symengine.lib.symengine_wrapper import FunctionSymbol
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
        elif type(name) == list:
            if type(name[0]) == str:
                l = []
                for na in name: # type: ignore
                    l.append(se.Symbol(na))
                name = se.Matrix(l)
        elif type(name) == se.Matrix or type(name) == sp.Matrix:
            name = se.sympify(name)
        elif type(name) == FunctionSymbol or type(name) == se.Symbol or type(name) == sp.Function or type(name) == sp.Symbol:
            name = se.Matrix([name])
        else:
            display(type(name))
            raise TypeError("name must be a string or a list of strings")
        
        self._code = code.subs(Symbol._Symbol_to_printable_dict)
        self._name = name.subs(Symbol._Symbol_to_printable_dict)  # type: ignore
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
            s += self._Indentation *"\t" + sp.octave_code(temp[0]) + " = " + sp.octave_code(temp[1]) + ";\n" # type: ignore
        s += "\n"
        
        if shape == (1,1):
            s += self._Indentation *"\t" + sp.octave_code(name[0,0]) + " = " + sp.octave_code(f2) + ";\n"  # type: ignore
        else:
            s += self._Indentation *"\t" + sp.octave_code(name) + " = " + sp.octave_code(se.Matrix(f2).reshape(shape[0], shape[1])) + ";\n"  # type: ignore
        s += "\n"
        if self._Clear:
            s += self._Indentation *"\t" + "clear "
            for temp in f1:
                s += sp.octave_code(temp[0]) + ", "  # type: ignore
            if s.endswith("clear "):
                s = s[:-6]
            else:
                s = s[:-2]
                s += ";"
            s += "\n"
        return s