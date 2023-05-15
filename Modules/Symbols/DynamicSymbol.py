from .Symbol import Symbol
import symengine as se
import sympy as sp
from typing import Union, List

from warnings import warn


class DynamicSymbol(Symbol):
    _dict_of_derivation_for_substitutions: dict = {}
    _derivation_variable: se.Symbol = se.Symbol("t", real=True)
    _dict_of_steady_state_substitutions: dict = {}

    def __init__(self, Notation: str, number_of_variables: int = 1, number_of_derivatives: int = 0) -> None:
        if number_of_variables <= 0:
            raise ValueError("number of variables has to be greater than 0")
        super().__init__(Notation)
        self._number_of_variables = number_of_variables
        self._number_of_derivatives = number_of_derivatives
        self._gen_numbered_state_variables()
        if number_of_derivatives > 0:
            self._gen_differentiation_dict()

    @property
    def vars(self) -> Union[se.MutableDenseMatrix, List[se.MutableDenseMatrix]]:
        if self._number_of_derivatives == 0:
            return se.Matrix(self._Symbols)
        else:
            v = []
            for i in range(self._number_of_derivatives + 1):
                v.append(se.Matrix(self._Symbols).reshape(
                    self._number_of_variables, self._number_of_derivatives + 1)[:, i])

            return v

    def _gen_numbered_state_variables(self):
        if self._number_of_variables == 1:

            s, s_sub = self._generate_Latex_string(self._Notation, 0, 0)
            self._Symbols.append(se.Function(s)(self._derivation_variable))
            self._Symbol_to_printable_dict.update(
                {self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(s))})
            # self._Symbols.append(se.Function(self._Notation)(self._derivation_variable))
            # self._Symbol_to_printable_dict.update({self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation))})

            for ii in range(1, self._number_of_derivatives + 1):
                s1: str = self._Notation[0]
                if len(self._Notation) > 1:
                    s2: str = self._Notation[1:]
                else:
                    s2: str = ""

                if ii == 1:
                    s: str = "\dot{" + f"{s1}}}{s2}"
                    s_sub: str = self._Notation + "dot"
                elif ii == 2:
                    s: str = "\ddot{" + f"{s1}}}{s2}"
                    s_sub: str = self._Notation + "ddot"
                else:
                    s: str = self._Notation + f"^({ii})"
                    s_sub: str = self._Notation + ii*"d" + "ot"

                s, s_sub = self._generate_Latex_string(self._Notation, 0, ii)

                self._Symbols.append(se.Function(s)(self._derivation_variable))

                self._Symbol_to_printable_dict.update(
                    {self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(s_sub))})

        else:
            for i in range(1, self._number_of_variables + 1):
                s, s_sub = self._generate_Latex_string(self._Notation, i, 0)

                self._Symbols.append(se.Function(s)(self._derivation_variable))
                self._Symbol_to_printable_dict.update(
                    {self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(s))})

                # self._Symbols.append(se.Function(self._Notation + f"_{i}")(self._derivation_variable))
                # self._Symbol_to_printable_dict.update({self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation + f"_{i}"))})

                for ii in range(1, self._number_of_derivatives + 1):
                    s1: str = self._Notation[0]
                    if len(self._Notation) > 1:
                        s2: str = self._Notation[1:]
                    else:
                        s2: str = ""

                    if ii == 1:
                        s: str = "\dot{" + f"{s1}}}{s2}_{i}"
                        s_sub: str = self._Notation + f"{i}" + "dot"
                    elif ii == 2:
                        s: str = "\ddot{" + f"{s1}}}{s2}_{i}"
                        s_sub: str = self._Notation + f"{i}" + "ddot"
                    else:
                        s: str = self._Notation + f"^{{({ii})}}" + f"_{i}"
                        s_sub: str = self._Notation + f"{i}" + ii*"d" + "ot"

                    s, s_sub = self._generate_Latex_string(
                        self._Notation, i, ii)

                    self._Symbols.append(se.Function(
                        s)(self._derivation_variable))
                    self._Symbol_to_printable_dict.update(
                        {self._Symbols[-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(s_sub))})

    def _gen_differentiation_dict(self):
        for i in range(len(self.vars) - 1):
            for ii in range(self._number_of_variables):
                self._dict_of_derivation_for_substitutions.update(
                    {se.diff(self.vars[i][ii], self._derivation_variable): self.vars[i+1][ii]})

    # def _gen_steady_state_substitutions(self):
    #     for i in range(len(self.vars)):
    #         for ii in range(self._number_of_variables):
    #             self._dict_of_steady_state_substitutions.update({self.vars[i][ii]: self.vars[0][ii]})

    def _repr_latex_(self):
        return se.Matrix(self._Symbols).reshape(self._number_of_variables, self._number_of_derivatives + 1)._repr_latex_()


def DynamicSymbols(names: List[str], number_of_variables: int = 1, number_of_derivatives: int = 0, as_matrx_list = False) -> List[DynamicSymbol]:
    l = []
    
    if as_matrx_list:  
        for s in names:
            l.append(DynamicSymbol(s, number_of_variables,
                    number_of_derivatives).var_as_vec())
    
    else:
        for s in names:
            l.append(DynamicSymbol(s, number_of_variables,
                    number_of_derivatives).var_as_vec())

        m = se.Matrix(l).reshape(len(names)*number_of_variables,
                                (number_of_derivatives + 1))
        l = []
        for i in range(number_of_derivatives + 1):
            l.append(list(m[:, i]))

    return l


def _diff_t(expression):
    """calculates the time derivativ of the expression an substitutes the correct symbols

    Args:
        expression (Any): expression which should be differentiated

    Returns:
        Any: differentiated expression with correct symbols
    """
    return se.diff(expression, DynamicSymbol._derivation_variable).subs(DynamicSymbol._dict_of_derivation_for_substitutions)
