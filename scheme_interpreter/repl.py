from interp import interp
from interp import global_env
from parse import parse
from parse import tokenize

def run(source: str, env):
    tokens = tokenize(source)
    while tokens:
        print("   ", interp(parse(tokens), env))

def repl():
    env = global_env()
    while True:
        try: 
            run(input(">>> "), env)
        except EOFError:
            print()
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    repl()