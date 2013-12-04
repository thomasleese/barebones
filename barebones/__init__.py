import argparse

from .interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description = "Barebones Interpreter.")
    parser.add_argument("files", type = str, nargs = "+", help = "Barebones files")
    args = parser.parse_args()

    for filename in args.files:
        Interpreter(filename).run()
