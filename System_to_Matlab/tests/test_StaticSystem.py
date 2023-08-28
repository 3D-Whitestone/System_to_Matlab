import pytest
import symengine as se
from System_to_Matlab import StaticSystem
from System_to_Matlab import StaticSymbols

[x,y,z] = StaticSymbols(["x","y","z"])
[in1,in2,in3] = StaticSymbols(["in_1","in_2","in_3"])

def test_addAdditionalEquation():
    sys = StaticSystem()
    sys.addAdditionalEquation(x**2, 'x')
    assert len(sys._Equations) == 1
    assert sys._Equations[0][0] == x**2
    assert sys._Equations[0][1] == 'x'

def test_addAdditionalEquation_list():
    sys = StaticSystem()
    sys.addAdditionalEquation([x**2,y**2,z**2], ['x','y','z'])
    assert len(sys._Equations) == 1
    assert sys._Equations[0][0] == [x**2,y**2,z**2]
    assert sys._Equations[0][1] == ['x','y','z']
    
def test_addAdditionalEquation_multible():
    sys = StaticSystem()
    sys.addAdditionalEquation(x**2, 'x')
    sys.addAdditionalEquation([y**2,z**2], ['y','z'])
    assert len(sys._Equations) == 2
    assert sys._Equations[0][0] == x**2
    assert sys._Equations[0][1] == 'x'
    assert sys._Equations[1][0] == [y**2,z**2]
    assert sys._Equations[1][1] == ['y','z']

def test_addInput_single():
    sys = StaticSystem()
    sys.addInput(in1, 'in1')
    assert len(sys._Inputs) == 1
    assert sys._Inputs[0][0] == in1
    assert sys._Inputs[0][1] == 'in1'

def test_addInput_list():
    sys = StaticSystem()
    sys.addInput([in1,in2,in3], ['in1','in2','in3'])
    assert len(sys._Inputs) == 1
    assert sys._Inputs[0][0] == [in1,in2,in3]
    assert sys._Inputs[0][1] == ['in1','in2','in3']
    
def test_addInput_multible():
    sys = StaticSystem()
    sys.addInput(in1, 'in1')
    sys.addInput([in2,in3], ['in2','in3'])
    assert len(sys._Inputs) == 2
    assert sys._Inputs[0][0] == in1
    assert sys._Inputs[0][1] == 'in1'
    assert sys._Inputs[1][0] == [in2,in3]
    assert sys._Inputs[1][1] == ['in2','in3']
    

def test_addOutput_single():
    sys = StaticSystem()
    sys.addOutput(x**2, 'y')
    assert len(sys._Outputs) == 1
    assert sys._Outputs[0][0] == x**2
    assert sys._Outputs[0][1] == 'y'

def test_addOutput_list():
    sys = StaticSystem()
    sys.addOutput([x**2,y**2,z**2], ['x','y','z'])
    assert len(sys._Outputs) == 1
    assert sys._Outputs[0][0] == [x**2,y**2,z**2]
    assert sys._Outputs[0][1] == ['x','y','z']
    
def test_addOutput_multible():
    sys = StaticSystem()
    sys.addOutput(x**2, 'x')
    sys.addOutput([y**2,z**2], ['y','z'])
    assert len(sys._Outputs) == 2
    assert sys._Outputs[0][0] == x**2
    assert sys._Outputs[0][1] == 'x'
    assert sys._Outputs[1][0] == [y**2,z**2]
    assert sys._Outputs[1][1] == ['y','z']

# def test_write_MFunctions():
#     sys = StaticSystem()
#     sys.addInput(in1, 'input')
#     sys.addOutput(x**2, 'y')
#     sys.addAdditionalEquation(in1**2+in1, x)
#     sys.write_MFunctions('test_MFunction')
#     # TODO: add assertions for file existence and content


# def test_write_init_File():
#     sys = StaticSystem()
#     sys.addInput(u, 'input')
#     sys.addOutput(x**2, 'y')
#     sys.addAdditionalEquation(x**2 + u, 'x')
#     sys.write_init_File('test_init_File')
#     # TODO: add assertions for file existence and content