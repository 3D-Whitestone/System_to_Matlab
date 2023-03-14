import symengine as se
from typing import Union, List
import sympy as sp

from warnings import warn

class DynamicSymbols:
    
    _dict_of_derivation_for_substitutions: dict = {}
    _dict_of_variable_and_symbols: dict = {}
    _derivation_variable: se.Symbol = se.Symbol("t", real = True)
    
    def __init__(self, symbols , number_of_variables : int, number_of_derivatives: int, pretty: bool = False):
        """generates a class for variables

        Args:
            symbols (str | list[str] | char): name of the symbols
            number_of_variables (int): number of variables to create. Has no effect if named variables are given
            number_of_derivatives (int): number of derivations to create
            pretty (bool, optional): spezifies if the vraiables should be pretty. Defaults to False.

        Raises:
            ValueError: _description_
            ValueError: _description_
            TypeError: _description_
        """
        
        if (number_of_derivatives < 0):
            raise ValueError("number of derivatives must be positive")
        self._number_of_derivatives = number_of_derivatives
        self._is_pretty = pretty
 
        if pretty and number_of_derivatives > 2:
            raise ValueError("pretty variables are only possible with 2 or less derivatives")
 
        if type(symbols) == str or type(symbols) == chr:
            self._number_of_variables = number_of_variables
            self._symbols: Union[None,List[str]] = None
            self._variable_char = symbols
            self._vars = self._gen_numbered_state_variables()
            self._syms = self._gen_numbered_state_symbols()
            self._is_numbered = True   
        
        elif type(symbols) == list:
            if number_of_variables != 1:
                warn("number of symbols has no effect if a list of symbol names is given")
            self._number_of_variables = len(symbols)
            self._symbols: Union[None,List[str]] = symbols
            self._variable_char = None
            self._vars = self._gen_list_of_state_variable()
            self._syms = self._gen_list_of_state_symbols()
            self._is_numbered = False
        else:
            raise TypeError("unknown Type of variables needs to be int or list of strings")
        
        if number_of_derivatives == 0:
            self._vars = self._vars[0]
            self._syms = self._syms[0]
        self._generate_and_add_diff_subs_dict()
        self._generate_and_add_syms_subs_dict()

    @property
    def vars(self) -> Union[se.MutableDenseMatrix, List[se.MutableDenseMatrix]]:
        return self._vars

    @property
    def syms(self) -> Union[se.MutableDenseMatrix, List[se.MutableDenseMatrix]]:
        return self._syms

    @property
    def is_numbered(self) -> bool:
        return self._is_numbered
    
    @property
    def variable_char(self) -> Union[str, None]:
        return self._variable_char

    @property
    def number_of_variables(self) -> int:
        return self._number_of_variables

    @property
    def is_pretty(self) -> bool:
        return self._is_pretty

    @property
    def number_of_derivatives(self) -> int:
         return self._number_of_derivatives

    @property
    def derivation_variable(self) -> se.Symbol:
         return DynamicSymbols._derivation_variable

    def var_as_vec(self) -> se.Matrix:
        if self.number_of_derivatives == 0:
            return self.vars
        vec: se.Matrix = self.vars[0]
        for i in range(self.number_of_derivatives):
            vec = vec.col_join(self.vars[i+1])
        vec = se.sympify(vec)
        if type(vec) != se.MutableDenseMatrix:
            vec = se.Matrix([vec])
        return vec
    
    def syms_as_vec(self) -> se.Matrix:
        if self.number_of_derivatives == 0:
            return self.syms
        vec: se.Matrix = self.syms[0]
        for sym in self.syms[1:]:
            vec = vec.col_join(sym)
        return se.sympify(vec)
    
    def get_variable_to_symbol_dict(self, symbol: str = None) -> dict[se.Expr, se.Expr]:
        """
    This method returns a dictionary that maps the old symbols in the self.var_as_vec() list to new symbols in the self.syms_as_vec() list or a custom symbol specified by the `symbol` parameter.

    Args:
        symbol (str, optional): The name of the custom symbol to use for the new symbols. If this parameter is not provided, the new symbols will be taken from the self.syms_as_vec() list.

    Returns:
        dict[se.Expr, se.Expr]: A dictionary that maps the old symbols to the new symbols.
    """
        old_sym = self.var_as_vec()
        if symbol is None:
            new_sym = self.syms_as_vec()
        else:
            new_sym = [se.Symbol(symbol + "(" + str(i) + ")", real = True) for i in range(1, len(old_sym) + 1)]

        old_new_dic = {old_sym[i]: new_sym[i] for i in range(len(new_sym))}
        return old_new_dic 
      
    def _gen_numbered_state_variables(self):
        """generates numbered state variables for a given variable class

        Returns
        -------
        list[se.Matrix(se.Symbols)]
            list containing the state vector and its derivatives
        """

        if self._is_pretty:
            if self.number_of_derivatives > 2:
                NameError(
                    "cannot print pretty symbols for more than 2 derivatives")
            q = []
            v = []
            dot_start = ""
            dot_end = ""

            for i in range(self.number_of_derivatives + 1):
                for ii in range(1, self.number_of_variables + 1):
                    v.append(se.Function(dot_start + self._variable_char + dot_end + f"_{ii}" , real=True)(self.derivation_variable))
                if i == 0:
                    dot_start = r"\dot{"
                    dot_end = "}"
                else:
                    dot_start = dot_start.replace("dot", "ddot")

                q.append(se.Matrix(v))
                v = []
        else:
            q = []
            v = []
            dot_end = ""

            for i in range(self.number_of_derivatives + 1):
                for ii in range(1, self.number_of_variables + 1):
                    v.append(se.Function(self._variable_char + str(ii) +
                            dot_end, real=True)(DynamicSymbols._derivation_variable))
                if i == 0:
                    dot_end = "_dot"
                else:
                    dot_end = dot_end.replace("dot", "ddot")

                q.append(se.Matrix(v))
                v = []

        return q

    def _gen_list_of_state_variable(self):
        """generates variables for the given variable class

        Returns
        -------
        list[se.Matrix(se.Symbols)]
            list containing the state vector and its derivatives
        """

        if self._is_pretty:
            if self.number_of_derivatives > 2:
                NameError(
                    "cannot print pretty symbols for more than 2 derivatives")
            q = []
            v = []
            dot_start = ""
            dot_end = ""

            for i in range(self.number_of_derivatives + 1):
                for sym in self._symbols:
                    if sym.find("_") != -1:
                        i_underline = sym.find("_")
                        v.append(se.Function(dot_start + sym[:sym.find("_")] + dot_end + sym[sym.find("_"):], real=True)(self.derivation_variable))
                    else:
                        v.append(se.Function(dot_start + sym + dot_end, real=True)(self.derivation_variable))
                if i == 0:
                    dot_start = r"\dot{"
                    dot_end = "}"
                else:
                    dot_start = dot_start.replace("dot", "ddot")

                q.append(se.Matrix(v))
                v = []
        else:
            q = []
            v = []
            dot_end = ""

            for i in range(self.number_of_derivatives + 1):
                for sym in self._symbols:
                    v.append(se.Function(sym + dot_end, real=True)(DynamicSymbols._derivation_variable))
                if i == 0:
                    dot_end = "_dot"
                else:
                    dot_end = dot_end.replace("dot", "ddot")

                q.append(se.Matrix(v))
                v = []

        return q

    def _gen_numbered_state_symbols(self):
        """generates numbered Symbols for the given variable class,
        these Symbols can NOT be differentiated

        Returns
        -------
        list[se.Matrix(se.Symbols)]
            list containing the state vector and its derivatives
        """
        
        variable_char = self._variable_char.replace('{','').replace('}','')
        q = []
        v = []
        dot_end = ""
        for i in range(self.number_of_derivatives + 1):
            for ii in range(1, self.number_of_variables + 1):
                #v.append(se.Symbol(variable_char + "(" + str(ii) + ")" + dot_end, real=True))
                v.append(se.Symbol(variable_char + str(ii) + dot_end, real=True))
            if i == 0:
                dot_end = "_dot"
            else:
                dot_end = dot_end.replace("dot", "ddot")

            q.append(se.Matrix(v))
            v = []
        return q

    def _gen_list_of_state_symbols(self):
        """generates Symbols for the given variable_class,
        these Symbols can NOT be differentiated

        Returns
        -------
        list[se.Matrix(se.Symbols)]
            list containing the state vector and its derivatives
        """

        q = []
        v = []
        dot_end = ""

        for i in range(self.number_of_derivatives + 1):
            for sym in self._symbols:
                sym_temp = sym.replace('{','').replace('}','')
                v.append(se.Symbol(sym_temp + dot_end, real=True))
            if i == 0:
                dot_end = "_dot"
            else:
                dot_end = dot_end.replace("dot", "ddot")

            q.append(se.Matrix(v))
            v = []
        return q

    def _repr_latex_(self):
        if self.number_of_derivatives == 0:
            return self.vars._repr_latex_()
        else:
            return self.var_as_vec().reshape(self.number_of_derivatives + 1,self.number_of_variables).T._repr_latex_()

    def _generate_and_add_diff_subs_dict(self):
        if self.number_of_derivatives > 0:
            for i in range(self.number_of_derivatives):
                for ii in range(self.number_of_variables):
                    DynamicSymbols._dict_of_derivation_for_substitutions.update({se.diff(self.vars[i][ii], self._derivation_variable): self.vars[i+1][ii]})

    def _generate_and_add_syms_subs_dict(self) -> None:
        DynamicSymbols._dict_of_variable_and_symbols.update(dict(zip(self.var_as_vec(), self.syms_as_vec())))
        
         
    @staticmethod
    def _diff_t(expression):
        """calculates the time derivativ of the expression an substitutes the correct symbols

        Args:
            expression (Any): expression which should be differentiated

        Returns:
            Any: differentiated expression with correct symbols
        """
        return se.diff(expression, DynamicSymbols._derivation_variable).subs(DynamicSymbols._dict_of_derivation_for_substitutions)
        
        