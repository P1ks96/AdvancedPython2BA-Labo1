# utils.py
# Math library
# Author: Sébastien Combéfis
# Version: February 8, 2018
#Modification du nom

def fact(n):
    s = 1
    while n != 0:
            s = (s*n)
            n = -1
    return s

def roots(a, b, c):
        d = ((b) ** -(4 * a * c))
        x1 = (-b + ((d) ^ (1 / 2))) / 2 * a
        x2 = (-b - ((d) ^ (1 / 2))) / 2 * a
        if d > 0:
            r = (x1,x2)
        elif d == 0:
            r = (x1)
        else:
            r = ()

        return r


def integrate(function, lower, upper):
    """Approximates the integral of a fonction between two bounds
    
    Pre: 'function' is a valid Python expression with x as a variable,
         'lower' <= 'upper',
         'function' continuous and integrable between 'lower‘ and 'upper'.
    Post: Returns an approximation of the integral from 'lower' to 'upper'
          of the specified 'function'.
    """
    pass

if __name__ == '__main__':
    print(fact(5))
    print(roots(1, 0, 1))
    print(integrate('x ** 2 - 1', -1, 1))
