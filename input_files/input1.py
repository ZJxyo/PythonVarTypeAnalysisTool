import random

import numpy


# class Input1:

    # global_var = "Hello World"
    #
    # def foo(self):
    #     input1 = Input1()
    #     x = input1.bar(1)
    #     if x > 0:
    #         x = 0
    #         if x > 1:
    #             y = 1
    #         elif x < 1:
    #             y = 1
    #         else:
    #             y = 2
    #         c = 2
    #         if x > 1:
    #             y = 1
    #         elif x > 2:
    #             y = 1
    #         else:
    #             y = 2
    #     elif x == 0:
    #         if x > 1:
    #             y = 1
    #         elif x > 2:
    #             y = 3
    #         else:
    #             y = 2
    #         y = 'one'
    #         if x > 1:
    #             y = 1
    #         elif x > 2:
    #             y = 3
    #         else:
    #             y = 2
    #     else:
    #         if x > 1:
    #             y = 1
    #         elif x < 1:
    #             y = 1
    #         else:
    #             y = 2
    #         c = 2
    #         if x > 1:
    #             y = 1
    #         elif x < 1:
    #             y = 1
    #         else:
    #             y = 2
    #
    # def bar(m):
    #     return 2*m
    #
    # def loops_foo(self):
    #     x = 0
    #     for i in range(69):
    #         x = 1
    #         y = 2
    #     else:
    #         z = 3
    #
    # def for_if_nested(self):
    #     for i in range(5):
    #         x = 123
    #         if i > 0:
    #             x = 123
    #             for j in range(5):
    #                 x = 123
    #                 if i > 0:
    #                     f = 1
    #                 else:
    #                     j = 1
    #                 t = 1
    #         elif i == 0:
    #             t = 1
    #             for t in range(42):
    #                 j = 99
    #                 if i > 0:
    #                     f = 1
    #                 else:
    #                     j = 1
    #                 t = 1
    #             t = 1
    #         elif i == -1:
    #             t = 1
    #             for k in range(55):
    #                 m = 5
    #                 if i > 0:
    #                     f = 1
    #                 else:
    #                     j = 1
    #                 t = 1
    #             m = 5
    #         else:
    #             m = 5
    #             for k in range(55):
    #                 m = 5
    #                 if i > 0:
    #                     f = 1
    #                 else:
    #                     j = 1
    #                 t = 1
    #             m = 5
    #
    # def while_foo(self):
    #     x = 0
    #     while x > 1:
    #         while x > 2:
    #             x = 4
    #         x = 3
    #     else:
    #         x = 4

    # def try_catch_foo(self):
    #     try:
    #         x = 1
    #     except ArithmeticError:
    #         x = 2
    #     except ZeroDivisionError:
    #         x = 3
    #     else:
    #         x = 4
    #     finally:
    #         x = 5

    # def unaryop(self):
    #     x = -11
    #     x = -x

    # def binaryop_add(self):
    #     x=1
    #     y=1
    #     x = x + y
    #     x = 1 + 1
    #     x = 1 + x
    #     x = 1 + 'a'
    #     x = 1 + (2 + 3 + (4 + 5))
    #     1 + (1 + 1)
    #     x = [1, 2] + [["1", "2"], 2]

    # def binaryop_sub(self):
    #     x=1
    #     y=1
    #     1 - 2
    #     3.0 - 1
    #     True - 1
    #     3.0 - False
    #     [3, 4] - 1

    # def binaryop_div(self):
    #     x=1
    #     y=1
    #     x = x / y
    #     x = 1 / 1
    #     x = 1 / x
    #     x = 1 / 'a'

    # def binaryop_mult(self):
    #     x=1
    #     y=1
    #     x = x * y
    #     x = 1 * 1
    #     x = 1 * x
    #     x = 1 * 'a'
    #     x = [1,1] * 5
    #     x = (1, 1) * 5
    #     x = [1, 2]

    # def binop(self):
    #     x = True and True
    #     y = x and False
    #     x = 1 or 1 or 2 and 3

    # def call1(self, x):
    #     return boo(a, b)
    #
    # def maincall(self):
    #     x = self.call1(2) + 1
    #     x= foo(a, b, c, boo(n))

    # def foo(self):
    #     x = 1
    #     y = "string"
    #     z = 1.23
    #     x = False
    #     y = t
    #     z = y

    # def if_var_union(self):
    #     x = 0
    #     y = random.Random.randint(0, 1)
    #     if y < 0.33:
    #         x = True
    #         if y > 0.11:
    #             x = 1.23
    #         else:
    #             x = "aaa"
    #             y = False
    #     elif y < 0.66:
    #         x = "Hello"
    #     else:
    #         x = 1
    #     x = 1

    # def forloop(self):
        # x = 0
        # y = [1, 2, [4, [7, 8], 6]]
        # x = [1, (1, (x, 3, (y, [2, 4, "aaa"])))]

        # for i in range(5):
        #     if i == y:
        #         x = "i = 0"
        #     elif i == y:
        #         x = True
        # for idx, val in enumerate(list['a','b']):
        # print(i)
        #
        # for i in [1, "string", ["aaa"]]:
        #     x = -1
        # #     print(i)

# {file name: {class name: {function name: {line number: {var name: {int: None},{list: int},{list: string}}}}}}

    # def bruh(self):
    #     x = -1
    #     x = not 1
    #     y = False
    #     if 1 > 0:
    #         x = "bruh"
    #     elif 1 == 1:
    #         x = 1.23
    #     else:
    #         x = -y
    #     z = -x
    #     a = "string"
    #     b = -a
    #     -t

    # def two_operands(self):
    #     a = True
    #     y = 1.2
    #     x = (1 + 1) + y
    #     # z = 'a'
    #     # x = y + z + x
    #     # y = x + 1
    #     # y = 1 + x
    #     # # y = x + x
    #     if x > 2:
    #         a = 1.0
    #         b = 2.0
    #     else:
    #         a = 'a'
    #         b = 'b'
    #     # x = a + b
    #     t = (a + 1) + ((y + 3) + x + 6)
    #     q = x + a + y

    # def boolop(self):
    #     a = (True and True) or False
    #     b = False and (True and True)
    #     x = a and True
    #     y = True or b
    #     z = a and b
    #     j = "string" and 1.0
    #     k = [1] or 1
    #     if a:
    #         p = [1, 0]
    #     else:
    #         p = (1, 0)
    #     q = p and a

    # def boo(self):
    #     a = 10
    #     y = False
    #     x = a
    #     y = x
    #     z = 1
    #     if 1>0:
    #         a = "str"
    #         x = 1
    #         z = False
    #         if 1<0:
    #             z = 'aaa'
    #     elif 1==0:
    #         a = [1]
    #     else:
    #         t = 1
    #         x = False


# def foo(a, b):
#     x = 1
#     y = a + b
#     y = a + x
#     y = b + x
    # y = -a
    # y = ~b
    # y = 1
    # y = b + [1]
    # y = a + [1]
    # a = 10
    # y = ~a
    # y = a * 1
    # y = a + 1
    # y = a + [1]
    # x = 1
    # if 1>0:
    #     x = "str"
    # else:
    #     x = 1
    # y = not x


    # return y
#
# def fff():
#     return -foo()
#
# def boo():
#     x = foo() + fff()

# def foo(a, b):
#     y = ~a
#     z = ~b
#     return "bruh"
# def foo2():
#     print()
# def boo():
# #     x = foo(-1, foo2())
# import numpy as np
#
#
# def foo(a):
#     return 1
#
# def foo(a, b):
#     x = foo(1)
#
# def foo(a):
#     return "33"
# def boo():
#     x=1
#     return [1]
#
#
# def foo2():
#     y=1

# def foo():
#     return "a  a"
# def boo():
#     print(foo().split())
#
#
# np.ndarray().max().

#
# def foo():
#     return "aaaa"
#
# def boo():
#     y = "aaa"
#     x = 'aaaaa'.foo().split().boo()
#     z = [1, 2].boo()
# a = [1, 'sttr', 1.2]
# a list
#     a[b[c]]
#     a[b][c]
#     a[b]
def foo():
    a = [1, 2, [3, 4, 5, [6, [7, 8], 9], 10], 11]
    y = 2 * a