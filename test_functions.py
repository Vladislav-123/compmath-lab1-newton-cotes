# Тестовые функции и их точные интегралы

import math

def f1(x):
    return math.exp(x)
def f1_exact(a, b):
    return math.exp(b) - math.exp(a)

def f2(x):
    return x**3
def f2_exact(a, b):
    return (b**4 - a**4) / 4

def f3(x):
    return math.sqrt(x)
def f3_exact(a, b):
    return (2/3) * (b**1.5 - a**1.5)

def f4(x):
    return 1 / (1 + 25 * x**2)
def f4_exact(a, b):
    return (math.atan(5*b) - math.atan(5*a)) / 5
