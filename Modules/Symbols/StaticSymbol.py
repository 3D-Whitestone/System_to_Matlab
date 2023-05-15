from .Symbol import Symbol
import symengine as se

from typing import Union, List

class StaticSymbol(Symbol):
    def __init__(self, Notation: str, number_of_variables: int = 1) -> None:
        super().__init__(Notation)
        self._number_of_variables = number_of_variables
        self._gen_numbered_state_variables()
    
    @property
    def vars(self) -> se.Matrix:
        return se.Matrix(self._Symbols)
    
        
    def _gen_numbered_state_variables(self) -> None:
        if self._number_of_variables == 1:
            s, s_sub = self._generate_Latex_string(self._Notation, 1, 0)
            self._Symbols.append(se.Symbol(s))
            self._Symbol_to_printable_dict.update({self._Symbols[0]: se.Symbol(self._remove_unwanted_chars_for_Matlab(s))})
            #self._Symbols.append(se.Symbol(self._Notation))
            #self._Symbol_to_printable_dict.update({self._Symbols[0]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation))})
        else:
            for i in range(1, self._number_of_variables + 1):
                s, s_sub = self._generate_Latex_string(self._Notation, i, 0)
                self._Symbols.append(se.Symbol(s))
                #self._Symbols.append(se.Symbol(self._Notation + f"_{i}"))
                self._Symbol_to_printable_dict.update({self._Symbols[i-1]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._remove_unwanted_chars_for_Matlab(s_sub)))})
        
    
    def _repr_latex_(self) -> str:
        return self.vars._repr_latex_()
    

def StaticSymbols(names: List[str], number_of_variables: int = 1) -> List[se.Symbol]:
    l = []
    if number_of_variables == 1:
        for s in names:
            l.append(StaticSymbol(s,number_of_variables).vars[0])
    else:    
        for s in names:
            l.append(StaticSymbol(s,number_of_variables).var_as_vec())
    
    
    return l