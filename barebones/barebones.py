import re

class LexicalAnalyser(object):
    rules = [
        ( "KEYWORD", "while|clear|incr|decr|not|do|end" ),
        ( "IDENTIFIER", "[A-Za-z_]+" ),
        ( "TERMINATOR", ";" ),
        ( "INTEGER", "[0-9]+" ),
        ( None, "[ \n\r]" )
    ]

    def __init__(self, filename):
        self.filename = filename

    def analyse(self):
        tokens = []

        with open(self.filename) as fd:
            buffer = fd.read()
            pos = 0
            end = len(buffer)

            while pos < end:
                substr = buffer[pos:end]
                for rule in self.rules:
                    res = re.match(rule[1], substr)
                    if res:
                        value = res.group(0)
                        if rule[0]:
                            tokens.append(( rule, value ))

                        pos += len(value)
                        break
                else:
                    print("ARGH!")
                    break

        return tokens

class SyntaxTree(object):
    def __init__(self, tokens):
        self.tokens = tokens

class Interpreter(object):
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        tokens = LexicalAnalyser(self.filename).analyse()
        print(tokens)
