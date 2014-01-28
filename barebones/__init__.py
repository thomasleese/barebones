from .interpreter import Interpreter

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description = "Barebones Interpreter.")
    parser.add_argument("files", type = str, nargs = "+", help = "Barebones files")
    args = parser.parse_args()

    for filename in args.files:
        Interpreter(filename).run()
