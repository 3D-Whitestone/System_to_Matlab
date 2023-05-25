from abc import ABC, abstractmethod
from typing import Union, Any, Tuple
from ..Symbols.Symbol import Symbol
import symengine as se
import sympy as sp

class FileGenerator(ABC):
    def __init__(self, Filename:str, Path:str = None) -> None: # type: ignore
        super().__init__()
        self._Filename = Filename
        self._Path = Path
        self._Elements = []
    @abstractmethod
    def generateFile(self) -> None:
        pass

    def _matlab_input_string_generator(self, inputs:list, name:str = "input", indents:int = 0)-> Tuple[str, str]:
        s_body:str = ""
        s_header:str = ""
        num_of_inputs:int = 0

        for i in inputs:
            if len(inputs) > 1:
                s_count = f"_{num_of_inputs}"
            else:
                s_count = ""
            
            if type(i) == list or type(i) == se.Matrix or type(i) == sp.Matrix:
                num_of_inputs += 1
                s_header += name + s_count + ", "
                
                for ii in range(len(i)):
                    s_body += str(i[ii].subs(Symbol._Symbol_to_printable_dict)) + " = " + name + s_count + f"({ii+1});\n" # type: ignore
                    
            else:
                s_header += str(i.subs(Symbol._Symbol_to_printable_dict)) + ", "

        return (s_header[:-2], s_body.replace("\n", "\n" + "\t" * indents))
            
    def _matlab_output_string_generator(self, outputs:list, name:str = "output", indents:int = 0)-> Tuple[str, str, str]:
        s_header:str = ""
        s_body_top:str = ""
        s_body_bot:str = ""
        num_of_outputs:int = 0

        for i in outputs:
            if len(outputs) > 1:
                s_count = f"_{num_of_outputs}"
            else:
                s_count = ""
            
            if type(i) == list or type(i) == se.Matrix or type(i) == sp.Matrix:
                num_of_outputs += 1
                s_header += name + s_count + ", "
                s_body_top += name + s_count + f" = zeros({len(i)},1); \n"
                
                for ii in range(len(i)):
                    s_body_bot += name + s_count + f"({ii+1})" + " = " + str(i[ii].subs(Symbol._Symbol_to_printable_dict)) + ";\n" # type: ignore

                    
            else:
                s_header += str(i.subs(Symbol._Symbol_to_printable_dict)) + ", "

        return (s_header[:-2], s_body_top.replace("\n", "\n" + "\t" * indents), s_body_bot.replace("\n", "\n" + "\t" * indents))