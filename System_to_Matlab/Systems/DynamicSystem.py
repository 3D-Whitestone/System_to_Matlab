#from .System import System
from ..Symbols import DynamicSymbol, StaticSymbol
from ..Symbols.Symbol import Symbol
from ..FileGenerators import MFile, MFunction, SFunction
from ..Calculation.Calculation import Calculation

import symengine as se
import sympy as sp

from typing import Any, Union

class DynamicSystem():
    """Generates a class for a dynamic system with the following structure:

        Args:
            x (se.Matrix): Vector of the state variables
            u (se.Matrix): Vector of the input variables

        Raises:
            ValueError: state vector is no column vector
            ValueError: input vector is no column vector
    """
    def __init__(self, x: se.Matrix, u: se.Matrix) -> None:
        """Generates a class for a dynamic system with the following structure:

        Args:
            x (se.Matrix): Vector of the state variables
            u (se.Matrix): Vector of the input variables

        Raises:
            ValueError: state vector is no column vector
            ValueError: input vector is no column vector
        """
        self._is_linearized = False
        if x.shape[1] != 1:
            raise ValueError("State vector has to be a column vector")
        if u.shape[1] != 1:
            raise ValueError("Input vector has to be a column vector")
        self._x = se.sympify(x)
        self._u = se.sympify(u)
        self._State_Equations: Calculation = Calculation()
        # self._Calcs: Calculation = Calculation()
        self._Outputs: list[se.Symbols | se.Function] = []
        self._Outputs_Calcs: Calculation = Calculation()
        self._Inputs: list[se.Symbols | se.Function] = [se.Symbol("u")]
        # self._Input_Calcs: Calculation = Calculation()

        # self._Input_Calcs.addCalculation(self._u, se.Symbol('u'),is_matrix_input=True)
        
        self._Parameters: list[tuple[se.Symbol | se.Function, float]] = []
    
    @property
    def A(self) -> se.Matrix:
        if self._is_linearized:
            return self._A
        else:
            raise ValueError("System has to be linearized before accessing the A matrix")
    
    @property
    def B(self) -> se.Matrix:
        if self._is_linearized:
            return self._B
        else:
            raise ValueError("System has to be linearized before accessing the B matrix")
        
    @property
    def C(self) -> se.Matrix:
        if self._is_linearized:
            return self._C
        else:
            raise ValueError("System has to be linearized before accessing the C matrix")
        
    @property
    def D(self) -> se.Matrix:
        if self._is_linearized:
            return self._D
        else:
            raise ValueError("System has to be linearized before accessing the D matrix")
    
    @property
    def x(self) -> se.Matrix:
        """ vector of the state variables

        Returns
        -------
        se.Matrix
            vector of the state variables
        """
        return self._x
    
    @property
    def u(self) -> se.Matrix:
        """vector of the input variables

        Returns
        -------
        se.Matrix
            vector of the input variables
        """
        return self._u
    
    @property
    def x_dot(self) -> se.Matrix:
        """vector of the derivatives of the state variables

        Returns
        -------
        se.Matrix
            vector of the derivatives of the state variables
        """
        return se.Matrix([se.diff(x, DynamicSymbol._derivation_variable).subs(DynamicSymbol._dict_of_derivation_for_substitutions) for x in self.x])
    
    @property
    def y(self) -> se.Matrix:
        """ vector of the output functions

        Returns
        -------
        se.Matrix
            vector of the output functions
        """
        _ , vec = self._Outputs_Calcs._generate_shape_index_list()
        return vec
    
    def linearize(self, steady_state_state_vec: se.Matrix = None, steady_state_input_vec: se.Matrix = None) -> list[se.Matrix]:
        """ linearizes the system around a given steady state

        Parameters
        ----------
        steady_state_state_vec : se.Matrix, optional
            vector of variables which should be used in the steady state, by default None
            Can be omitted if the steady state is 0
        steady_state_input_vec : se.Matrix, optional
            vector of input variables which should be used in the strady state , by default None
            Can be omitted if the steady state is 0

        Returns
        -------
        list[se.Matrix]
            returns the linearized Matrizes [A,B,C,D]

        Raises
        ------
        ValueError
            Raised if the dimensions of the given steady state vector does not match the dimensions of the state vector 
        """
        
        
        if len(self._State_Equations.calcs) == 0 or len(self._Outputs_Calcs.calcs) == 0:
            raise ValueError("State and output equations have to be set before linearization")
        
        if steady_state_state_vec is None:
            steady_state_state_vec = self._create_symbolic_steady_state_state_vector()
            
        if steady_state_input_vec is None:
            steady_state_input_vec = self._create_symbolic_steady_state_input_vector()
        
        if steady_state_state_vec.shape != self.x.shape or steady_state_input_vec.shape != self.u.shape:
            raise ValueError(
                "Size of steady_state hast to be equal to the size of the state vector x")

        self._A: se.Matrix = self._State_Equations._generate_shape_index_list()[1].jacobian(self.x)
        self._B: se.Matrix = self._State_Equations._generate_shape_index_list()[1].jacobian(self.u)
        self._C: se.Matrix = self._Outputs_Calcs._generate_shape_index_list()[1].jacobian(self.x)
        self._D: se.Matrix = self._Outputs_Calcs._generate_shape_index_list()[1].jacobian(self.u)

        for i in range(len(self.x)):
            self._A = self._A.subs(self.x[i], steady_state_state_vec[i])
            self._B = self._B.subs(self.x[i], steady_state_state_vec[i])
            self._C = self._C.subs(self.x[i], steady_state_state_vec[i])
            self._D = self._D.subs(self.x[i], steady_state_state_vec[i])
        
        for i in range(len(self.u)):
            self._A = self._A.subs(self.u[i], steady_state_input_vec[i])
            self._B = self._B.subs(self.u[i], steady_state_input_vec[i])
            self._C = self._C.subs(self.u[i], steady_state_input_vec[i])
            self._D = self._D.subs(self.u[i], steady_state_input_vec[i])

        self._is_linearized = True

        
        return [self._A, self._B, self._C, self._D]

    def addStateEquations(self, equations: se.Matrix , add_as_Output = True) -> None:
        """adding the equations for the states of the system x_dot = f(x, u)

        Args:
            equation (se.Matrix): Matrix of the expressions corresponding to the system states
            add_as_Output (bool, optional): If true the equations will be added as outputs. Defaults to True.
        """
        if isinstance(equations, se.Matrix):
            if equations.shape[1] != 1:
                raise ValueError("Equations have to be a column vector")
            if equations.shape[0] != self.x.shape[0]:
                raise ValueError("Number of equations has to be equal to the number of states")
        else:
            raise TypeError("Equations have to be a Matrix")
        
        if len(self._State_Equations.calcs) != 0:
            raise ValueError("State equations are already set")
        self._State_Equations.addCalculation(self.x_dot, equations)
        self._number_of_states = equations.shape[0]
        
        if add_as_Output:
            for state in self.x:
                self.addOutput(state)
  
    # def addInput(self, input: se.Symbol | se.Function | se.Matrix, name: str | se.Symbol = "") -> None:
    #     """Adds an aditional input to the System.
    #     Not needed normally, standard inputs should be given when initializing the System.
    #     (Inputs which do not change should be included via the parameters)
    #     When a name is given the given Symbol/Matrix will be outputed with the given name.
    #     Names are not used in the S-Function 
    #         --(order of the input vector must be the same as here)
    #         --(if you input multiple inputs the order is also the same)
    #     ----------
    #     input : se.Symbol | se.Function | se.Matrix
    #         The input to be added.
    #     name : str, optional
    #         The name of the input. If non is given the name of the Symbol itself is used. Defaults to "".
    #     """
        
    #     if isinstance(input, se.Matrix):
    #         if name == "":
    #             raise ValueError("Matrix inputs have to have a name")
    #         is_input_matrix = True
    #     else:
    #         is_input_matrix = False
        
    #     if name == "":
    #         self._Inputs.append(input)
    #     else:
    #         self._Inputs.append(se.Symbol(name))
    #         self._Input_Calcs.addCalculation(input, se.Symbol(name),is_matrix_input=is_input_matrix)
        
    
    def addCalculation(self, name: Union[str, se.Symbol, list[str], Calculation], rhs: se.Expr = None) -> None:
        """Adding an Calculation to the System. Should be used if you want to add some Output equations in the form y = f(x) 
        Has to have the form name = rhs.
            name hast to be a Symbol or a string which can be converted to a Symbol
        Parameters
        ----------
        name : Union[str, se.Symbol, list[str]]
            Can be an Calculation object or,
            the name of the variable calculated in the equation. Must be a Symbol or a string that can be converted to a Symbol. 
        rhs : se.Expr, optional
            The calculation to be added to the system. Defaults to None.
        """

        if isinstance(name, Calculation):
            self._Outputs_Calcs.append_Calculation(name)
        else:
            calc = Calculation()
            calc.addCalculation(name, rhs)
            self._Outputs_Calcs.addCalculation(name, rhs)

    def addOutput(self, output: se.Symbol | se.Function, name: str = "") -> None:
        """Adds an output to the System.
        When a name is given the given Symbol will be outputed with the given name (only when using M-Functions, an S-function has only one combined output).
        ----------
        output : se.Symbol | se.Function
            The output to be added.
        name : str, optional
            The name of the output. Defaults to "".
        """
        if not isinstance(output, (se.Symbol, se.Function)):
            raise TypeError("Output has to be a Symbol or a Function")
        if name == "":
            self._Outputs.append(output)
            self._Outputs_Calcs.addCalculation(output, output)
        else:
            self._Outputs.append(se.Symbol(name))
            self._Outputs_Calcs.addCalculation(se.Symbol(name), output)
    
    def addParameter(self, parameter: Any, values:list|int = 0) -> None:
        """adds a parameter to the System. If values are provided then the init file will include them if not they will be set to 0.

        Args:
            parameter (Any): parameter which should be added to the system, has to be a symbol or a Matrix of symbols
            
            values (Union[None, Any], optional): values for the parameter. Either a list or a column Matrix.
            Defaults to None.
        """
        parameter = list(parameter)
        if values == 0:
            values = list(0 for i in range(len(parameter)))
        if len(parameter) != len(values):
            raise ValueError("Number of parameters and values does not match")
        
        self._Parameters.extend(list(zip(parameter, values)))
    
    def write_ABCD_to_File(self, name:str, path:str = "", overwrite:bool = True):
        """writes the ABCD Matrizes of the linearized system to a matlab file

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path in which the file should be saved, by default ""
        overwrite : bool, optional
            If true, the file will be overwritten if it already exists, by default True
        """
        File = MFile(name, path)
        ABCD_calc = Calculation()
        ABCD_calc.addCalculation(se.Symbol("A"), self._A)
        ABCD_calc.addCalculation(se.Symbol("B"), self._B)
        ABCD_calc.addCalculation(se.Symbol("C"), self._C)
        ABCD_calc.addCalculation(se.Symbol("D"), self._D)
        File.addCalculation(ABCD_calc)
        File.generateFile(overwrite)
    
    def write_init_File(self, name:str, path:str = "", overwrite:bool = True):
        """writes an init file for the Parameters and the initial conditions of the system

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path where the file should be saved, by default ""
        overwrite : bool, optional
            If true, the file will be overwritten if it already exists, by default True
        """
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict)) for para in self._Parameters]) + "]; \n \n") # type: ignore
        File.addText(r"%% Initial conditions" + "\n")
        File.addText("x_ic = " + str(sp.octave_code(self._x * 0)) + ";\n")
        File.generateFile(overwrite)
    
    def write_SFunction(self, name:str, path:str = "", overwrite:bool = True):
        """writes the nonlinear system as a SFunction to a matlab file

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path where the file should be stored, by default ""
        overwrite : bool, optional
            If true, the file will be overwritten if it already exists, by default True
        """
        File = SFunction(name, path)
        File.addState(self._x, self._State_Equations)
        File.addOutput_equations(self._Outputs_Calcs)
        for o in self._Outputs:
            File.addOutput(o)
        
        #for i in self._Input_Calcs.outputs:
        #    File.addInput(i)
        File.addInput(self._u, se.Symbol('u'))
            
        File.addParameter(self._Parameters) 
        File.generateFile(overwrite)
    
    def write_MFunctions(self, name:str, path:str = "", overwrite:bool = True):
        """write the nonlinear system as two MFunctions to a matlab file

        Parameters
        ----------
        name : str
            Name of the files
        path : str, optional
            Path where the files should be saved, by default ""
        overwrite : bool, optional
            If true, the files will be overwritten if they already exist, by default True
        """
        Fdyn = MFunction(name + "_dyn", path)
        
        Fdyn.addInput(self.x, "x")
        Fdyn.addInput(self.u, "u")
        # pars = []
        # for i in self._Parameters:
        #     pars.append(i[0])
        Fdyn.addInput(se.Matrix([i[0] for i in self._Parameters ]), "params")
        #Fdyn.addOutput(self.x_dot, "xdot")
        temp = Calculation()
        temp.addCalculation(se.Symbol("xdot"),self._State_Equations.calcs[0] )
        Fdyn.addCalculation(Calculation.append_Calculations([temp]))
        Fdyn.addOutput(se.Symbol("xdot"))
        
        Fdyn.generateFile(overwrite)
        
        Fout = MFunction(name + "_out", path)
        Fout.addInput(self.x, "x")
        Fout.addInput(se.Matrix([i[0] for i in self._Parameters ]), "params")
        Fout.addOutput(self.y, "y")
        Fout.addCalculation(Calculation.append_Calculations([self._Outputs_Calcs]))
        Fout.generateFile(overwrite)
    
    def _create_symbolic_steady_state_state_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("x_{" + str(i) + "ss}") for i in range(len(self.x))])
    
    def _create_symbolic_steady_state_input_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("u_{" + str(i) + "ss}") for i in range(len(self.u))])
    
    