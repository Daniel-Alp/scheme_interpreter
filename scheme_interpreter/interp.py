import operator
from functools import reduce
from typing import Any
from parse import expr

def global_env():
    env = [
        ('+', (lambda args : reduce(operator.add, args))),
        ('-', (lambda args : reduce(operator.sub, args))),
        ('*', (lambda args : reduce(operator.mul, args))),
        ('/', (lambda args : reduce(operator.truediv, args)))
    ]
    return env

def lookup(lookup_id: str, env: list[tuple[str,Any]]):    
    for binding in reversed(env):
        id, value = binding
        if id == lookup_id:
            return value
    print(f"Unbound identifier '{lookup_id}'")
    raise Exception

def interp(expr: expr, env: list):
    if type(expr) is float: 
        return expr
    if type(expr) is str:
        return lookup(expr, env)
    proc = expr[0]
    match proc:
        case "define":
            name = expr[1]
            value = interp(expr[2], env)
            env.append((name, value))
        case "let":
            new_bindings = []
            for binding in expr[1]:
                name = binding[0]
                value = interp(binding[1], env)
                new_bindings.append((name, value))
            body = expr[2]
            return interp(body, env + new_bindings)
        case "lambda":
            params = expr[1]
            body = expr[2]
            return (lambda args : interp(body, env + list(zip(params, args))))
        case _:
            closure = interp(proc, env)
            args = map(lambda arg : interp(arg, env), expr[1:])
            return closure(args)