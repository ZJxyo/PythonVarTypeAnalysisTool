import random

import numpy

# test

#test another comment

def foo(a, b):
    
    x = 20.0
    if (a > b):
        x = "str"
    else:
        x = 66
    return x

def bar():
    a = 33
    b = 44
    b = a = 55
    x = foo(44, 33)

    x += a
    print(x)
