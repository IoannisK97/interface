import sympy as sp
import re

def format_polynomial(coefficients):

    degree = len(coefficients) - 1

   
    polynomial_str = ""

    for i, coef in enumerate(coefficients):
        power = degree - i

        if coef != 0:
            if power == 0:
                if coef >= 0:
                    polynomial_str += f"+ {coef}"
                else:
                    polynomial_str += f"- {-coef}"
            elif power == 1:
                if coef >= 0:
                    polynomial_str += f"+ {coef}x"
                else:
                    polynomial_str += f"- {-coef}x"
            else:
                if coef >= 0:
                    polynomial_str += f"+ {coef}x^{power}"
                else:
                    polynomial_str += f"- {-coef}x^{power}"

    if polynomial_str[0] == '+':
        polynomial_str = polynomial_str[2:]

    return polynomial_str



def create_polynomial_function_from_string(polynomial_str):
    print(polynomial_str)
    polynomial_str = polynomial_str.replace('^', '**')

    polynomial_str = re.sub(r'([0-9]+)x', r'\1 * x', polynomial_str)
    print(polynomial_str)

    def f(x):
        return eval(polynomial_str)

    return f

def calculate_derivative(func):
    
    x = sp.symbols('x')  
    f_derivative = sp.diff(func(x), x)  
    derivative_function = sp.lambdify(x, f_derivative, 'numpy')
    derivative_polynomial_str = sp.expand(f_derivative).simplify().as_poly().as_expr()
    #print(derivative_polynomial_str)
    return derivative_function

