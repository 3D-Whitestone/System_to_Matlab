from .System import System
from ..Symbols import DynamicSymbol, StaticSymbol
from ..Symbols.Symbol import Symbol
from ..FileGenerators import MFile, MFunction, SFunction

import symengine as se
import sympy as sp

from typing import Any, Union


class DynamicSystem(System):
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
        super().__init__()
        self._is_linearized = False
        if x.shape[1] != 1:
            raise ValueError("State vector has to be a column vector")
        if u.shape[1] != 1:
            raise ValueError("Input vector has to be a column vector")
        self._x = se.sympify(x)
        self._u = se.sympify(u)
        self._Equations = [None, None]
    
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
        return se.Matrix([se.diff(x, DynamicSymbol._derivation_variable).subs(DynamicSymbol._dict_of_derivation_for_substitutions) for x in self.x])
    
    @property
    def y(self) -> se.Matrix:
        """ vector of the output functions

        Returns
        -------
        se.Matrix
            vector of the output functions
        """
        l = None
        for i in self._Outputs:
            if l is None:
                l = i[1]
            else:
                l = l.col_join(i[1])
        return l
    
    def linearize(self, steady_state_state_vec: se.Matrix = None, steady_state_input_vec: se.Matrix = None) -> list[se.Matrix]:
        """ linearizes the system around a given steady state

        Parameters
        ----------
        steady_state_state_vec : se.Matrix, optional
            vector of variables which should be used in the steady state, by default None
        steady_state_input_vec : se.Matrix, optional
            vector of input variables which should be used in the strady state , by default None

        Returns
        -------
        list[se.Matrix]
            returns the linearized Matrizes [A,B,C,D]

        Raises
        ------
        ValueError
            Raised if the dimensions of the given steady state vector does not match the dimensions of the state vector 
        """
        
        
        if self._Equations[0] is None or self._Equations[1] is None:
            raise ValueError("State and output equations have to be set before linearization")
        
        if steady_state_state_vec is None:
            steady_state_state_vec = self._create_symbolic_steady_state_state_vector()
            
        if steady_state_input_vec is None:
            steady_state_input_vec = self._create_symbolic_steady_state_input_vector()
        
        if steady_state_state_vec.shape != self.x.shape or steady_state_input_vec.shape != self.u.shape:
            raise ValueError(
                "Size of steady_state hast to be equal to the size of the state vector x")

        self._A: se.Matrix = self._Equations[0].jacobian(self.x)
        self._B: se.Matrix = self._Equations[0].jacobian(self.u)
        self._C: se.Matrix = self._Equations[1].jacobian(self.x)
        self._D: se.Matrix = self._Equations[1].jacobian(self.u)

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

    def addStateEquations(self, equations: se.Matrix) -> None:
        """adding the equations for the states of the system x_dot = f(x, u)

        Args:
            equation (se.Matrix): Matrix of the expressions corresponding to the system states
        """
        if equations.shape[1] != 1:
            raise ValueError("Equations have to be a column vector")
        if equations.shape[0] != self.x.shape[0]:
            raise ValueError("Number of equations has to be equal to the number of states")
        
        # maybe add warning if equations are already set
        self._Equations[0] = equations
  
    def addInput(self, input: Any, name: str) -> None:
        """Adds an input to the system

        Args:
            input (Any): input which should be added to the system, has to be an expressions or a Matrix of expressions
        """
        self._Inputs.append(input)  
    
    def addOutput(self, output: Union[se.Expr, se.Matrix], name: str) -> None:
        """Adds an output to the system y = h(x,u)

        Args:
            output (Union[se.Expr, se.Matrix]): output which should be added to the system, has to be an expressions or a Matrix of expressions
            name (str): name of the output
        """
        output = se.sympify(output)
        
        if self._Equations[1] is None:
            if type(output) == se.Matrix:
                self._Equations[1] = output
            else:
                self._Equations[1] = se.Matrix([output])
        else:
            if type(output) == se.Matrix:
                self._Equations[1] = self._Equations[1].col_join(output)
            else:
                self._Equations[1] = self._Equations[1].col_join(se.Matrix([output]))
        
        self._Outputs.append((output, StaticSymbol(name, len(output)).vars))
        
    def write_ABCD_to_File(self, name:str, path:str = ""):
        """writes the ABCD Matrizes of the linearized system to a matlab file

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path in which the file should be saved, by default ""
        """
        File = MFile(name, path)
        File.addMathExpression(self._A, "A")
        File.addMathExpression(self._B, "B")
        File.addMathExpression(self._C, "C")
        File.addMathExpression(self._D, "D")
        File.generateFile()
        pass
    
    def write_init_File(self, name:str, path:str = ""):
        """writes an init file for the Parameters and the initial conditions of the system

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path where the file should be saved, by default ""
        """
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(str(sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict))) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([sp.octave_code(para[0].subs(Symbol._Symbol_to_printable_dict)) for para in self._Parameters]) + "]; \n \n") # type: ignore
        File.addText(r"%% Initial conditions" + "\n")
        File.addText("x_ic = " + str(sp.octave_code(self._x * 0)) + ";\n")
        File.generateFile()
    
    def write_SFunction(self, name:str, path:str = ""):
        """writes the nonlinear system as a SFunction to a matlab file

        Parameters
        ----------
        name : str
            Name of the file
        path : str, optional
            Path where the file should be stored, by default ""
        """
        File = SFunction(name, path)
        File.addState(self._x, self._Equations[0])
        File.addOutput(self._Equations[1])
        for inp in self._Inputs:
            File.addInput(inp)
        File.addParameter(self._Parameters) 
        File.generateFile()
    
    def write_MFunctions(self, name:str, path:str = ""):
        """write the nonlinear system as two MFunctions to a matlab file

        Parameters
        ----------
        name : str
            Name of the files
        path : str, optional
            Path where the files should be saved, by default ""
        """
        Fdyn = MFunction(name + "_dyn", path)
        Fdyn.addInput(self.x, "x")
        Fdyn.addInput(self.u, "u")
        Fdyn.addOutput(self.x_dot, "xdot")
        Fdyn.addEquations(self._Equations[0], self.x_dot)
        Fdyn.addParameters(self._Parameters)
        Fdyn.generateFile()
        
        Fout = MFunction(name + "_out", path)
        Fout.addInput(self.x, "x")
        Fout.addOutput(self.y, "y")
        Fout.addEquations(self._Equations[1], self.y)
        Fout.addParameters(self._Parameters)
        Fout.generateFile()
    
    def _create_symbolic_steady_state_state_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("x_{" + str(i) + "ss}") for i in range(len(self.x))])
    
    def _create_symbolic_steady_state_input_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("u_{" + str(i) + "ss}") for i in range(len(self.u))])
    
    