import symengine as se


def Drehmatrix(angle_vec: se.Matrix | list) -> se.Matrix:
    """Computes the 3D rotation matrix for the given angle vector.

    The angle vector must be in the form [x, y, z], where x, y, and z
    represent the angles of rotation around the x, y, and z axes, respectively.

    Args:
        angle_vector: A 3x1 matrix or a list of three numbers representing the angles of rotation around the x, y, and z axes.

    Returns:
        A 3x3 symengine matrix representing the rotation matrix for the given angle vector.

    Raises:
        ValueError: If the input is not a valid angle vector.
    """
    angle_vec = se.Matrix(angle_vec)
    if angle_vec.shape != (3, 1):
        raise ValueError("The input must be a 3x1 matrix representing the angles of rotation around the x, y, and z axes.")

    angle = angle_vec[0]
    Rx = se.Matrix([[1, 0, 0], [0, se.cos(angle), -se.sin(angle)],
                   [0, se.sin(angle), se.cos(angle)]])
    angle = angle_vec[1]
    Ry = se.Matrix([[se.cos(angle), 0, se.sin(angle)], [
                   0, 1, 0], [-se.sin(angle), 0, se.cos(angle)]])
    angle = angle_vec[2]
    Rz = se.Matrix([[se.cos(angle), -se.sin(angle), 0],
                   [se.sin(angle), se.cos(angle), 0], [0, 0, 1]])

    return Rz*Ry*Rx