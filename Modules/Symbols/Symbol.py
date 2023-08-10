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
    
    def _generate_Latex_string(self, Name:str, number:int, derivativ:int) -> tuple[str,str]:
        s = ""
        
        if Name[0] == "\\":
            re_startChracter = re.search("^\\\\[a-zA-Z]+", Name)
            if re_startChracter is not None:
                s_startChracter: str = re_startChracter.group(0)
            else:
                raise Exception("The given string is not a valid latex string")
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
            s = s_startChracter
            if number != 0:
                s_sub:str = Name + f"{number}"
            else:
                s_sub:str = Name
        elif derivativ == 1:
            s = "\dot{" +f"{s_startChracter}}}{s_rest}"
            if number != 0:
                s_sub:str = Name + f"{number}" + "dot"
            else:
                s_sub:str = Name + "dot"
        elif derivativ == 2:
            s = "\ddot{" +f"{s_startChracter}}}{s_rest}"
            if number != 0:
                s_sub:str = Name + f"{number}" + "ddot"
            else: 
                s_sub:str = Name + "ddot"
        else:
            s = s_startChracter + s_rest
            if number != 0:
                s_sub:str = Name + f"{number}" + derivativ*"d" + "ot"
            else:
                s_sub:str = Name + derivativ*"d" + "ot"
            
        
        if s_tiefgestellt == "" and number != 0:
            s += f"_{{{number}}}"
        else:
            if number != 0:
                if s_tiefgestellt != "":
                    s += "_{{" + s_tiefgestellt + "}_{" + f"{number}" + "}}" 
                else:
                    s += f"_{{{number}}}"
            else:
                if s_tiefgestellt != "":
                    s += f"_{{{s_tiefgestellt}}}"
                
        
        if s_hochgestellt != "" and derivativ > 2:
            s += f"^{{{s_hochgestellt}\ ^{{({derivativ})}}}}"
        elif derivativ > 2:
            s += f"^{{({derivativ})}}"
        else:
            if s_hochgestellt != "":
                s += f"^{{{s_hochgestellt}}}"
        return s, self._remove_unwanted_chars_for_Matlab(s_sub)
    

# def _generate_Latex_string(self, Name: str, number: int, derivativ: int) -> tuple[str, str]:
#     start_character, rest = self._parse_name(Name)
#     hochgestellt = self._parse_subscript_or_superscript(Name, "^")
#     tiefgestellt = self._parse_subscript_or_superscript(Name, "_")

#     if derivativ == 0:
#         s = start_character
#         s_sub = self._get_subscript_string(Name, number)
#     elif derivativ == 1:
#         s = f"\\dot{{{start_character}}}{rest}"
#         s_sub = self._get_subscript_string(Name, number, "dot")
#     elif derivativ == 2:
#         s = f"\\ddot{{{start_character}}}{rest}"
#         s_sub = self._get_subscript_string(Name, number, "ddot")

#     return s, s_sub

# def _parse_name(self, Name: str) -> tuple[str, str]:
#     if Name[0] == "\\":
#         s_startChracter = re.search("^\\\\[a-zA-Z]+", Name).group(0)
#         s_rest = Name.replace(s_startChracter, "")
#     else:
#         s_startChracter = Name[0]
#         s_rest = Name[1:]

#     return s_startChracter, s_rest

# def _parse_subscript_or_superscript(self, Name: str, symbol: str) -> str:
#     match = re.search(f"{symbol}[a-zA-Z1-9{{}}]+", Name)
#     if match:
#         s_rest = match.group(0)
#         s_sub = re.sub("[{}^_]", "", s_rest)
#         return s_sub
#     else:
#         return ""

# def _get_subscript_string(self, Name: str, number: int, suffix: str = "") -> str:
#     if number != 0:
#         return f"{Name}{number}{suffix}"
#     else:
#         return f"{Name}{suffix}"