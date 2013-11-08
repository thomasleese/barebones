import re

class CompilerError(Exception):
    pass

class RuntimeError(Exception):
    pass

class LexicalAnalyser(object):
    rules = [
        ( "KEYWORD", "while|clear|incr|decr|do|end|sub|call|init|print|if|then|print" ),
        ( "OPERATOR", "not|!=|==" ),
        ( "TERMINATOR", ";" ),
        ( "IDENTIFIER", "[A-Za-z_]+" ),
        ( "INTEGER", "[0-9]+" ),
        ( "STRING", "\"[^\"]+\"" ),
        ( None, "[ \n\r\t]" ),
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

    def is_string(self):
        return self.is_token("STRING")

    def read_string(self):
        token = self.read_token("STRING")
        return ( token[0], token[1][1:-1] )

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
        return self.is_keyword([ "clear", "incr", "decr", "while", "sub", "call", "init", "if", "print" ])

    def read_statement(self):
        if self.is_keyword([ "clear" ]):
            return self.read_clear_statement()
        elif self.is_keyword([ "incr" ]):
            return self.read_incr_statement()
        elif self.is_keyword([ "decr" ]):
            return self.read_decr_statement()
        elif self.is_keyword([ "while" ]):
            return self.read_while_statement()
        elif self.is_keyword([ "sub" ]):
            return self.read_sub_statement()
        elif self.is_keyword([ "call" ]):
            return self.read_call_statement()
        elif self.is_keyword([ "init" ]):
            return self.read_init_statement()
        elif self.is_keyword([ "if" ]):
            return self.read_if_statement()
        elif self.is_keyword([ "print" ]):
            return self.read_print_statement()
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

    def read_sub_statement(self):
        self.read_keyword([ "sub" ])
        identifier = self.read_identifier()
        self.read_terminator()
        block = self.read_block()
        return ( "SUBROUTINE", identifier, block )

    def read_call_statement(self):
        self.read_keyword([ "call" ])
        identifier = self.read_identifier()
        self.read_terminator()
        return ( "CALL", identifier )

    def read_init_statement(self):
        self.read_keyword([ "init" ])
        identifier = self.read_identifier()
        expr = self.read_expression()
        self.read_terminator()
        return ( "INIT", identifier, expr )

    def read_if_statement(self):
        self.read_keyword([ "if" ])
        expr = self.read_expression()
        self.read_keyword([ "then" ])
        self.read_terminator()
        block = self.read_block()
        return ( "IF", expr, block )

    def read_print_statement(self):
        self.read_keyword([ "print" ])
        operand = self.read_expression()
        self.read_terminator()
        return ( "PRINT", operand )

    def read_block(self):
        statements = [ ]
        while self.is_statement():
            statements.append(self.read_statement())

        self.read_keyword([ "end" ])
        self.read_terminator()
        return ( "BLOCK", statements )

    def read_operand(self):
        if self.is_identifier():
            return ( "OPERAND", self.read_identifier() )
        elif self.is_string():
            return ( "OPERAND", self.read_string() )
        else:
            return ( "OPERAND", self.read_integer() )

    def read_binary_expression(self):
        lhs = self.read_operand()
        op = self.read_operator()
        rhs = self.read_operand()
        return ( "BINARY_EXPRESSION", lhs, op, rhs )

    def read_expression(self):
        if self.is_string() or self.is_integer():
            return ( "UNARY_EXPRESSION", self.read_operand() )
        else:
            return self.read_binary_expression()

    def generate(self):
        return self.read_block()

class Interpreter(object):
    def __init__(self, filename):
        self.filename = filename
        self.variables = { }
        self.subroutines = { }

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

    def get_subroutine(self, identifier):
        try:
            return self.subroutines[identifier[1]]
        except KeyError:
            print("Try defining " + identifier[0] + " first!")

    def set_subroutine(self, identifier, block):
        self.subroutines[identifier[1]] = block

    def get_operand(self, operand):
        if operand[1][0] == "IDENTIFIER":
            return self.get_variable(operand[1])
        else:
            return operand[1][1]

    def eval_expression(self, expr):
        if expr[0] == "BINARY_EXPRESSION":
            lhs = self.get_operand(expr[1])
            op = expr[2][1]
            rhs = self.get_operand(expr[3])

            if op == "not":
                return lhs != rhs
            elif op == "==":
                return lhs == rhs
            else:
                raise RuntimeError("No such operator! " + op)
        else:
            return self.get_operand(expr[1])

    def run_clear_statement(self, statement):
        self.set_variable(statement[1], 0)

    def run_incr_statement(self, statement):
        self.change_variable(statement[1], +1)

    def run_decr_statement(self, statement):
        self.change_variable(statement[1], -1)

    def run_while_statement(self, statement):
        while self.eval_expression(statement[1]):
            self.run_block(statement[2])

    def run_subroutine_statement(self, statement):
        self.set_subroutine(statement[1], statement[2])

    def run_call_statement(self, statement):
        block = self.get_subroutine(statement[1])
        self.run_block(block)

    def run_init_statement(self, statement):
        identifier = statement[1]
        expr = statement[2]
        self.set_variable(identifier, self.eval_expression(expr))

    def run_if_statement(self, statement):
        if self.eval_expression(statement[1]):
            self.run_block(statement[2])

    def run_print_statement(self, statement):
        print(self.eval_expression(statement[1]))

    def run_statement(self, statement):
        if statement[0] == "CLEAR":
            self.run_clear_statement(statement)
        elif statement[0] == "INCR":
            self.run_incr_statement(statement)
        elif statement[0] == "DECR":
            self.run_decr_statement(statement)
        elif statement[0] == "WHILE":
            self.run_while_statement(statement)
        elif statement[0] == "SUBROUTINE":
            self.run_subroutine_statement(statement)
        elif statement[0] == "CALL":
            self.run_call_statement(statement)
        elif statement[0] == "INIT":
            self.run_init_statement(statement)
        elif statement[0] == "IF":
            self.run_if_statement(statement)
        elif statement[0] == "PRINT":
            self.run_print_statement(statement)
        else:
            raise RuntimeError("No such statement " + statement[0])

    def run_block(self, block):
        for statement in block[1]:
            self.run_statement(statement)

    def run(self):
        tokens = LexicalAnalyser(self.filename).analyse()
        ast = SyntaxTree(tokens).generate()
        self.run_block(ast)
        print(self.variables)
