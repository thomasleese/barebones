import re

class CompilerError(Exception):
    pass

class RuntimeError(Exception):
    pass

class LexicalAnalyser(object):
    rules = [
        ( "KEYWORD", "while|clear|incr|decr|do|end" ),
        ( "OPERATOR", "not" ),
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
                    raise CompilerError("Syntax error!\n" + substr)

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

    def is_operator(self):
        return self.is_token("OPERATOR")

    def read_operator(self):
        return self.read_token("OPERATOR")

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

    def read_operand(self):
        if self.is_identifier():
            return ( "OPERAND", ( self.read_identifier() ) )
        else:
            return ( "OPERAND", ( self.read_integer() ) )

    def read_binary_expression(self):
        lhs = self.read_operand()
        op = self.read_operator()
        rhs = self.read_operand()
        return ( "EXPRESSION", lhs, op, rhs )

    def read_expression(self):
        return self.read_binary_expression()

    def generate(self):
        return self.read_block()

class Interpreter(object):
    def __init__(self, filename):
        self.filename = filename
        self.variables = { }

    def get_variable(self, identifier):
        try:
            return self.variables[identifier[1]]
        except KeyError:
            print("Try initialising " + identifier[0] + " first!")

    def set_variable(self, identifier, value):
        self.variables[identifier[1]] = value

    def change_variable(self, identifier, value):
        v = self.get_variable(identifier)
        self.set_variable(identifier, v + value)

    def get_operand(self, operand):
        if operand[1][0] == "IDENTIFIER":
            return self.get_variable(operand[1])
        else:
            return operand[1][1]

    def test_expression(self, expr):
        lhs = self.get_operand(expr[1])
        op = expr[2][1]
        rhs = self.get_operand(expr[3])

        if op == "not":
            return lhs != rhs

    def run_clear_statement(self, statement):
        self.set_variable(statement[1], 0)

    def run_incr_statement(self, statement):
        self.change_variable(statement[1], +1)

    def run_decr_statement(self, statement):
        self.change_variable(statement[1], -1)

    def run_while_statement(self, statement):
        while self.test_expression(statement[1]):
            self.run_block(statement[2])

    def run_statement(self, statement):
        if statement[0] == "CLEAR":
            self.run_clear_statement(statement)
        elif statement[0] == "INCR":
            self.run_incr_statement(statement)
        elif statement[0] == "DECR":
            self.run_decr_statement(statement)
        elif statement[0] == "WHILE":
            self.run_while_statement(statement)

    def run_block(self, block):
        for statement in block[1]:
            self.run_statement(statement)

    def run(self):
        tokens = LexicalAnalyser(self.filename).analyse()
        ast = SyntaxTree(tokens).generate()
        self.run_block(ast)
        print(self.variables)
