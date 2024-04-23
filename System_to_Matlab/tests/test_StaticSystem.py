import pytest
import symengine as se
from System_to_Matlab import StaticSystem, StaticSymbol
from System_to_Matlab import StaticSymbols
import filecmp
import os


[x,y,z] = StaticSymbols(["x","y","z"])
[in1,in2,in3] = StaticSymbols(["in_1","in_2","in_3"])
[out1, out2, out3] = StaticSymbols(["out_1","out_2","out_3"])
path_test = os.path.dirname(os.path.abspath(__file__)) + "\\Test_System"

def test_addAdditionalEquation():
    sys = StaticSystem()
    sys.addCalculation(x, x**2)
    assert len(sys._Equations.calcs) == 1
    assert sys._Equations.calcs[0][0] == x**2
    assert sys._Equations.vars[0][0] == x
    
def test_addAdditionalEquation_multible():
    sys = StaticSystem()
    sys.addCalculation(x, x**2)
    sys.addCalculation(y,se.Matrix([y**2,z**2]))
    assert len(sys._Equations.calcs) == 2
    assert sys._Equations.calcs[0][0] == x**2
    assert sys._Equations.vars[0][0] == x
    assert sys._Equations.calcs[1] == se.Matrix([y**2,z**2])
    assert sys._Equations.vars[1][0] == y

def test_addInput_single():
    sys = StaticSystem()
    sys.addInput(in1, 'in1')
    assert len(sys._Inputs) == 1
    assert sys._Inputs[0] == (in1, 'in1')

def test_addInput_list():
    sys = StaticSystem()
    sys.addInput(se.Matrix([in1,in2,in3]), "in")
    assert len(sys._Inputs) == 1
    assert sys._Inputs[0] == (se.Matrix([in1,in2,in3]), 'in')

    

def test_addOutput_single():
    sys = StaticSystem()
    sys.addOutput(se.Symbol('y'))
    assert len(sys._Outputs) == 1
    assert sys._Outputs[0] == se.Symbol('y')

    
def test_addOutput_multiple():
    sys = StaticSystem()
    sys.addOutput(se.Symbol('y'))
    sys.addOutput(se.Symbol('x'), "out1")
    assert len(sys._Outputs) == 2
    assert sys._Outputs[0] == se.Symbol('y')
    assert sys._Outputs[1] == se.Symbol('out1')

def test_write_MFunctions():
    sys = StaticSystem()
    sys.addInput(in1, 'input')
    sys.addInput(se.Matrix([in2,in3]), "input2")
    sys.addInput(se.Matrix([[in1,in2],[in3,in1]]), "input3")
    sys.addCalculation(x , in2**2+in3)
    sys.addCalculation(out1, x**2 + in1**2)
    sys.addCalculation(z, x**2)
    sys.addCalculation(out2, se.Matrix([out1,z]))
    sys.addOutput(out1, "output")
    sys.addOutput(out2)
    
    sys.write_MFunctions('test_MFunction', path_test)
    assert filecmp.cmp(path_test + "\\test_MFunction.m", path_test +"\\test_MFunction_ref.m", shallow = False) == True
    


# def test_write_init_File():
#     sys = StaticSystem()
#     sys.addInput(u, 'input')
#     sys.addOutput(x**2, 'y')
#     sys.addAdditionalEquation(x**2 + u, 'x')
#     sys.write_init_File('test_init_File')
#     # TODO: add assertions for file existence and content