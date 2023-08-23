import pytest
import symengine as se
from System_to_Matlab import StaticSymbol, StaticSymbols


def test_StaticSymbol_standard():
    # Test initialization with valid input
    ss = StaticSymbol("x")
    assert ss._Notation == "x"
    assert ss._number_of_variables == 1
    
def test_StaticSymbol_invalid_input():
    # Test initialization with invalid input
    with pytest.raises(ValueError):
        ss = StaticSymbol("")
        
def test_StaticSymbol_vars():
    # Test the vars property
    ss = StaticSymbol("x", 3).vars
    assert isinstance(ss, se.Matrix)
    assert isinstance(ss[0], se.Symbol)
    assert str(ss) == "[x_{1}]\n[x_{2}]\n[x_{3}]\n"
    
def test_StaticSymbols_standard():
    # Test initialization with valid input
    ss = StaticSymbols(["x","y","z"])
    assert isinstance(ss, list)
    assert isinstance(ss[0], se.Symbol)
    

    
    