from __future__ import annotations
import symengine as se
from ..Symbols import DynamicSymbol
from typing import Union



class Calculation:

    def __init__(self) -> None:
        """ An object to store a calculation and the variables used in it.
        Left side of the calculation has to be a Symbol or a Matrix of Symbols.
        """
        self._inputs: list[se.Symbol | se.Function] = []
        self._outputs: list[se.Symbol | se.Function] = []
        self._vars: list[se.Matrix] = []
        self._calcs: list[se.Matrix] = []

    def addCalculation(self, var: Union[se.Symbol, se.Function, se.Matrix], calc: Union[se.Expr, se.Matrix], is_matrix_input: bool = False):
        """ adds a calculation to the object
            var = calc.
        ----------
        var : Union[se.Symbol, se.Matrix]
            The variables used in the calculation.
        calc : Union[se.Expr, se.Matrix]
            The calculation.
        is_matrix_input : bool, optional
            used when defining a input variable which should be treadted as a Matrix, by default False
        """

        # Check data types
        if not isinstance(var, (se.Symbol, se.Function, se.Matrix)):
            raise TypeError(f"var has to be a Symbol or a Matrix of Symbols but {type(var)} was given")
        if not isinstance(calc, (se.Expr, se.Matrix)):
            raise TypeError(f"calc has to be a Symbol or a Matrix of Symbols but {type(calc)} was given")
        if isinstance(var, se.Matrix) and not isinstance(calc, se.Matrix) and not is_matrix_input:
            raise TypeError(f"var and calc have to be of the same type but {type(var)} and {type(calc)} were given")

        if isinstance(var, se.Matrix) and not is_matrix_input:
            if var.shape != calc.shape:
                raise ValueError(
                        f"var and calc have to have the same shape but {var.shape} and {calc.shape} were given")

        for i in range(len(self._calcs)):
            calc = calc.subs(self._vars[i], self._calcs[i])

        # add calculation
        self._check_and_add_outputs(var)
        self._check_and_add_Inputs(calc)

        if isinstance(var,(se.Symbol, se.Function)):
            var = se.Matrix([var])
        if isinstance(calc, se.Expr):
            calc = se.Matrix([calc])

        self._vars.append(var)
        self._calcs.append(calc)

    def _check_and_add_outputs(self, var):
        """ Checks if the outputs are already defined and if issue a warning.
        """
        if isinstance(var,( se.Symbol, se.Function)):
            if var == DynamicSymbol._derivation_variable:
                return  # do not add the derivation variable to the outputs
            elif self._outputs.__contains__(var):
                print(f"WARNING: Output {var} is already defined, variable will maybe be overwritten")
            else:
                self._outputs.append(var)
        else:
            for i in var:
                self._check_and_add_outputs(i)

    def _check_and_add_Inputs(self, calc):

        """ Checks if the inputs are already defined and if not, defines them.
        """
        if not isinstance(calc, se.Matrix):
            l1 = list(calc.atoms(se.Symbol))
            l2 = list(calc.atoms(se.AppliedUndef))

            if l2 != []:
                l1.remove(DynamicSymbol._derivation_variable)
            l = l1 + l2
            del l1, l2

            for i in l:
                if not self._inputs.__contains__(i):
                    self._inputs.append(i)
        else:
            for i in calc:
                self._check_and_add_Inputs(i)

    def subs(self, subs: dict):
        """ Substitutes the variables in the calculation.
        ----------
        subs : dict
            A dictionary with the substitutions.
        """
        for i in range(len(self._vars)):
            self._vars[i] = self._vars[i].subs(subs)
            self._calcs[i] = self._calcs[i].subs(subs)

        for i in range(len(self._inputs)):
            self._inputs[i] = self._inputs[i].subs(subs)

        for i in range(len(self._outputs)):
            self._outputs[i] = self._outputs[i].subs(subs)

    def _generate_shape_index_list(self) -> tuple[list[tuple[tuple[int, int], tuple[int, int]]], se.Matrix]:
        """
        Generates a list of tuples with the shape and the index for cse code generation.
        """
        indizes_shapes: list[tuple[tuple[int, int], tuple[int, int]]] = []
        index: int = 0
        code_vector: se.Matrix = None

        for i in range(len(self._vars)):
            indizes = (index, index + len(self._calcs[i]))
            index = indizes[1]
            shape = self._calcs[i].shape
            indizes_shapes.append((indizes, shape))

            if code_vector == None:
                code_vector = self._calcs[i].reshape(len(self._calcs[i]), 1)
            else:
                code_vector = code_vector.col_join(self._calcs[i].reshape(len(self._calcs[i]), 1))
        return indizes_shapes, code_vector

    def append_Calculation(self, calc: Calculation) -> Calculation:
        """ Appends a Calculation to the current one.
        ----------
        calc : Calculation
            The Calculation to be appended.
        """
        for i in range(len(calc._calcs)):
            if calc._vars[i].shape == (1,1):
                self.addCalculation(calc._vars[i][0], calc._calcs[i], is_matrix_input=True)
            else:
                self.addCalculation(calc._vars[i], calc._calcs[i], is_matrix_input=True)
            
        return self


    @property
    def inputs(self):
        return se.Matrix(self._inputs)

    @property
    def outputs(self):
        return se.Matrix(self._outputs)

    @property
    def vars(self):
        return self._vars

    @property
    def calcs(self):
        return self._calcs
    
    
    def __len__(self):
        l = 0
        for i in self._calcs:
            l += len(i)
        return l