import operator
from functools import reduce
from typing import Any
from parse import expr

type env = list[tuple[str,Any]]

def global_env():
    env = [
        ('+', (lambda args : reduce(operator.add, args))),
        ('-', (lambda args : reduce(operator.sub, args))),
        ('*', (lambda args : reduce(operator.mul, args))),
        ('/', (lambda args : reduce(operator.truediv, args))),
        ('=', (lambda args : operator.eq(*args))),
        ('>=',(lambda args : operator.ge(*args))),
        ('<=',(lambda args : operator.le(*args))),
        ('>', (lambda args : operator.gt(*args))),
        ('<', (lambda args : operator.lt(*args))),
    ]
    return env

def lookup(lookup_id: str, env: env):    
    for binding in reversed(env):
        id, value = binding
        if id == lookup_id:
            if value is None:
                raise Exception(f"'{lookup_id}' undefined. Cannot use before initialization.")
            return value
    raise Exception(f"Unbound identifier '{lookup_id}'")

class Procedure:
    def __init__(self, params: list, body: expr, env: env):
        self.params = params
        self.env = env
        self.body = body    

    def __call__(self, args: list):
        if len(args) != len(self.params):
            raise Exception(f"Expected {len(self.params)} argument(s), got {len(args)}")
        return interp(self.body, self.env + list(zip(self.params, args)))

def interp(expr: expr, env: env):
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
        case "letrec":
            bindings = expr[1]
            new_env = env + [(name, None) for name,_ in bindings]
            for i in range(len(bindings)):
                name = bindings[i][0]
                value = interp(bindings[i][1], new_env)
                new_env[len(env) + i] = (name, value)
            body = expr[2]
            return interp(body, new_env)
        case "lambda":
            params = expr[1]
            body = expr[2]
            return Procedure(params, body, env)
        case "if":
            bool_expr = expr[1]
            true_expr = expr[2]
            false_expr = expr[3]
            if interp(bool_expr, env) is False:
                return interp(false_expr, env)
            return interp(true_expr, env)
        case _:
            closure = interp(proc, env)
            args = list(map(lambda arg : interp(arg, env), expr[1:]))
            return closure(args)