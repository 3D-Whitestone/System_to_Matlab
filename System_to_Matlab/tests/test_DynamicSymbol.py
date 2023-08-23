import pytest
import symengine as se
from System_to_Matlab import DynamicSymbol, DynamicSymbols


def test_DynamicSymbol_values():
    # Test initialization with valid input
    ds = DynamicSymbol("x", number_of_variables=2, number_of_derivatives=1)
    assert ds._Notation == "x"
    assert ds._number_of_variables == 2
    assert ds._number_of_derivatives == 1
    
def test_DynamicSymbol_invalid_input():
    # Test initialization with invalid input
    with pytest.raises(ValueError):
        ds = DynamicSymbol("", number_of_variables=2, number_of_derivatives=1)
    
    with pytest.raises(ValueError):
        ds = DynamicSymbol("x", number_of_variables=-1, number_of_derivatives=0)
        
def test_DynamicSymbol_numbergeneration():
    # Test vars property
    ds = DynamicSymbol("x", number_of_variables=2, number_of_derivatives=0).vars
    assert isinstance(ds, se.Matrix)
    assert ds.shape == (2, 1)
    assert isinstance(ds[0], se.Function)
    assert isinstance(ds[1], se.Function)
    assert ds[0].args[0] == DynamicSymbol._derivation_variable
    assert str(ds) == "[x_{1}(t)]\n[x_{2}(t)]\n"
    
def test_DynamicSymbol_numbergeneration_with_derivatives():
    #Test vars with multiple derivatives
    ds = DynamicSymbol("x", number_of_variables=2, number_of_derivatives=3).vars
    assert isinstance(ds, list) 
    assert len(ds) == 4
    assert isinstance(ds[0], se.Matrix) 
    assert ds[0].shape == (2, 1)
    assert isinstance(ds[1], se.Matrix) 
    assert ds[1].shape == (2, 1)
    assert isinstance(ds[2], se.Matrix)
    assert ds[2].shape == (2, 1)
    assert str(ds) == "[[x_{1}(t)]\n[x_{2}(t)]\n, [\\dot{x}_{1}(t)]\n[\\dot{x}_{2}(t)]\n, [\\ddot{x}_{1}(t)]\n[\\ddot{x}_{2}(t)]\n, [x_{1}^{(3)}(t)]\n[x_{2}^{(3)}(t)]\n]"
    
def test_DynamicSymbols_standard():
    dss = DynamicSymbols(["x","y","z"])
    assert isinstance(dss, list)
    assert isinstance(dss[0], se.Function)
    
def test_DynamicSymbols_multible_vars():
    dss = DynamicSymbols(["x","y","z"], number_of_variables=2)
    assert isinstance(dss, list)
    assert isinstance(dss[0], se.Function)
    assert str(dss) == "[x_{1}(t), x_{2}(t), y_{1}(t), y_{2}(t), z_{1}(t), z_{2}(t)]"

def test_DynamicSymbols_with_derivatives():
    dss = DynamicSymbols(["x","y","z"], number_of_variables=2, number_of_derivatives=3)
    assert isinstance(dss, list)
    assert isinstance(dss[0], list)
    assert isinstance(dss[0][0], se.Function)
    assert str(dss) == "[[x_{1}(t), x_{2}(t), y_{1}(t), y_{2}(t), z_{1}(t), z_{2}(t)], [\dot{x}_{1}(t), \dot{x}_{2}(t), \dot{y}_{1}(t), \dot{y}_{2}(t), \dot{z}_{1}(t), \dot{z}_{2}(t)], [\ddot{x}_{1}(t), \ddot{x}_{2}(t), \ddot{y}_{1}(t), \ddot{y}_{2}(t), \ddot{z}_{1}(t), \ddot{z}_{2}(t)], [x_{1}^{(3)}(t), x_{2}^{(3)}(t), y_{1}^{(3)}(t), y_{2}^{(3)}(t), z_{1}^{(3)}(t), z_{2}^{(3)}(t)]]"
    
def test_DynamicSymbols_with_as_Matrix():
    dss = DynamicSymbols(["x","y","z"], number_of_variables=2, number_of_derivatives=3, as_matrix_list=True)
    assert isinstance(dss, list)
    assert isinstance(dss[0], se.Matrix)
    assert isinstance(dss[0][0], se.Function)
    assert str(dss) == "[[x_{1}(t)]\n[\\dot{x}_{1}(t)]\n[\\ddot{x}_{1}(t)]\n[x_{1}^{(3)}(t)]\n[x_{2}(t)]\n[\\dot{x}_{2}(t)]\n[\\ddot{x}_{2}(t)]\n[x_{2}^{(3)}(t)]\n, [y_{1}(t)]\n[\\dot{y}_{1}(t)]\n[\\ddot{y}_{1}(t)]\n[y_{1}^{(3)}(t)]\n[y_{2}(t)]\n[\\dot{y}_{2}(t)]\n[\\ddot{y}_{2}(t)]\n[y_{2}^{(3)}(t)]\n, [z_{1}(t)]\n[\\dot{z}_{1}(t)]\n[\\ddot{z}_{1}(t)]\n[z_{1}^{(3)}(t)]\n[z_{2}(t)]\n[\\dot{z}_{2}(t)]\n[\\ddot{z}_{2}(t)]\n[z_{2}^{(3)}(t)]\n]"