from .System import System
from ..Symbols import DynamicSymbol
from ..FileGenerators import MFile, MFunction, SFunction

import symengine as se
import sympy as sp

from typing import Any, Union


class DynamicSystem(System):
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
        
        self._number_of_outputs = 0
        self._number_of_inputs = 0
    
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
        return self._x
    
    @property
    def u(self) -> se.Matrix:
        return self._u
    
    @property
    def x_dot(self) -> se.Matrix:
        return se.Matrix([se.diff(x, DynamicSymbol._derivation_variable).subs(DynamicSymbol._dict_of_derivation_for_substitutions) for x in self.x])
    
    
    def linearize(self, steady_state_state_vec: se.Matrix = None, steady_state_input_vec: se.Matrix = None) -> list:
        
        
        if self._Equations[0] is None or self._Equations[1] is None:
            raise ValueError("State and output equations have to be set before linearization")
        
        if steady_state_state_vec is None:
            steady_state_input_vec = self._create_symbolic_steady_state_state_vector()
            
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
  
    def addInput(self, input: Any, name:str) -> None:
        """Adds an input to the system

        Args:
            input (Any): input which should be added to the system, has to be an expressions or a Matrix of expressions
            name (str): name of the input
        """
        self._number_of_inputs += 1
        self._Inputs.append(input)
    
    def addOutput(self, output: Any, name:str) -> None:
        output = se.sympify(output)
        self._number_of_outputs += 1
        """Adds an output to the system y = h(x,u)

        Args:
            output (Any): output which should be added to the system, has to be an expressions or a Matrix of expressions
            name (str): name of the output
        """
        if self._Equations[1] is None:
            if type(output) == se.Matrix:
                self._Equations[1] = output
            else:
                self._Equations[1] = se.Matrix([output])
        else:
            if type(output) == se.Matrix:
                self._Equations[1].col_join(output)
            else:
                self._Equations[1].col_join(se.Matrix([output]))
            
        self._Outputs.append((output, name))
        
    def write_ABCD_to_File(self, name:str, path:str = ""):
        File = MFile(name, path)
        File.addMathExpression(self._A, "A")
        File.addMathExpression(self._B, "B")
        File.addMathExpression(self._C, "C")
        File.addMathExpression(self._D, "D")
        File.generateFile()
        pass
    
    def write_init_File(self, name:str, path:str = ""):
        File = MFile(name, path)
        File.addText(r"%% System parameters")
        File.addText("\n")
        for para in self._Parameters:
            File.addText(sp.octave_code(para[0].subs(DynamicSymbol._Symbol_to_printable_dict)) + " = " + str(para[1]) + ";\n")
            
            
        File.addText(r"params = [" + ", ".join([sp.octave_code(para[0].subs(DynamicSymbol._Symbol_to_printable_dict)) for para in self._Parameters]) + "]; \n \n")
        File.addText(r"%% Initial conditions" + "\n")
        File.addText("x_ic = "+ sp.octave_code(self._x * 0) + ";\n")
        File.generateFile()
    
    def write_SFunction(self, name:str, path:str = ""):
        File = SFunction(name, path)
        File.addState(self._x, self._Equations[0])
        File.addOutput(self._Equations[1])
        for inp in self._Inputs:
            File.addInput(inp)
        File.addParameter(self._Parameters) 
        File.generateFile()
    
    def _create_symbolic_steady_state_state_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("x_{" + str(i) + "ss}") for i in range(len(self.x))])
    
    def _create_symbolic_steady_state_input_vector(self) -> se.Matrix:
        return se.Matrix([se.Symbol("u_{" + str(i) + "ss}") for i in range(len(self.u))])
    
    