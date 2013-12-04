from .errors import CompilerError

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
        self.index += 1
        t = self.is_terminator()
        self.index -= 1

        if t:
            return ( "UNARY_EXPRESSION", self.read_operand() )
        else:
            return self.read_binary_expression()

    def generate(self):
        return self.read_block()
