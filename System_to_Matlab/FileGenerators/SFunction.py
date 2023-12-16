from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement

import os
import symengine as se

from typing import Any, Union

class SFunction(FileGenerator):
    def __init__(self, Filename: str, Path: str = "") -> None:
        """ Generates an instance of the SFunction class.

        Parameters
        ----------
        Filename : str
            The name of the file to be generated. If the file does not end with .m, it will be added.
        Path : str, optional
            Path in which the file should me saved if non is given the current path is used , by default ""
        """
        if not Filename.endswith(".m"):
            Filename += ".m"
        super().__init__(Filename, Path)
        
        self._StateEquations = []
        self._States = []
        self._Outputs = []
        self._Inputs = []
        self._Parameters = []

    def addState(self, state: Union[se.Matrix, list],  equation: Union[se.Matrix, list]) -> None:
        """Adding the state to the SFunction

        Parameters
        ----------
        state : se.Matrix or list
            State of a system, can be a list of states or a matrix of states.
        equation : se.Matrix or list
            equations to calculate the derivative of the state, can be a list of equations or a matrix of equations

        Raises
        ------
        ValueError
            Raised if the number o states and equations does not match or if the states and equations are not column vectors.
        """
        if type(state) != se.Matrix:
            state == se.Matrix(state)
        if type(equation) != se.Matrix:
            equation = se.Matrix(equation)
        if state.shape[0] != equation.shape[0]:
            raise ValueError("The number of states and equations does not match")   
        if state.shape[1] != 1 or equation.shape[1] != 1:
            raise ValueError("The states and equations have to be column vectors")
        for eq in equation:
            self._StateEquations.append(eq)
        for st in state:
            self._States.append(st)

    def addOutput(self, equation) -> None:
        """Adding the output to the SFunction

        Parameters
        ----------
        equation : _type_
            equations to calculate the output, can be a list of equations or a matrix of equations
        """
        if isinstance(equation, list):
            for eq in equation:
                self._Outputs.append(eq)
        elif isinstance(equation, se.Matrix) and equation.shape[1] == 1:
            for eq in equation:
                self._Outputs.append(eq)
        else:
            self._Outputs.append(equation)
    
    def addInput(self, input) -> None:
        """Adding the input to the SFunction

        Parameters
        ----------
        input : _type_
            input of the system, can be a list of inputs or a matrix of inputs
        """
        if isinstance(input, list):
            for inp in input:
                self._Inputs.append(inp)
        elif isinstance(input, se.Matrix) and input.shape[1] == 1:
            for inp in input:
                self._Inputs.append(inp)
        else:
            self._Inputs.append(input)
     
    def addParameter(self, parameter) -> None:
        """Adding the parameter to the SFunction. All values which are constants in Matlab should be defined as parameters. (They will be defined in the ini file)

        Parameters
        ----------
        parameter : _type_
            parameter of the system, can be a list of parameters or a matrix of parameters
        """
        if type(parameter) == list:
            for para in parameter:
                self._Parameters.append(para)
        elif type(parameter) == se.Matrix and parameter.shape[1] == 1:
            for para in parameter:
                self._Parameters.append(para)
        else:
            self._Parameters.append(parameter)
    
    def _Parameter_Input_String(self) -> str:
        """PRIVATE Generates the string for the parameters and inputs of the SFunction

        Returns
        -------
        str
            String for the parameters and inputs of the SFunction
        """
        s = list(se.Matrix(self._Parameters)[:,0])
        s = self._matlab_input_string_generator([s],"params", 2)[1]
        s += self._matlab_input_string_generator(self._Inputs,"u", 2)[1]
        return s
    
    def generateFile(self, overwrite = True) -> None:
        """Generates the file with the given name and path. If the file already exists, it will be overwritten. (If you don't want to overwrite the file, set overwrite to False)

        Parameters
        ----------
        overwrite : bool, optional
            Defines if the file should be overwritten, by default True
        """
        
        if not overwrite and os.path.exists(self._Path + "\\" + self._Filename):
            return
        i = 0
        
        for state in self._States:
            i += 1
            for ii in range(len(self._StateEquations)):
                self._StateEquations[ii] = self._StateEquations[ii].subs(state, se.Symbol(f"x({i})"))
            for ii in range(len(self._Outputs)):
                self._Outputs[ii] = self._Outputs[ii].subs(state, se.Symbol(f"x({i})"))
        i = 0    
        for inp in self._Inputs:
            i+=1
            for ii in range(len(self._StateEquations)):
                self._StateEquations[ii] = self._StateEquations[ii].subs(inp, se.Symbol(f"u({i})"))
            for ii in range(len(self._Outputs)):
                self._Outputs[ii] = self._Outputs[ii].subs(inp, se.Symbol(f"u({i})"))
        
        s_para_input = self._Parameter_Input_String()
        self._Elements.append(StringElement(f"function [sys,x0,str,ts] = {self._Filename[:-2]}(t,x,u,flag,params,x_ic) \n "))
        self._Elements.append(StringElement("switch flag, \n"))
        self._Elements.append(StringElement("\t" + r"case 0, % initialization" + " \n"))
        self._Elements.append(StringElement("\t \t" + "sizes = simsizes; \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumContStates = {len(self._StateEquations)}; \t"  + r"% number of continous states" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumDiscStates = 0; \t"  + r"% number of discrete states" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumOutputs = {len(self._Outputs)}; \t"  + r"% number of system outputs" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumInputs = {len(self._Inputs)}; \t"  + r"% number of system inputs" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.DirFeedthrough = 0; \t"  + r"% direct feedtrough flag" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumSampleTimes = 1; \t"  + r"% at least one sample time is needed" + " \n"))
        self._Elements.append(StringElement("\t \t" + "sys = simsizes(sizes); \n \n"))
        self._Elements.append(StringElement("\t \t" + r"% initial conditions"+ " \n" ))
        self._Elements.append(StringElement("\t \t" + "x0 = x_ic; \n \n"))
        self._Elements.append(StringElement("\t \t" + "str = []; "  + r"% str is always an empty matrix" + "\n \n"))
        self._Elements.append(StringElement("\t \t" + "ts = [0 0];"  + r"% initialize the array of sample times" + " \n \n"))

        self._Elements.append(StringElement("\t" + r"case 1, % derivative" + " \n"))
        self._Elements.append(StringElement("\t \t" + s_para_input +"\n"))
        self._Elements.append(StringElement("\t \t" + f"sys = zeros({len(self._StateEquations)},1); \n"))
        
        self._Elements.append(CodeElement(self._StateEquations, "sys",2, True, False))
        
        self._Elements.append(StringElement("\t" + r"case 3, % output" + " \n"))
        self._Elements.append(StringElement("\t \t" + s_para_input +"\n"))
        self._Elements.append(StringElement("\t \t" + f"sys = zeros({len(self._Outputs)},1); \n"))  
        self._Elements.append(CodeElement(self._Outputs, "sys",2, True, False))
        
        self._Elements.append(StringElement("\t" + r"case {2,4,9}, % unused flags" + " \n"))
        self._Elements.append(StringElement("\t \t" + "sys = []; \n"))
        
        self._Elements.append(StringElement("\t" + r"otherwise % unused flags" + " \n"))
        self._Elements.append(StringElement("\t \t" + "error(['Unhandled flag = ',num2str(flag)]); \n"))
        self._Elements.append(StringElement("end"))

        if self._Path is None or self._Path == "":
            path = self._Filename
        else:
            if self._Path.endswith("\\"):
                path = self._Path + self._Filename
            else:
                path = self._Path + "\\" + self._Filename
        with open(path, "w") as f:
            for element in self._Elements:
                f.write(element.generateCode())