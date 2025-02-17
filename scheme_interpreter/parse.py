from collections import deque

type expr = list[expr] | float | str

def tokenize(source: str) -> deque[str]:
    return deque(source.replace('(', ' ( ').replace(')', ' ) ').split())

def match(tokens: deque[str], token) -> bool:
    return tokens and tokens[0] == token

def parse(tokens: deque[str]) -> expr:
    if not tokens:
        raise Exception("Unexpected EOF")
    next = tokens.popleft()
    if next == '(':
        expr = []
        expr.append(parse(tokens))
        while not match(tokens, ')'):
            expr.append(parse(tokens))
        tokens.popleft()
        return expr
    elif next == ')':
        raise Exception("Unexpected ')'")
    else:
        return atom(next)

def atom(token):
    try:
        return float(token)
    except ValueError:
        return token