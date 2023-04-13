from entities.token import Token
from nodes.nodes_module import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.scope = {}

    def match(self, expected):
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if current_token.token_type in expected:
                self.position += 1
                return current_token

        return None

    def require(self, expected):
        token = self.match(expected)
        if token is None:
            raise Exception(f'Expected {expected[0].word} at {self.position}')
        return token


    def parse_expression(self) -> Node:
        pass

    def parse_code(self) -> Node:
        root = StatementsNode()
        while self.position < len(self.tokens):
            code_string_node = self.parse_expression()
            self.require('SEPARATOR')
            root.add_node(code_string_node)
        return root
