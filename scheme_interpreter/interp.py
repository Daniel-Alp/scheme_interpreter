import operator
from functools import reduce
from parse import expr
from parse import parse
from parse import tokenize

def resolve_binding(lookup: str, env: list[tuple[str,]]):
    i = len(env) - 1
    while True:
        name, binding = env[i]
        if name == lookup:
            return binding
        i -= 1

def global_env():
    env = [
        ('+', (lambda args : reduce(operator.add, args))),
        ('-', (lambda args : reduce(operator.sub, args))),
        ('*', (lambda args : reduce(operator.mul, args))),
        ('/', (lambda args : reduce(operator.truediv, args)))
    ]
    return env

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
        case "lambda":     
            names = expr[1]
            body = expr[2]  
            return lambda args : interp(body, env + [(names[i], args[i]) for i in range(len(names))])
        case _:
            closure = interp(expr[0], env)
            args = list(map(lambda arg : interp(arg, env), expr[1:]))
            return closure(args)

if __name__ == "__main__":
    print(interp(parse(tokenize("(+ 1 2 (* 4 5) 6)")), global_env()))
    print(interp(parse(tokenize("(- 3 4 5)")), global_env()))
    print(interp(parse(tokenize("(let ((a (+ 1 200)) (b 4)) (+ a b))")), global_env()))
    print(interp(parse(tokenize("((lambda (x) (+ x 3)) 4)")), global_env()))


