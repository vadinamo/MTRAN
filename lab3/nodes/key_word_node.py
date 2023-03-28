from entities.token import Token
from nodes.node import Node


class KeyWordNode(Node):
    def __init__(self, word: Token):
        self.word = word
        