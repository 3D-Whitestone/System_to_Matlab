from .Symbol import Symbol
import symengine as se

from typing import Union, List

class StaticSymbol(Symbol):
    """generates an instance of the StaticSymbol class

        Parameters
        ----------
        Notation : str
            Name of the Symbol
        number_of_variables : int, optional
            Number of variables which should be created, by default 1
    """
    def __init__(self, Notation: str, number_of_variables: int = 1) -> None:
        """generates an instance of the StaticSymbol class

        Parameters
        ----------
        Notation : str
            Name of the Symbol
        number_of_variables : int, optional
            Number of variables which should be created, by default 1
        """
        super().__init__(Notation)
        self._number_of_variables = number_of_variables
        self._gen_numbered_state_variables()
    
    @property
    def vars(self) -> se.Matrix:
        """returns a Matrix of the generated Symbols

        Returns
        -------
        se.Matrix
            Matrix of the generated Symbols
        """
        return se.Matrix(self._Symbols)
    
        
    def _gen_numbered_state_variables(self) -> None:
        if self._number_of_variables == 1:
            s, s_sub = self._generate_Latex_string(self._Notation, 0, 0)
            self._Symbols.append(se.Symbol(s))
            
            super()._Symbol_to_printable_dict.update({self._Symbols[0]: se.Symbol(s_sub)})
            #self._Symbols.append(se.Symbol(self._Notation))
            #super()._Symbol_to_printable_dict.update({self._Symbols[0]: se.Symbol(self._remove_unwanted_chars_for_Matlab(self._Notation))})
        else:
            for i in range(1, self._number_of_variables + 1):
                s, s_sub = self._generate_Latex_string(self._Notation, i, 0)
                self._Symbols.append(se.Symbol(s))
                
                #self._Symbols.append(se.Symbol(self._Notation + f"_{i}"))
                super()._Symbol_to_printable_dict.update({self._Symbols[i-1]: se.Symbol(s_sub)})
        
    def _repr_latex_(self) -> str:
        return self.vars._repr_latex_()
    

def StaticSymbols(names: List[str], number_of_variables: int = 1) -> List[se.Symbol]:
    """Method to generate a list of StaticSymbols

    Parameters
    ----------
    names : List[str]
        List of names for the StaticSymbols
    number_of_variables : int, optional
        Number of variables to create per name given, by default 1

    Returns
    -------
    List[se.Symbol]
        List of the generated StaticSymbols
    """
    l = []
    if number_of_variables == 1:
        for s in names:
            l.append(StaticSymbol(s,number_of_variables).vars[0])
    else:    
        for s in names:
            l.append(StaticSymbol(s,number_of_variables).var_as_vec())
    
    
    return l