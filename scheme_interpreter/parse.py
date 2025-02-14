from collections import deque

type expr = list[expr] | float | str

# TODO error handling
def parse(tokens: deque[str]) -> expr:
    next = tokens.popleft()
    if next == '(':
        expr = []
        while tokens[0] != ')':
            expr.append(parse(tokens))
        tokens.popleft()
        return expr
    else:
        return atom(next)

def atom(token):
    try:
        return float(token)
    except ValueError:
        return token

print(parse(deque(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')'])))