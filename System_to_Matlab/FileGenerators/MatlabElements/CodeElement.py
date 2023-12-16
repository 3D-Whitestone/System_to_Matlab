from .MatlabElement import MatlabElement
from ...Symbols import DynamicSymbol
from ...Symbols.Symbol import Symbol


import symengine as se
import sympy as sp

from typing import Union, Any


class CodeElement(MatlabElement):
    def __init__(self, code, name: str, indent: int = 0,  use_cse: bool = True, clear: bool = True):
        """ Code Element for the Matlab File Generator. Represents a chunk of code. Can also use cse to make the code more efficient.

        Parameters
        ----------
        code : list, se.Matrix
            code which should be generated
        name : str oo se.Symbol
            Name of the varibal in which the result of the code should be stored
        indent : int, optional
            how much indents should be added at the front of every line, by default 0
        use_cse : bool, optional
            Sets if cse should be used on the code, by default True
        clear : bool, optional
            sets if the variables from cse should be cleared afterwards, by default True
        """
        MatlabElement.__init__(self)

        if not isinstance(code, (list, se.Matrix)):
            code = se.Matrix([code])
        else:
            code = se.Matrix(code)

        if isinstance(name, str):
            name = se.Symbol(name)
            name = se.Matrix([name])
        if isinstance(name, se.Symbol):
            name = se.Matrix([name])
            

        self._code = code.subs(Symbol._Symbol_to_printable_dict)
        self._name = name.subs(
            Symbol._Symbol_to_printable_dict)  # type: ignore
        self._use_cse = use_cse
        self._Indentation = indent
        self._Clear = clear

    def generateCode(self) -> str:

        s = ""
        if self._use_cse:
            s += self._generate_cse(self._code, self._name)
        else:
            s += self._remove_curlyBreakets(sp.octave_code(self._name)) + " = " + self._remove_curlyBreakets(sp.octave_code(self._code)) + ";\n"
        return s

    def _generate_cse(self, code: se.Matrix, name: str) -> str:
        # TODO allow cse for list of Matrices to maybe enhance the performance
        # But this code in the File generator to make use cse on the whole code no only on each block individually
        s = ""

        shape = code.shape

        f1, f2 = se.cse(code)
        for temp in f1:
            s += self._Indentation * "\t" + \
                self._remove_curlyBreakets(sp.octave_code(temp[0])) + " = " + \
                self._remove_curlyBreakets(sp.octave_code(temp[1])) + ";\n"  # type: ignore
        s += "\n"

        if shape == (1, 1):
            s += self._Indentation * "\t" + \
                self._remove_curlyBreakets(sp.octave_code(name[0, 0])) + " = " + \
                self._remove_curlyBreakets(sp.octave_code(f2)) + ";\n"  # type: ignore
        else:
            s += self._Indentation * "\t" + self._remove_curlyBreakets(sp.octave_code(name)) + " = " + sp.octave_code(
                se.Matrix(f2).reshape(shape[0], shape[1])) + ";\n"  # type: ignore
        s += "\n"
        if self._Clear:
            s += self._Indentation * "\t" + "clear "
            for temp in f1:
                s += self._remove_curlyBreakets(sp.octave_code(temp[0])) + " "  # type: ignore
            if s.endswith("clear "):
                s = s[:-6]
            else:
                s = s[:-1]
                s += ";"
            s += "\n"
        return s

    def _remove_curlyBreakets(self, code: str) -> str:
        if code.startswith("{") and code.endswith("}"):
            code = code[1:-1]
        return code