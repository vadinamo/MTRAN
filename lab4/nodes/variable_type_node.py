from entities.token import Token
from nodes.node import Node


class VariableTypeNode(Node):
    def __init__(self, type: Token):
        self.type = type
