from abc import ABC, abstractmethod
import symengine as se
import re
from typing import Union

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
        return input.replace("_", "").replace("{", "").replace("}", "").replace("\\", "").replace("^", "")
    
    def _generate_Latex_string(self, Name:str, number:int, derivativ:int) -> str:
        s = ""
        
        if Name[0] == "\\":
            s_startChracter = re.search("^\\\\[a-zA-Z]+", Name).group(0)
            s_rest = Name.replace(s_startChracter, '')
        else:
            s_startChracter:str = Name[0]
            s_rest = Name[1:]
        
        s_hochgestellt = re.search("\^[a-zA-Z1-9{}]+", Name)
        if s_hochgestellt != None:
            s_rest = s_rest.replace(s_hochgestellt.group(0), '')
            s_hochgestellt = re.sub('[{}^_]', '', s_hochgestellt.group(0))
        else:
            s_hochgestellt = ""
            
        s_tiefgestellt = re.search("_[a-zA-Z1-9{}]+", Name)
        if s_tiefgestellt != None:
            s_rest = s_rest.replace(s_tiefgestellt.group(0), '')
            s_tiefgestellt = re.sub('[{}^_]', '', s_tiefgestellt.group(0))
        else:
            s_tiefgestellt = ""
        
        if derivativ == 0:
            s:str = s_startChracter
            if number != 0:
                s_sub:str = Name + f"{number}"
            else:
                s_sub:str = Name
        if derivativ == 1:
            s:str = "\dot{" +f"{s_startChracter}}}{s_rest}"
            if number != 0:
                s_sub:str = Name + f"{number}" + "dot"
            else:
                s_sub:str = Name + "dot"
        elif derivativ == 2:
            s:str = "\ddot{" +f"{s_startChracter}}}{s_rest}"
            if number != 0:
                s_sub:str = Name + f"{number}" + "ddot"
            else: 
                s_sub:str = Name + "ddot"
        else:
            s:str = s_startChracter + s_rest
            if number != 0:
                s_sub:str = Name + f"{number}" + derivativ*"d" + "ot"
            else:
                s_sub:str = Name + derivativ*"d" + "ot"
            
        
        if s_tiefgestellt == "" and number != 0:
            s += f"_{{{number}}}"
        else:
            if number != 0:
                s += "_{{" + s_tiefgestellt + "}_{" + f"{number}" + "}}" 
            else:
                s += f"_{{{s_tiefgestellt}}}"
                
        
        if s_hochgestellt != "" and derivativ > 2:
            s += f"^{{{s_hochgestellt}\ ^{{({derivativ})}}}}"
        elif derivativ > 2:
            s += f"^{{({derivativ})}}"
        else:
            s += f"^{{{s_hochgestellt}}}"
        return s, s_sub