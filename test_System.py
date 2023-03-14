from Modules.Robotik_System import *
import symengine as se
import sympy
import pytest

def test_Drehmatrix_valid_input():
    # Test that the Drehmatrix() method returns the expected result for a valid angle vector input.
    angle_vec = se.Matrix([[0], [0], [0]])
    expected_result = se.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    result = Drehmatrix(angle_vec)
    assert result == expected_result, f'Expected {expected_result}, but got {result}'


def test_Drehmatrix_invalid_input():
    # Test that the Drehmatrix() method raises a ValueError when the input is not a valid angle vector.
    angle_vec = se.Matrix([[0], [0]])
    with pytest.raises(ValueError):
        Drehmatrix(angle_vec)

    angle_vec = [0, 0]
    with pytest.raises(ValueError):
        Drehmatrix(angle_vec)

    angle_vec = 'invalid input'
    with pytest.raises(ValueError):
        Drehmatrix(angle_vec)
        
