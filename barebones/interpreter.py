from .errors import RuntimeError
from .lexer import LexicalAnalyser
from .ast import SyntaxTree

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
            elif op == "+":
                return lhs + rhs
            elif op == "-":
                return lhs - rhs
            elif op == "*":
                return lhs * rhs
            elif op == "/":
                return lhs / rhs
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
