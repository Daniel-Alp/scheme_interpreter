from collections import deque

#TODO ERROR HANDLING

type expr = list[expr] | float | str

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

if __name__ == "__main__":
    print(parse(deque(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')'])))