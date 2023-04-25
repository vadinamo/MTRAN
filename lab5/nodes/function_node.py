from entities.token import Token
from nodes.node import Node


class FunctionNode(Node):
    def __init__(self, name: Token, parameters: list, body: Node):
        self.name = name
        self.parameters = parameters
        self.body = body
