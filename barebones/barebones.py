import re

class CompilerError(Exception):
    pass

class LexicalAnalyser(object):
    rules = [
        ( "KEYWORD", "while|clear|incr|decr|not|do|end" ),
        ( "TERMINATOR", ";" ),
        ( "IDENTIFIER", "[A-Za-z_]+" ),
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
                            tokens.append(( rule[0], value ))

                        pos += len(value)
                        break
                else:
                    raise CompilerError("ARGH! You need to fix your code!\n" + substr)

        tokens.append(( "KEYWORD", "end" ))
        tokens.append(( "TERMINATOR", ))

        return tokens

class SyntaxTree(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def is_token(self, type):
        try:
            token = self.tokens[self.index]
            return token[0] == type
        except IndexError:
            return False

    def read_token(self, type):
        try:
            token = self.tokens[self.index]
            if self.is_token(type):
                self.index += 1
                return token
            else:
                raise CompilerError("Expected " + type + ", got " + str(token))
        except IndexError:
            raise CompilerError("Expected " + type + ", got nothing")

    def is_terminator(self):
        return self.is_token("TERMINATOR")

    def read_terminator(self):
        return self.read_token("TERMINATOR")

    def is_identifier(self):
        return self.is_token("IDENTIFIER")

    def read_identifier(self):
        return self.read_token("IDENTIFIER")

    def is_integer(self):
        return self.is_token("INTEGER")

    def read_integer(self):
        token = self.read_token("INTEGER")
        return ( token[0], int(token[1]) )

    def is_keyword(self, types):
        token = self.tokens[self.index]
        if self.is_token("KEYWORD"):
            return token[1] in types

        return False

    def read_keyword(self, types):
        token = self.read_token("KEYWORD")
        if token[1] in types:
            return ( "KEYWORD", token[1] )
        else:
            raise CompilerError("Expected one of " + str(types) + ", got " + str(token))

    def is_statement(self):
        return self.is_keyword([ "clear", "incr", "decr", "while" ])

    def read_statement(self):
        if self.is_keyword([ "clear" ]):
            return self.read_clear_statement()
        elif self.is_keyword([ "incr" ]):
            return self.read_incr_statement()
        elif self.is_keyword([ "decr" ]):
            return self.read_decr_statement()
        elif self.is_keyword([ "while" ]):
            return self.read_while_statement()
        else:
            raise CompilerError("Expected statement, got " + str(token))

    def read_clear_statement(self):
        self.read_keyword([ "clear" ])
        identifier = self.read_identifier()
        self.read_terminator()
        return ( "CLEAR", identifier )

    def read_incr_statement(self):
        self.read_keyword([ "incr" ])
        identifier = self.read_identifier()
        self.read_terminator()
        return ( "INCR", identifier )

    def read_decr_statement(self):
        self.read_keyword([ "decr" ])
        identifier = self.read_identifier()
        self.read_terminator()
        return ( "DECR", identifier )

    def read_while_statement(self):
        self.read_keyword([ "while" ])
        expr = self.read_expression()
        self.read_keyword([ "do" ])
        self.read_terminator()
        block = self.read_block()
        return ( "WHILE", expr, block )

    def read_block(self):
        statements = [ ]
        while self.is_statement():
            statements.append(self.read_statement())

        self.read_keyword([ "end" ])
        self.read_terminator()
        return ( "BLOCK", statements )

    def read_expression(self):
        identifier = self.read_identifier()
        self.read_keyword([ "not" ])
        integer = self.read_integer()
        return ( "NOT", ( "EQUAL", identifier, integer ) )

    def generate(self):
        return self.read_block()

class Interpreter(object):
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        tokens = LexicalAnalyser(self.filename).analyse()
        ast = SyntaxTree(tokens).generate()
        print(ast)
