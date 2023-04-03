from Modules.Symbols.Symbols import Symbols
import symengine as se

from typing import Union, List

class StaticSymbols(Symbols):
    def __init__(self, Notation: str, number_of_variables: int = 1) -> None:
        super().__init__(Notation)
        self._number_of_variables = number_of_variables
        self._gen_numbered_state_variables()
    
    @property
    def vars(self) -> se.Matrix:
        return se.Matrix(self._Symbols)
    
        
    def _gen_numbered_state_variables(self)-> None:
        if self._number_of_variables == 1:
            self._Symbols.append(se.Symbol(self._Notation))
            self._Symbol_to_printable_dict.update({self._Symbols[0]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation))})
        
        for i in range(self._number_of_variables):
            self._Symbols.append(se.Symbol(self._Notation + f"_{i}"))
            
            self._Symbol_to_printable_dict.update({self._Symbols[i]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation + str(i)))})
        
    
    def _repr_latex_(self) -> str:
        return self.vars._repr_latex_()
    
    