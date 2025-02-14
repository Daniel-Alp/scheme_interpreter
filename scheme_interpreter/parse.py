def rep_num(token: str):
    try:
        float(token)
    except ValueError:
        return False
    return True

type expr = list[expr] | float | str

def parse(tokens: list[str]) -> list[expr]:
    next = 0
    def parse_helper() -> expr:
        nonlocal next
        if next >= len(tokens):
            print("ERROR UNTERMINATED EXPRESSION")
            raise Exception

        token = tokens[next]
        next += 1
        if token == '(':
            expr = []
            while True:
                expr.append(parse_helper())
                if next >= len(tokens):
                    print("ERROR UNTERMINATED EXPRESSION")
                    raise Exception
                if tokens[next] == ')':
                    break
            return expr
        elif rep_num(token):
            return float(token)
        else:
            return token
    return parse_helper()

print(parse(['(', '+', '34', '(', '*', '4', '5', ')', '7', ')']))


print(parse(['1']))
try:
    print(parse(['(', '+', '1', '2']))
except Exception:
    pass