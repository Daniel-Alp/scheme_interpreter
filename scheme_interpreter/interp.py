import operator
from collections import deque
from functools import reduce
from parse import expr
from parse import parse

def global_env():
    env = [
        ('+', (lambda args : reduce(operator.add, args))),
        ('-', (lambda args : reduce(operator.sub, args))),
        ('*', (lambda args : reduce(operator.mul, args))),
        ('/', (lambda args : reduce(operator.truediv, args)))
    ]
    return env

def resolve_binding(lookup: str, env: list[tuple[str,]]):
    i = len(env) - 1
    while True:
        name, binding = env[i]
        if name == lookup:
            return binding
        i -= 1

def interp(expr: expr, env: list):
    if type(expr) is float:
        return expr
    if type(expr) is str:
        return resolve_binding(expr, env)
    match expr[0]:
        case "let":
            for binding in expr[1]:
                name = binding[0]
                defn = interp(binding[1], env)
                env.append((name, defn))
            return interp(expr[2], env)
        case _:
            func = interp(expr[0], env)
            args = list(map(lambda arg : interp(arg, env), expr[1:]))
            return func(args)

if __name__ == "__main__":
    print(interp(parse(deque(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')'])),
                 global_env()))
    print(interp(parse(deque(['(', '-', '34', '3', '2', '1', ')'])),
                 global_env()))
    print(interp(parse(deque(['(', 'let', '(', '(', 'a', '(', '+', '1', '2', ')', ')', '(', 'b', '4', ')', ')', '(', '+', 'a', 'b', ')', ')'])),
                 global_env()))
    # print(interp(parse(deque(['(', '(', 'lambda', '(', 'n', ')', '(', '*', 'n', 'n', ')', ')', '10', ')'])),
    #              global_env()))