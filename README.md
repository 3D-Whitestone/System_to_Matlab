# System-to-Matlab

This is a small library written to convert Sympy expressions into Matlab code (Funktions, S-Funktions, ...). 

# Basic functionality

The first thing introduced with this library is a new "type" of variable. These variables are symengine variables but also include some additional functionality.  

### Dynamic Symbol

There are two types Dynamic and Static Symbols. 
The difference is that Dynamic Symbols are represented as Funktions of $t$ (e.g. $x(t)$). This is needed if you want to differentiate them. 

```python
from System_to_Matlab import DynamicSymbol

ds = DynamicSymbol("x", number_of_variables=2, number_of_derivatives=1).vars

display(ds)
```
$ \left[ \left[\begin{matrix}x_{1}{\left(t \right)}\\x_{2}{\left(t \right)}\end{matrix}\right], \  \left[\begin{matrix}\dot{x}_{1}{\left(t \right)}\\\dot{x}_{2}{\left(t \right)}\end{matrix}\right]\right]$

#### differentiation 

All Dynamic Symbols depend on the variable t.
```python
x = ds[0]
t = DynamicSymbol._derivation_variable
disp(x)
```
$$
\left[\begin{matrix}x_{1}{\left(t \right)}\\x_{2}{\left(t \right)}\end{matrix}\right] 
$$
```python
disp(se.diff(x, t))
```
$$
\left[\begin{matrix}\frac{d}{d t} x_{1}{\left(t \right)}\\\frac{d}{d t} x_{2}{\left(t \right)}\end{matrix}\right] 
$$
```python
from System_to_Matlab import diff_t
disp(diff_t(x))
```
$$
\left[\begin{matrix}\dot{x}_{1}{\left(t \right)}\\\dot{x}_{2}{\left(t \right)}\end{matrix}\right]
$$

These variables can be differentiated without any issue. The diff_t function can be used to directly replace the derivative with the corresponding symbol. 

### Static Symbol

The Static Symbol represents a variable without a dependency. 

```python
 ds = StaticSymbol("x", number_of_variables=2).vars
disp(ds)
```
$$ \left[\begin{matrix}x_{1}\\x_{2}\end{matrix}\right] $$

