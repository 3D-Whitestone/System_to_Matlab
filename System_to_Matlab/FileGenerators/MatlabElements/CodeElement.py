from __future__ import annotations
from .MatlabElement import MatlabElement
from ...Symbols import DynamicSymbol
from ...Symbols.Symbol import Symbol
from ...Calculation.Calculation import Calculation

import symengine as se
import sympy as sp

from typing import Union, Any


class CodeElement(MatlabElement):
    def __init__(self, code: Calculation, indent: int = 0,  use_cse: bool = True, clear: bool = True):
        """ Code Element for the Matlab File Generator. Represents a chunk of code. Can also use cse to make the code more efficient.

        Parameters
        ----------
        code : Calculation
            code which should be generated
        indent : int, optional
            how much indents should be added at the front of every line, by default 0
        use_cse : bool, optional
            Sets if cse should be used on the code, by default True
        clear : bool, optional
            sets if the variables from cse should be cleared afterwards, by default True
        """
        MatlabElement.__init__(self)

        # if not isinstance(code, (list, se.Matrix)):
        #     code = se.Matrix([code])
        # else:
        #     code = se.Matrix(code)

        # if isinstance(name, str):
        #     name = se.Symbol(name)
        #     name = se.Matrix([name])
        # if isinstance(name, se.Symbol):
        #     name = se.Matrix([name])
            
        if not isinstance(code, Calculation):
            raise TypeError(f"code has to be a Calculation but {type(code)} was given")
        self._code: Calculation = code
        self._code.subs(Symbol._Symbol_to_printable_dict)
        # self._name = name.subs(
        #     Symbol._Symbol_to_printable_dict)  # type: ignore
        self._use_cse: bool = use_cse
        self._Indentation: int = indent
        self._Clear: bool = clear
        self._override: bool = False
        self._lhs: se.Symbol = None

    def override_lhs(self, lhs: se.Symbol) -> CodeElement:
        self._override = True
        self._lhs = lhs
        return self

    def generateCode(self) -> str:

        s = ""
        if self._use_cse:
            s += self._generate_cse()
        else:
            for i in range(len(self._code._calcs)):
                if self._override:
                    s += self._Indentation * "\t" + self._remove_curlyBreakets(sp.octave_code(self._lhs)) + " = " + self._remove_curlyBreakets(sp.octave_code(self._code._calcs[i])) + ";\n"
                else:
                    s += self._Indentation * "\t" + self._remove_curlyBreakets(sp.octave_code(self._code._vars[i])) + " = " + self._remove_curlyBreakets(sp.octave_code(self._code._calcs[i])) + ";\n"
            # s += self._remove_curlyBreakets(sp.octave_code(self.vars)) + " = " + self._remove_curlyBreakets(sp.octave_code(self._code)) + ";\n"
        return s

    def _generate_cse(self) -> str:
        s = ""

        indizes_shapes, code_vector = self._code._generate_shape_index_list()
        
        f1, f2 = se.cse(code_vector)
        for temp in f1:
            s += self._Indentation * "\t" + \
                self._remove_curlyBreakets(sp.octave_code(temp[0])) + " = " + \
                self._remove_curlyBreakets(sp.octave_code(temp[1])) + ";\n"  # type: ignore
        if f1 != []:
            s += "\n"

        ii = 0
        for i in indizes_shapes:
            index = i[0]
            shape = i[1]
            code = f2[index[0]:index[1]]
            if self._override:
                name = self._lhs
            else:
                name = self._code._vars[ii]
            ii += 1

            if shape == (1, 1):
                s += self._Indentation * "\t" + \
                    self._remove_curlyBreakets(sp.octave_code(name[0])) + " = " + \
                    self._remove_curlyBreakets(sp.octave_code(code)) + ";\n"  # type: ignore
            else:
                s += self._Indentation * "\t" + self._remove_curlyBreakets(sp.octave_code(name)) + " = " + sp.octave_code(
                    se.Matrix(code).reshape(shape[0], shape[1])) + ";\n"  # type: ignore
            # s += "\n"
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
            if s.endswith("\n\n\n"):
                s = s[:-2]
        return s

    def _remove_curlyBreakets(self, code: str) -> str:
        if code.startswith("{") and code.endswith("}"):
            code = code[1:-1]
        return code