from .FileGenerators import FileGenerator
from .MatlabElements import CodeElement, StringElement
from ..Calculation.Calculation import Calculation
import os
import symengine as se

from typing import Union

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
        
        self._Inputs: list[se.Symbol | se.Function] = []
        self._Input_Calcs: Calculation = Calculation()
        self._Outputs: list[se.Symbol | se.Function] = []
        self._Output_Calculations: Calculation = Calculation()

        self._StateEquations: Calculation = Calculation()
        self._States: se.Matrix = None
        self._Parameters = []
        self._number_of_inputs = 0

    def addState(self, state: se.Matrix ,  equation: Calculation) -> None:
        """Adding the state and the state equations to the SFunction
        x_punkt = f(x,u)

        Parameters
        ----------
        state : se.Matrix
            State of a system
        equation : Calculation
            Equation to calculate the state derivatives
    	"""
        # if type(state) != se.Matrix:
        #     state == se.Matrix(state)
        # if type(equation) != se.Matrix:
        #     equation = se.Matrix(equation)
        # if state.shape[0] != equation.shape[0]:
        #     raise ValueError("The number of states and equations does not match")   
        # if state.shape[1] != 1 or equation.shape[1] != 1:
        #     raise ValueError("The states and equations have to be column vectors")
        if self._States != None:
            raise ValueError("The SFunction already has states")
        
        self._StateEquations.append_Calculation(equation)
        self._States = state

    def addOutput_equations(self, calc: Calculation) -> None:
        """Adding the output equations to the SFunction

        Parameters
        ----------
        calc : Calculation
            Calculation of the outputs
        """
        self._Output_Calculations.append_Calculation(calc)
        #self._Output_Calculations._vars = [se.Matrix([se.Symbol("sys")])]

    # def addInput(self, input: se.Symbol | se.Function, expands_to = 1) -> None:
    #     """Adds an input to the function.

    #     Parameters
    #     ----------
    #     input : se.Symbol | se.Function
    #         The input to be added. (Must be a symengine object)
    #     """
    #     self._number_of_inputs += expands_to
    #     self._Inputs.append(input)

    def addInput(self, input: se.Symbol | se.Function | se.Matrix, name: str | se.Symbol = "") -> None:
        """Adds an input to the System.
        When a name is given the given Symbol/Matrix will be outputed with the given name.
        ----------
        input : se.Symbol | se.Function | se.Matrix
            The input to be added.
        name : str, optional
            The name of the input. If non is given the name of the Symbol itself is used. Defaults to "".
        """
        
        if isinstance(input, se.Matrix):
            if name == "":
                raise ValueError("Matrix inputs have to have a name")
            is_input_matrix = True
        else:
            is_input_matrix = False
        
        if name == "":
            self._Inputs.append(input)
        else:
            
            if isinstance(name, str):
                name = se.Symbol(name)
            self._Inputs.append(name)
            self._Input_Calcs.addCalculation(input, name,is_matrix_input=is_input_matrix)


    def addOutput(self, output: se.Symbol | se.Function) -> None:
        """Adds an output to the function.

        Parameters
        ----------
        output : se.Symbol | se.Function
            The output to be added. (Must be a symengine object)
        """
        self._Outputs.append(output)
     
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
        
        for i, state in enumerate(self._States):
            self._StateEquations.subs({state: se.Symbol(f"x({i+1})")})
            self._Output_Calculations.subs({state: se.Symbol(f"x({i+1})")})
            for ii, out in enumerate(self._Outputs):
                self._Outputs[ii] = out.subs({state: se.Symbol(f"x({i+1})")})

        # for i, input in enumerate(self._Inputs):
        #     self._StateEquations.subs({input: se.Symbol(f"u({i+1})")})
        #     self._Output_Calculations.subs({input: se.Symbol(f"u({i+1})")})
            
        
        s_para_input = self._Parameter_Input_String()
        self._Elements.append(StringElement(f"function [sys,x0,str,ts] = {self._Filename[:-2]}(t,x,u,flag,params,x_ic) \n "))
        self._Elements.append(StringElement("switch flag, \n"))
        self._Elements.append(StringElement("\t" + r"case 0, % initialization" + " \n"))
        self._Elements.append(StringElement("\t \t" + "sizes = simsizes; \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumContStates = {len(self._States)}; \t"  + r"% number of continous states" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumDiscStates = 0; \t"  + r"% number of discrete states" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumOutputs = {len(self._States)}; \t"  + r"% number of system outputs" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumInputs = {len(self._Input_Calcs.vars)}; \t"  + r"% number of system inputs" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.DirFeedthrough = 0; \t"  + r"% direct feedtrough flag" + " \n"))
        self._Elements.append(StringElement("\t \t" + f"sizes.NumSampleTimes = 1; \t"  + r"% at least one sample time is needed" + " \n"))
        self._Elements.append(StringElement("\t \t" + "sys = simsizes(sizes); \n \n"))
        self._Elements.append(StringElement("\t \t" + r"% initial conditions"+ " \n" ))
        self._Elements.append(StringElement("\t \t" + "x0 = x_ic; \n \n"))
        self._Elements.append(StringElement("\t \t" + "str = []; "  + r"% str is always an empty matrix" + "\n \n"))
        self._Elements.append(StringElement("\t \t" + "ts = [0 0];"  + r"% initialize the array of sample times" + " \n \n"))

        self._Elements.append(StringElement("\t" + r"case 1, % derivative" + " \n"))
        self._Elements.append(StringElement("\t \t" + s_para_input +"\n"))
        self._Elements.append(StringElement("\t \t" + f"sys = zeros({len(self._States)},1); \n"))
        
        self._Elements.append(CodeElement(self._Input_Calcs, 2, True, False))
        self._Elements.append(CodeElement(self._StateEquations, 2, True, False).override_lhs(se.Symbol("sys")))
        
        self._Elements.append(StringElement("\t" + r"case 3, % output" + " \n"))
        self._Elements.append(StringElement("\t \t" + s_para_input +"\n"))
        self._Elements.append(StringElement("\t \t" + f"sys = zeros({len(self._States)},1); \n"))
        
        self._Elements.append(CodeElement(self._Input_Calcs, 2, True, False))  
        self._Elements.append(CodeElement(self._Output_Calculations, 2, True, False))
        temp = Calculation()
        temp.addCalculation(se.Symbol("sys"), se.Matrix(self._Outputs))
        self._Elements.append(CodeElement(temp,2, True, False))
        
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