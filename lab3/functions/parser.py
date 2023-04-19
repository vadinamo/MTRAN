from functions.lexer import Lexer
from nodes.nodes_module import *


class Parser:
    def __init__(self, tokens: [], lexer: Lexer):
        self.tokens = tokens
        self.position = 0
        self.scope = {}
        self.lexer = lexer  # instead of

    def match(self, expected):
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if current_token.word in expected:
                self.position += 1
                return current_token

        return None

    def require(self, expected):
        token = self.match(expected)
        if token is None:
            raise Exception(f'Expected {expected[0].word} at {self.position}')

        return token

    def parse_expression(self) -> Node:
        if self.match(self.lexer.var_tokens.keys()):
            pass
        if self.match(self.lexer.var_types_tokens):
            pass
        if self.match(self.lexer.func_tokens.keys()):
            pass
        if self.match(self.lexer.constants_tokens.keys()):
            pass
        if self.match(self.lexer.key_word_tokens):
            pass

    def parse_code(self) -> Node:
        root = StatementsNode()
        while self.position < len(self.tokens):
            code_string_node = self.parse_expression()
            self.require('SEPARATOR')  # must be changed
            root.add_node(code_string_node)

        return root
