from functions.lexer import Lexer
from nodes.nodes_module import *
from entities.constants import all_operators


class Parser:
    def __init__(self, lexer: Lexer):
        self.tokens = lexer.tokens
        self.position = 0
        self.scope = {}
        self.lexer = lexer  # instead of

    def match(self, expected: []) -> Token:
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            # print(current_token.word, expected, current_token.word in expected)
            if current_token.word in expected:
                self.position += 1
                return current_token

        return None

    def require(self, expected):
        token = self.match(expected)
        if token is None:
            raise Exception(f'Expected {expected} at {self.position}')

        return token

    def parse_variable_or_constant(self) -> Node:
        constant = self.match(self.lexer.constants_tokens.keys())
        if constant:
            return ConstantNode(constant)

        var = self.match(self.lexer.var_tokens.keys())
        if var:
            return VariableNode(var)

        raise Exception(f'Expected number or variable at {self.position}')

    def parse_parentheses(self) -> Node:
        if self.match(['(']):
            node = self.parse_formula()
            self.require([')'])

            return node

        else:
            return self.parse_variable_or_constant()

    def parse_formula(self) -> Node:
        left_node = self.parse_parentheses()
        operation = self.match(all_operators)

        while operation:
            if operation.word == '<<' or operation.word == '>>':
                self.position -= 1
                break
            elif operation.word == '++' or operation.word == '--':
                left_node = UnaryOperationNode(operation, left_node)
                operation = self.match(all_operators)
            else:
                right_node = self.parse_parentheses()
                left_node = BinaryOperationNode(operation, left_node, right_node)
                operation = self.match(all_operators)

        return left_node

    def parse_variable_definition(self, variable_token):
        var = VariableNode(variable_token)

        operation = self.match([','])
        while operation:
            new_var = self.match(self.lexer.var_tokens.keys())
            if new_var:
                var = BinaryOperationNode(Token('=', 'OPERATION'), var, VariableNode(new_var))
            else:
                raise Exception(f'Expected variable after "," at {self.position}')

            operation = self.match([','])

        operation = self.match(['='])
        if operation:
            value = self.parse_formula()
            self.require([';'])
            return BinaryOperationNode(operation, var, value)

        self.require([';'])
        return None

    def parse_cin(self):
        operation = self.match(['>>'])
        expression = []

        while operation:
            expression.append(self.parse_formula())
            operation = self.match(['>>'])

        self.require([';'])
        return CinNode(expression)

    def parse_cout(self):
        operation = self.match(['<<'])
        expression = []

        while operation:
            endl = self.match(['endl'])
            if endl:
                expression.append(KeyWordNode(endl))
            else:
                expression.append(self.parse_formula())

            operation = self.match(['<<'])

        self.require([';'])
        return CoutNode(expression)

    def parse_while(self):
        self.require(['('])
        condition = self.parse_formula()
        self.require([')'])

        self.require(['{'])
        body = self.parse_code()
        self.require(['}'])

        return WhileNode(condition, body)

    def parse_for(self):
        self.require(['('])
        self.match(self.lexer.var_types_tokens)
        begin = self.parse_formula()
        self.require([';'])
        condition = self.parse_formula()
        self.require([';'])
        step = self.parse_formula()
        self.require([')'])

        self.require(['{'])
        body = self.parse_code()
        self.require(['}'])

        return ForNode(begin, condition, step, body)

    def parse_if_else_condition(self):
        self.require(['('])
        condition = self.parse_formula()
        self.require([')'])

        self.require(['{'])
        body = self.parse_code()
        self.require(['}'])

        if self.match(['else']):
            if self.match(['if']):
                else_condition = self.parse_if_else_condition()
            else:
                self.require(['{'])
                else_condition = self.parse_code()
                self.require(['}'])

            return IfNode(condition, body, else_condition)

        return IfNode(condition, body, None)

    def parse_expression(self) -> Node:
        if self.match(self.lexer.var_tokens.keys()):
            self.position -= 1  # current position is variable
            var_node = self.parse_variable_or_constant()

            operation = self.match(all_operators)
            if operation:
                # unary and array processing
                right_formula_node = self.parse_formula()
                self.require([';'])
                return BinaryOperationNode(operation, var_node, right_formula_node)

        if self.match(self.lexer.var_types_tokens):
            variable_token = self.match(self.lexer.var_tokens.keys())
            if variable_token:
                return self.parse_variable_definition(variable_token)

            function_token = self.match(self.lexer.func_tokens.keys())
            if function_token:
                pass

            raise Exception(f'Expected variable or function at {self.position}')

        key_word = self.match(self.lexer.key_word_tokens)
        if key_word:
            if key_word.word == 'case':
                pass
            elif key_word.word == 'cin':
                return self.parse_cin()
            elif key_word.word == 'cout':
                return self.parse_cout()
            elif key_word.word == 'for':
                return self.parse_for()
            elif key_word.word == 'if':
                return self.parse_if_else_condition()
            elif key_word.word == 'switch':
                pass
            elif key_word.word == 'while':
                return self.parse_while()

    def parse_code(self) -> Node:  # block parse
        root = StatementsNode()
        while self.position < len(self.tokens):
            if self.match(['}']):
                self.position -= 1
                return root
            code_string_node = self.parse_expression()
            if code_string_node:
                root.add_node(code_string_node)

        return root
