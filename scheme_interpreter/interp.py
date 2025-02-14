import operator
from collections import deque
from functools import reduce
from parse import expr
from parse import parse

#TODO ERROR HANDLING

def global_env():
    env = [
        ('+', (lambda args : reduce(operator.add, args))),
        ('-', (lambda args : reduce(operator.sub, args))),
        ('*', (lambda args : reduce(operator.mul, args))),
        ('/', (lambda args : reduce(operator.truediv, args)))
    ]
    return env

def find_binding(lookup: str, env: list[tuple[str,]]):
    i = len(env) - 1
    while True:
        name, binding = env[i]
        if name == lookup:
            return binding
        i -= 1

def interp(expr: expr, env: list):
    if type(expr) is float:
        return expr
    elif type(expr) is str:
        return find_binding(expr, env)
    else:
        func = interp(expr[0], env)
        args = list(map(lambda arg : interp(arg, env), expr[1:]))
        return func(args)

if __name__ == "__main__":
    print(interp(parse(deque(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')'])),
                 global_env()))