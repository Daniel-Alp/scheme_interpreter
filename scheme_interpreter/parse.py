from collections import deque

def represent_num(token: str):
    try:
        float(token)
    except ValueError:
        return False
    return True

type expr = list[expr] | float | str

def parse(tokens: deque[str]) -> expr:
    next = tokens.popleft()
    if next == '(':
        expr = []
        expr.append(parse(tokens))
        while tokens[0] != ')':
            expr.append(parse(tokens))
        tokens.popleft()
        return expr
    elif represent_num(next):
        return float(next)
    else:
        return next

print(parse(deque(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')'])))
print(parse(deque(['1'])))
try:
    print(parse(deque(['(', '+', '1'])))
except Exception:
    print("Error")
try:
    print(parse(deque(['(', '+', '1', '(', '*', '+', ')'])))
except Exception:
    print("Error")