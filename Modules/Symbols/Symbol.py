from abc import ABC, abstractmethod
import symengine as se

class Symbol(ABC):
    _Symbol_to_printable_dict: dict = {}
    
    
    def __init__(self, Notation) -> None:
        super().__init__()
        self._Notation = Notation
        self._Symbols: list = []
        
    
    @property
    def Symbol_to_printable_dict(self) -> dict:
        return self._Symbol_to_printable_dict
    
    def var_as_vec(self) -> se.Matrix:
        """creates a vector of the state variables

        Returns
        -------
        se.Matrix
            vector of the state variables
        """
        return se.Matrix(self._Symbols)
    
    @abstractmethod
    def _repr_latex_(self) -> str:
        pass
    
    def _remove_unwanted_chars_for_Matlab(self, input:str) -> str:
        return input.replace("_", "").replace("{", "").replace("}", "").replace("\\", "")