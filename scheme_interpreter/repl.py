from interp import interp
from interp import global_env
from parse import parse
from parse import tokenize

def run(source: str, env):
    return interp(parse(tokenize(source)), env)

def repl():
    env = global_env()
    while True:
        source = input(">>> ")
        print("   ", run(source, env))

if __name__ == "__main__":
    repl()