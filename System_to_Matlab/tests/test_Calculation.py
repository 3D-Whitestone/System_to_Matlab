from System_to_Matlab.Calculation import Calculation
import pytest
import symengine as se



def test_Calculation_init():
    calc = Calculation()
    assert calc._inputs == []
    assert calc._outputs == []
    assert calc._vars == []
    assert calc._calcs == []
    
def test_addCalculation_simple():
    calc = Calculation()
    in1 = se.Symbol("input1")
    out1 = se.Symbol("output1")
    calc.addCalculation(out1, se.sin(in1))
    assert calc._outputs == [out1]
    assert calc._inputs == [in1]
    assert calc._vars == [se.Matrix([out1])]
    assert calc._calcs == [se.Matrix([se.sin(in1)])]

def test_addCalculation_matrix_1d():
    calc = Calculation()
    ins = se.Matrix([se.Symbol("in1"), se.Symbol("in2")])
    outs = se.Matrix([se.Symbol("out1"), se.Symbol("out2")])
    calc.addCalculation(outs, se.Matrix([se.sin(ins[0]), se.sin(ins[1])]))
    assert calc._outputs == [outs[0], outs[1]]
    assert calc._inputs == [ins[0], ins[1]]
    assert calc._vars == [outs]
    assert calc._calcs == [se.Matrix([se.sin(ins[0]), se.sin(ins[1])])]
    
def test_addCalculation_matrix_2d():
    calc = Calculation()
    ins = se.Matrix([se.Symbol("in1"), se.Symbol("in2"), se.Symbol("in3")])
    outs = se.Matrix([[se.Symbol("out1"), se.Symbol("out2"), se.Symbol("out3")], [se.Symbol("out4"), se.Symbol("out5"), se.Symbol("out6")], [se.Symbol("out7"), se.Symbol("out8"), se.Symbol("out9")]])
    mat = se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]) @ se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]).T
    calc.addCalculation(outs, mat)
    
    assert calc._outputs == [outs[0, 0], outs[0, 1], outs[0, 2], outs[1, 0], outs[1, 1], outs[1, 2], outs[2, 0], outs[2, 1], outs[2, 2]]
    assert calc._inputs == [ins[0], ins[1], ins[2]]
    assert calc._vars == [outs]
    assert calc._calcs == [mat]
    
    
def test_generate_shape_index_list():
    calc = Calculation()
    ins = se.Matrix([se.Symbol("in1"), se.Symbol("in2"), se.Symbol("in3")])
    outs = se.Matrix([[se.Symbol("out1"), se.Symbol("out2"), se.Symbol("out3")], [se.Symbol("out4"), se.Symbol("out5"), se.Symbol("out6")], [se.Symbol("out7"), se.Symbol("out8"), se.Symbol("out9")]])
    
    mat = se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]) @ se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]).T
    
    calc.addCalculation(outs[0,0], se.sin(ins[0]))
    calc.addCalculation(outs[:,0], se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]))
    calc.addCalculation(outs, mat)
    
    #also checking internal variables
    assert len(calc._outputs) == 9
    for i in outs:
        assert calc._outputs.__contains__(i)
    assert calc._inputs == [ins[0], ins[1], ins[2]]
    assert calc._vars == [se.Matrix([outs[0,0]]), outs[:,0], outs]
    assert calc._calcs == [se.Matrix([se.sin(ins[0])]), se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])]), mat]
        
    indizes_shapes, code_vector = calc._generate_shape_index_list()
    assert indizes_shapes == [((0, 1), (1, 1)), ((1, 4), (3, 1)), ((4, 13), (3, 3))]
    assert code_vector == se.Matrix([se.sin(ins[0])]).col_join(se.Matrix([se.sin(ins[0]), se.sin(ins[1]), se.sin(ins[2])])).col_join(mat.reshape(9,1))

def test_addCalculation_matrix_wrong_shape():
    calc = Calculation()
    var = se.Matrix([se.Symbol("var1"), se.Symbol("var2")])
    with pytest.raises(ValueError):
        calc.addCalculation(var, se.Matrix([se.sin(var[0])]))
        
def test_addCalculation_wrong_type():
    calc = Calculation()
    var = se.Matrix([se.Symbol("var1"), se.Symbol("var2")])
    with pytest.raises(TypeError):
        calc.addCalculation(var, se.sin(var[0]))
        
def test_appendCalculation():
    calc = Calculation()
    var = se.Matrix([se.Symbol("var1"), se.Symbol("var2"), se.Symbol("var3"), se.Symbol("var4")])
    calc.addCalculation(var[0], var[1]**2)
    calc2 = Calculation()
    calc2.addCalculation(var[2], var[3]**2)
    calc.append_Calculation(calc2)
    
    assert calc._outputs == [var[0], var[2]]
    assert calc._inputs == [var[1], var[3]]
    assert calc._vars == [se.Matrix([var[0]]), se.Matrix([var[2]])]
    assert calc._calcs == [se.Matrix([var[1]**2]), se.Matrix([var[3]**2])]
    
    
    

def test_addCalculation_var_calc_mismatch():
    calc = Calculation()
    var = se.Matrix([se.Symbol("var1"), se.Symbol("var2")])
    with pytest.raises(TypeError):
        calc.addCalculation(var, se.sin(var[0]))

def test_addCalculation_var_calc_shape_mismatch():
    calc = Calculation()
    var = se.Matrix([se.Symbol("var1"), se.Symbol("var2")])
    with pytest.raises(ValueError):
        calc.addCalculation(var, se.Matrix([se.sin(var[0])]))
