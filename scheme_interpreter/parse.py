from collections import deque

type expr = list[expr] | float | str

def tokenize(source: str) -> deque[str]:
    return deque(token for token in source.replace('(', ' ( ').replace(')', ' ) ').split(' ') if token)

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
    print(parse(tokenize("(+ 34 (* 4 5)(* 5 6))")))