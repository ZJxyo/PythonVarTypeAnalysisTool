def foo(a, arg):
    b = 2
    c = 2.0
    d = '2.0'
    e = b + c
    f = b * d
    k = False
    if bool_arg > 4:
        b = 2.5 + c
    elif arg == 4:
        b = '2.5' + d
    g = b
    return a + d

def boo(k):
    tool_version = 2
    x = foo(tool_version,k)
    return numpy.random.randint(5)
