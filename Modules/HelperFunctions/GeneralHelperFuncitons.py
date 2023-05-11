from typing import Union, Any, List, Tuple
import symengine as se

def SymbolicMatrix(symbol:str, rows:int, cols:int) -> se.Matrix:
    """Creates a symbolic matrix with the given symbol.

    Args:
        symbol: The symbol to use for the matrix.
        rows: The number of rows of the matrix.
        cols: The number of columns of the matrix.

    Returns:
        A symbolic matrix with the given symbol and the given dimensions.
    """
    
    for i in range(rows):
        for ii in range(cols):
            if i == 0 and ii == 0:
                m = se.Matrix([[se.Symbol(symbol + f"_{{{i}{ii}}}")]])
            else:
                m = m.row_join(se.Matrix([[se.Symbol(symbol + f"_{{{i}{ii}}}")]]))
    
    return m.reshape(rows,cols)