from entities.token import Token

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