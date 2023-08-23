from System_to_Matlab.FileGenerators.MatlabElements import CodeElement
import pytest
import symengine as se

q1 = se.Symbol("q1")
q2 = se.Symbol("q2")
R = se.Matrix([[se.cos(q1+q2), -se.sin(q1+q2), 0],[se.sin(q1+q2), se.cos(q1+q2), 0],[0, 0, 1]])

def test_CodeElement_standard():
    ce =  CodeElement(R, "R")
    assert ce.generateCode() =="x0 = q1 + q2;\nx1 = cos(x0);\nx2 = sin(x0);\n\nR = [x1 -x2 0; x2 x1 0; 0 0 1];\n\nclear x0 x1 x2;\n"

def test_CodeElement_indents():
    ce =  CodeElement(R, "R", indent=1)
    assert ce.generateCode() =="\tx0 = q1 + q2;\n\tx1 = cos(x0);\n\tx2 = sin(x0);\n\n\tR = [x1 -x2 0; x2 x1 0; 0 0 1];\n\n\tclear x0 x1 x2;\n"

def test_CodeElement_no_cse():
    ce =  CodeElement(R, "R", use_cse=False)
    assert ce.generateCode() =="R = [cos(q1 + q2) -sin(q1 + q2) 0; sin(q1 + q2) cos(q1 + q2) 0; 0 0 1];\n"

def test_CodeElement_clear():
    ce = CodeElement(R, "R",  clear=False)
    assert ce.generateCode() =="x0 = q1 + q2;\nx1 = cos(x0);\nx2 = sin(x0);\n\nR = [x1 -x2 0; x2 x1 0; 0 0 1];\n\n"