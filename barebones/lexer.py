import re

from .errors import CompilerError

class LexicalAnalyser(object):
    rules = [
        ( "KEYWORD", "while|clear|incr|decr|do|end|sub|call|init|print|if|then|print" ),
        ( "OPERATOR", "not|!=|==|\\*|\\+|\\-|/" ),
        ( "TERMINATOR", ";" ),
        ( "IDENTIFIER", "[A-Za-z_]+" ),
        ( "INTEGER", "[0-9]+" ),
        ( "STRING", "\"[^\"]*\"" ),
        ( None, "[ \n\r\t]" ),
    ]

    def __init__(self, filename):
        self.filename = filename

    def analyse(self):
        tokens = [ ]

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
                            tokens.append(( rule[0], value ))

                        pos += len(value)
                        break
                else:
                    raise CompilerError("Syntax error!\n" + substr)

        tokens.append(( "KEYWORD", "end" ))
        tokens.append(( "TERMINATOR", ))

        return tokens
