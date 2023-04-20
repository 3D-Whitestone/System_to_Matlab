
import os
#os.environ['USE_SYMENGINE'] = '1'
import symengine as se
from Modules.Symbols.DynamicSymbols import DynamicSymbols
from Modules.HelperFunctions.RobotikHelperFuncitons import _matlab_input_string_generator, _matlab_output_string_generator

import sympy as sp
from typing import Union, Any, List, Tuple


class Robotik_System:
    def __init__(self, f, h, x:DynamicSymbols, u:DynamicSymbols, params: list, is_linear: bool = False) -> None:
        """Generates a System of the form 
        x_dot = f(x,u)
        y     = h(x,u)
        x and u are Objects form the sys_var class

        Parameters
        ----------
        f : Any
            Sympy function of the given states and inputs
        h : Any
            Sympy function of the given states and inputs
        x : sys_var
            sys_var object containing the system states
        u : sys_var
            sys_var object containing the system inputs
        params : list
            list of the system parameters 
        is_linear : bool
            variable stating if the system is linear or not
        """        

        # Check that `x` is a sys_var object
        if not isinstance(x, DynamicSymbols):
            raise TypeError(f'Expected a sys_var object for x, got {type(x)}')
        # Check that `u` is a sys_var object
        if not isinstance(u, DynamicSymbols):
            raise TypeError(f'Expected a sys_var object for u, got {type(u)}')
        # Check that `params` is a list
        if not isinstance(params, list):
            raise TypeError(f'Expected a list for params, got {type(params)}')
        # Check that `is_linear` is a bool
        if not isinstance(is_linear, bool):
            raise TypeError(f'Expected a bool for is_linear, got {type(is_linear)}')


        self._f = f
        self._h = h
        self._x = x
        self._u = u
        self._params = params
        self._is_linear = is_linear
        
        if self._is_linear:
            self._calc_state_matrices()
            self._is_linearized = True
        else:
            self._is_linearized = False

    def _calc_state_matrices(self):
        if not self._is_linear:
            raise NameError("cannot generate state matrices from nonlinear System use linearize instead")
            
        self._A = self.f.jacobian(self.x)
        self._B = self.f.jacobian(self.u)
        self._C = self.h.jacobian(self.x)
        self._D = self.h.jacobian(self.u)

    @property
    def f(self) -> Any:
        return self._f

    @property
    def h(self) -> Any:
        return self._h

    @property
    def x(self) -> se.Matrix:
        return se.Matrix(self._x.var_as_vec()[0:-self._x.number_of_variables])

    @property
    def x_p(self) -> se.Matrix:
        return se.Matrix(self._x.var_as_vec()[self._x.number_of_variables:])

    @property
    def u(self) -> Any:
        return self._u.vars

    @property
    def params(self) -> list:
        return self._params

    @property
    def A(self) -> Union[se.Matrix, str]:
        if not self._is_linearized:
            self._calc_state_matrices()
        return self._A

    @property
    def B(self) -> Union[se.Matrix, str]:
        if not self._is_linearized:
            self._calc_state_matrices()
        return self._B

    @property
    def C(self) -> Union[se.Matrix, str]:
        if not self._is_linearized:
            self._calc_state_matrices()
        return self._C

    @property
    def D(self) -> Union[se.Matrix, str]:
        if not self._is_linearized:
            self._calc_state_matrices()
        return self._D

    def write_matlab_funs(self, filename: str, override = True):
        """write the state eqations into matlab functions,
        writes one file for the dynamic and one for the output functions

        Args:
            filename (str): Name of the output file (ans function)
            override (bool, optional): states if the file should be overwritten if it already exists. Defaults to True.
        """
        if not filename.endswith(".m"):
            filename = filename + ".m"
        if not override and os.path.exists("dyn_fun_" + filename):
            return

        par_var = self._build_sub_dict_mat_fun()
        number_of_variables = self._x.number_of_variables * self._x.number_of_derivatives


        file_s_fun = open("dyn_fun_" + filename, "w")
        file_s_fun.write(f"function state_dot = dyn_fun_" + filename.removesuffix(".m") + "(state, input_0, SC_param_0)  \n")
        file_s_fun.write(f"\t state_dot = zeros({number_of_variables},1); \n")
        file_s_fun.write(f"\t old = zeros(1,{number_of_variables}); \n")
        file_s_fun.write(f"\t old(1:{number_of_variables}) = state(1:{number_of_variables}); \n")
        file_s_fun.write(f"\t eval = zeros({number_of_variables},1); \n")


        f1, f2 = se.cse(self.f.subs(par_var))
        for temp in f1:
            file_s_fun.write("\t " + sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
         
        for i in range(1, number_of_variables + 1):
            file_s_fun.write(f"\t eval({i}) = " + sp.octave_code(f2[i-1]) + ";" + "\n")
     
        
        file_s_fun.write(
            f"\t state_dot(1:{number_of_variables}) = eval(1:{number_of_variables}); \n")
        file_s_fun.write("end")
        file_s_fun.close()


        h1, h2 = se.cse(self.h.subs(par_var))
        num_of_outputs = len(self.h)
        file_s_fun = open("out_fun_" + filename, "w")
        file_s_fun.write(f"function output = dyn_fun_" + filename.removesuffix(".m") + "(state, SC_param_0)  \n")
        file_s_fun.write("\t output = zeros(" + str(num_of_outputs) + ",1)"  + "\n")
        file_s_fun.write(f"\t old = state(1:" + str(num_of_outputs) + "); \n")
        
        for temp in h1:
            file_s_fun.write("\t " + sp.octave_code(temp[0]) + " = " + sp.octave_code(temp[1]) + "; \n")
        i = 1
        for temp in h2:
            file_s_fun.write("\t output(" + str(i) + ") = " + str(temp) + "; \n")
            i += 1
        file_s_fun.write("end")
        file_s_fun.close()

    def write_s_funs(self, filename: str, override = True):
        """writes the state equations into an matlab s function

        Args:
            filename (str): name of the file (and matlab function)
            override (bool, optional): states if the file should be overwritten if it already exists. Defaults to True.
        """
        if not filename.endswith(".m"):
            filename = filename + ".m"
        if not override and os.path.exists("s_fun_" + filename):
            return
        
        par_var = self._build_sub_dict_s_fun()
        number_of_variables = self._x.number_of_variables * self._x.number_of_derivatives
        
        s_num_of_vars = str(number_of_variables)
        s_num_of_outs = str(len(self.h))
        s_num_of_ins  = str(len(self.u))
        
        file_s_fun = open("s_fun_" + filename, "w")
        
        file_s_fun.write("function [sys,x0,str,ts] = s_fun_" + filename.removesuffix(".m") + "(t,x,u,flag,params,x1_ic)")
        file_s_fun.write("\n")
        file_s_fun.write("switch flag, \n")
        
        file_s_fun.write("\t" + r"case 0, % initialization" + "\n")
        file_s_fun.write("\t \t \t sizes = simsizes; \n")
        file_s_fun.write("\t \t \t sizes.NumContStates = " + s_num_of_vars + ";    % number of continous states \n")
        file_s_fun.write("\t \t \t sizes.NumDiscStates = 0;    % number of discrete states \n")
        file_s_fun.write("\t \t \t sizes.NumOutputs = " + s_num_of_outs + ";       % number of system outputs \n")
        file_s_fun.write("\t \t \t sizes.NumInputs = " + s_num_of_ins + ";        % number of system inputs \n")
        file_s_fun.write("\t \t \t sizes.DirFeedthrough = 0;   % direct feedtrough flag \n")
        file_s_fun.write("\t \t \t sizes.NumSampleTimes = 1;   % at least one sample time is needed \n")
        file_s_fun.write("\t \t \t sys = simsizes(sizes); \n \n")
        file_s_fun.write("\t \t \t" + r" % initial conditions" + " \n")
        file_s_fun.write("\t \t \t x0 = x1_ic; \n \n")
        file_s_fun.write("\t \t \t str = [];   % str is always an empty matrix \n \n")
        file_s_fun.write("\t \t \t ts = [0 0]; % initialize the array of sample times \n \n")
        
        file_s_fun.write("\t" + r"case 1, %derivates" + "\n")
        file_s_fun.write("\t \tsys = zeros(" + s_num_of_vars + ",1); \n")
        
        f1, f2 = se.cse(self.f.subs(par_var))
        for temp in f1:
            file_s_fun.write("\t \t" + sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
        file_s_fun.write("\n")
        for i in range(1, number_of_variables + 1):
            file_s_fun.write(f"\t \t sys({i}) = " + sp.octave_code(f2[i-1]) + ";" + "\n")
        
        
        h1, h2 = se.cse(self.h.subs(par_var))
        file_s_fun.write("\t" + r"case 3, % outputs" + "\n")
        file_s_fun.write("\t \t sys = zeros(" + s_num_of_vars + ",1); \n")
        for temp in h1:
            file_s_fun.write("\t \t" + sp.octave_code(temp[0]) + " = " + sp.octave_code(temp[1]) + "; \n")
        i = 1
        for temp in h2:
            file_s_fun.write("\t \t sys(" + str(i) + ") = " + str(temp) + "; \n")
            i += 1
        
        file_s_fun.write("\t" + r"case {2,4,9},   % unused flags" + "\n")
        file_s_fun.write("\t \t sys = []; \n")
        file_s_fun.write("\t" + " otherwise       % unexpected flags" + "\n")
        file_s_fun.write("\t \t error(['Unhandled flag = ',num2str(flag)]); \n")
        file_s_fun.write("end") 
            
    def write_init_vars(self, filename: str, override = False):
        """writes an init file for the variables (paramters) of the equations

        Args:
            filename (str): name of the file
            override (bool, optional): states if the file should be overwritten if it already exists.. Defaults to True.
        """
        if not filename.endswith(".m"):
            filename = filename + ".m"
        if override == False and os.path.exists("init_var_" + filename) == True:
            return
            
        file_vars = open("init_var_" + filename, "w")
        file_vars.write(r"%% Parameters" + "\n")
        
        
        var_dict = self._build_sub_dict_params()
        temp = ""
        for i in self.params:
            file_vars.write(str(i.subs(var_dict)) + " = 0; \n")
            temp = temp + str(i.subs(var_dict)) + " "
            
        file_vars.write("params = [" + temp + "]; \n \n" )
        
        file_vars.write(r"%% Initial conditions" + "\n")
        file_vars.write("x1_ic = zeros(" + str(len(self.x)) + ",1);")
        file_vars.close()

    def _build_sub_dict_mat_fun(self) -> dict:
        sub_dict = {}
        
        
        sub_dict.update(self._x.get_variable_to_symbol_dict("old"))
        sub_dict.update(self._u.get_variable_to_symbol_dict("input_0"))

        par = DynamicSymbols("SC_param_0",len(self.params),0,False)
        par_new = par._syms
        for i in range(len(self.params)):
            par_var_one = {self.params[i]: par_new[i]}
            sub_dict.update(par_var_one)
            
        
        return sub_dict
    
    def _build_sub_dict_s_fun(self) -> dict:
        """method to build the substitution dictionary for the s-function

        Returns
        -------
        dict
            dict including the nessecary substitutions for the s-function
        """
        sub_dict = {}
        
        sub_dict.update(self._x.get_variable_to_symbol_dict("x"))
        sub_dict.update(self._u.get_variable_to_symbol_dict("u"))

        par = DynamicSymbols("params",len(self.params),0,False)
        par_new = par._syms
        for i in range(len(self.params)):
            par_var_one = {self.params[i]: par_new[i]}
            sub_dict.update(par_var_one)
        return sub_dict
        
    def _build_sub_dict_params(self) -> dict:
        par_dic = {}
        
        for par in self.params:
            st = str(par).replace("{","").replace("}","").replace("\\","")
            par_dic.update({par : se.Symbol(st,real = True)})
        
        return par_dic 
        
    def write_ABCD_to_file(self, filename: str, override = True):
        """writes the linearized state space matrices into a matlab file

        Args:
            filename (str): name of the matlab file
            override (bool, optional): states if the file should be overwritten if it already exists.. Defaults to True.

        Raises:
            NameError: _description_
        """
        if not filename.endswith(".m"):
            filename = filename + ".m"
        if not override and os.path.exists(filename):
            return

        if not self._is_linearized:
            raise NameError("System must be linearized before the Matrices can be saved")
        
        var_dic = self._build_sub_dict_params()
        
        with open(filename, "w") as file:
            f1, f2 = se.cse(self.A.subs(var_dic))
            for temp in f1:
                file.write(sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
            file.write("\n")
            file.write("A=" + sp.octave_code(se.Matrix(f2).reshape(self.x.shape[0] ,self.x.shape[0])) + ";\n")
            if len(f1) != 0:
                file.write("clear")
                for x in f1:
                    file.write(" " + str(x[0]))
                file.write("\n\n")
            
            f1, f2 = se.cse(self.B.subs(var_dic))
            for temp in f1:
                file.write(sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
            file.write("\n")
            file.write("B=" + sp.octave_code(se.Matrix(f2).reshape(self.x.shape[0] ,self.u.shape[0])) + ";\n")
            if len(f1) != 0:
                file.write("clear")
                for x in f1:
                    file.write(" " + str(x[0]))
                file.write("\n\n")
            
            f1, f2 = se.cse(self.C.subs(var_dic))
            for temp in f1:
                file.write(sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
            file.write("\n")
            file.write("C=" + sp.octave_code(se.Matrix(f2).reshape(self.h.shape[0] ,self.x.shape[0])) + ";\n")
            if len(f1) != 0:
                file.write("clear")
                for x in f1:
                    file.write(" " + str(x[0]))
                file.write("\n\n")
            
            f1, f2 = se.cse(self.D.subs(var_dic))
            for temp in f1:
                file.write(sp.octave_code(temp[0]) + "=" + sp.octave_code(temp[1]) + ";" + "\n")
            file.write("\n")
            file.write("D=" + sp.octave_code(se.Matrix(f2).reshape(self.h.shape[0] ,self.u.shape[0])) + ";\n")
            if len(f1) != 0:
                file.write("clear")
                for x in f1:
                    file.write(" " + str(x[0]))
                file.write("\n\n")
        
    def linearize(self, steady_state_state_vec: se.Matrix, steady_state_input_vec: se.Matrix, simplify = False, force = False) -> list:
        """linearizes the equations around the given steady state

        Args:
            steady_state_state_vec (se.Matrix): steady state vector fot the state variables
            steady_state_input_vec (se.Matrix): steady state vector for the input variables
            simplify (bool, optional): states if the matrices should be simplified, use with caution simplification of big matrices takes a very long time. Defaults to False.
            force (bool, optional): true to recalculate the ABCD Matrices (should not be necessary)

        Raises:
            ValueError: is thrown if the size of the steady state vector doesn't match the size of the actual vector

        Returns:
            list: list of the linear matrices ([A,B,C,D])
        """
        if self._is_linearized and not force:
            print("System has already been linearized, stored matrices are returned")
            return[self._A, self._B, self._C, self._D]
        
        if steady_state_state_vec.shape != self.x.shape or steady_state_input_vec.shape != self.u.shape:
            raise ValueError(
                "Size of steady_state hast to be equal to the size of the state vector x")

        self._A = self.f.jacobian(self.x)
        self._B = self.f.jacobian(self.u)
        self._C = self.h.jacobian(self.x)
        self._D = self.h.jacobian(self.u)

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
        if simplify:
            self._A = se.sympify(sp.simplify(self._A))
            self._B = se.sympify(sp.simplify(self._B))
            self._C = se.sympify(sp.simplify(self._C))
            self._D = se.sympify(sp.simplify(self._D))
        
        return [self._A, self._B, self._C, self._D]

    

def write_m_func(filename: str, eqs: tuple, inputs: list, outputs: list, path = ""):
    """writes an eqation or a list of eqations in a matlab function

    Parameters
    ----------
    filename : str
        name of the file and matlab function
    eqs : tuple
        tuple containing two Matrices, first the left side of the equations and second the right side of the equatio 
    inputs : list
        list of Symbols which should be interpreted as inputs
    path : str, optional
        path if the file should be in another directory, do not add the filename here, by default ""
    """
    
    if not filename.endswith(".m"):
        filename += ".m"
        
    if type(eqs) != tuple:
        raise TypeError("eqs must be a tuple")

    # for i in range(len(eqs[0])):
    #     lhs = sp.octave_code(eqs[0][i].subs(DynamicSymbols._dict_of_variable_and_symbols))

        # if "{" in str_sym  or "}" in str_sym or "\\" in str_sym:
        #     raise NameError("variable Names cannot contain { or } or \\")


    # if type(inputs) != list:
    #     if type(inputs) != sp.Symbol and type(inputs) != se.Symbol and  inputs is not None:
    #         raise TypeError("inputs must be list of sympy.Symbols or symengine.Symbols, a sympy.Symbol, or symengine.Symbol or None")
    # else:
    #     for i in inputs:
    #         if type(i) != sp.Symbol and type(i) != se.Symbol:
    #             raise TypeError("inpust must be a list of sympy.Symbols or symengine.Symbols")

    
    (sin, s_define) = _matlab_input_string_generator(inputs)
    (sheader, sbody_top, sbody_bot) = _matlab_output_string_generator(outputs)

    mfile = open(path + filename,"w")
    
    # sout = sp.octave_code(eqs[0][0])
    # for i in range(1,len(eqs)):
    #     sout += ", " + sp.octave_code(eqs[i][0].subs(DynamicSymbols._dict_of_variable_and_symbols))
    
    # sin = sp.octave_code(inputs[0])
    # for i in range(1,len(inputs)):
    #     sin += ", " + sp.octave_code(inputs[i].subs(DynamicSymbols._dict_of_variable_and_symbols))
    
    
    mfile.write("function [" + sheader + "] = " + filename.removesuffix(".m") + "(" + sin +") \n")
    mfile.write(s_define)
    mfile.write(sbody_top)
    
    f1, f2 = se.cse(eqs[1].subs(DynamicSymbols._dict_of_variable_and_symbols))
    f2 = f2[0]
    for eq in f1:
        mfile.write(str(eq[0]) + " = " +sp.octave_code(eq[1]) + ";\n")
    
    for i in range(len(eqs[0])):
        mfile.write(sp.octave_code(eqs[0][i].subs(DynamicSymbols._dict_of_variable_and_symbols)) + " = " + sp.octave_code(f2[i]) + "; \n")
        
    mfile.write(sbody_bot)
    mfile.write("end")
    mfile.close()
       
       
def write_init_prams(params: DynamicSymbols, filename: str, override = True):
    """writes an init file for the variables (paramters) of the equations

    Args:
        filename (str): name of the file
        override (bool, optional): states if the file should be overwritten if it already exists.. Defaults to True.
    """
    if not filename.endswith(".m"):
        filename = filename + ".m"
    if override == False and os.path.exists("init_var_" + filename) == True:
        return
        
    file_vars = open("init_var_" + filename, "w")
    file_vars.write(r"%% Parameters" + "\n")
    
    
    #var_dict = params._build_sub_dict_params()
    temp = ""
    for i in params._syms:
        file_vars.write( sp.octave_code(i.subs(DynamicSymbols._dict_of_variable_and_symbols)) + " = 0; \n")
        
        temp = temp + sp.octave_code(i.subs(DynamicSymbols._dict_of_variable_and_symbols)) + " "
        
    file_vars.write("params = [" + temp + "]; \n \n" )
       
def diff_t(expression):
    return DynamicSymbols._diff_t(expression)