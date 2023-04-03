from Modules.Symbols.DynamicSymbols import DynamicSymbols
import symengine as se
import pytest


def test_sys_var_numbered_pretty_vars():
    var = DynamicSymbols("q",2,2,True)
    t = se.Symbol("t",real=True)
    q =    se.Matrix([se.Function("q_1",real = True)(t), se.Function("q_2",real = True)(t)])
    q_dot = se.Matrix([se.Function(r"\dot{q}_1",real = True)(t), se.Function(r"\dot{q}_2",real = True)(t)])
    q_ddot = se.Matrix([se.Function(r"\ddot{q}_1",real = True)(t), se.Function(r"\ddot{q}_2",real = True)(t)])

    assert var.vars == [q, q_dot, q_ddot]
    
def test_sys_var_numbered_pretty_syms():    
    var = DynamicSymbols("q",2,2,True)
    q =    se.Matrix([se.Symbol("q1",real = True), se.Symbol("q2",real = True)])
    q_dot = se.Matrix([se.Symbol(r"q1_dot",real = True), se.Symbol(r"q2_dot",real = True)])
    q_ddot = se.Matrix([se.Symbol(r"q1_ddot",real = True), se.Symbol(r"q2_ddot",real = True)])
    print(var._syms, q,q_dot,q_ddot)

    assert var._syms == [q, q_dot, q_ddot]

def test_sys_var_named_pretty_vars():
    var = DynamicSymbols(["M_{Mot}","F1_{ext}"],1,1,True)
    t = se.Symbol("t",real=True)
    q = se.Matrix([se.Function(r"M_{Mot}",real = True)(t), se.Function("F1_{ext}",real = True)(t)])
    q_dot = se.Matrix([se.Function(r"\dot{M}_{Mot}",real = True)(t), se.Function(r"\dot{F1}_{ext}",real = True)(t)])
    
    # Test that `var.vars` is a list of two elements
    assert len(var.vars) == 2 , f"E1 Expected length 2, got {len(var.vars)}"
    
    # Test that the first element of `var.vars` is equal to `q`
    assert var.vars[0] == q , f"E2 Expected {q}, got {var.vars[0]}"
    
    # Test that the second element of `var.vars` is equal to `q_dot`
    assert var.vars[1] == q_dot , f"E3 Expected {q_dot}, got {var.vars[1]}"
    
    # Test that the whole output matches
    assert var.vars == [q, q_dot] , f"E4 Expected {[q, q_dot]}, got {var.vars}"

def test_sys_var_named_pretty_syms():#

    var = DynamicSymbols(["M_{Mot}","F1_{ext}"],1,1,True)
    q =    se.Matrix([se.Symbol(r"M_Mot",real = True), se.Symbol("F1_ext",real = True)])
    q_dot = se.Matrix([se.Symbol(r"M_Mot_dot",real = True), se.Symbol(r"F1_ext_dot",real = True)])
    
    assert var._syms == [q, q_dot]
    
def test_sys_var_invalid_symbols_type():
    # Test that a TypeError is raised if a dictionary is passed as the `symbols` argument
    with pytest.raises(TypeError):
        var = DynamicSymbols({"a": 1, "b": 2}, 2, 2)
    
    # Test that a TypeError is raised if a tuple is passed as the `symbols` argument
    with pytest.raises(TypeError):
        var = DynamicSymbols(("a", "b"), 2, 2)
