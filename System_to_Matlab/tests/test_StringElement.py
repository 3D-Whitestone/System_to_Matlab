from System_to_Matlab.FileGenerators.MatlabElements import StringElement
import pytest
import symengine as se


def test_StringElement_standard():
    se = StringElement("Test \n Test2")
    assert se.generateCode() == "Test \n Test2"
    
def test_StringElement_indents():
    se = StringElement("Test \n Test2", indent=1)
    assert se.generateCode() == "\tTest \n\t Test2"