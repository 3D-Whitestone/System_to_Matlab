from abc import ABC, abstractmethod


class Symbols(ABC):
    _Symbol_to_printable_dict: dict = {}
    
    
    def __init__(self, Notation) -> None:
        super().__init__()
        self._Notation = Notation
        self._Symbols: list = []
        
    
    @property
    def Symbol_to_printable_dict(self) -> dict:
        return self._Symbol_to_printable_dict
    
    
    @abstractmethod
    def _repr_latex_(self) -> str:
        pass
    
    def _remove_unwanted_chars_for_Matlab(self, input:str) -> str:
        return input.replace("_", "").replace("{", "").replace("}", "").replace("\\", "")