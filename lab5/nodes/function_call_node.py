from entities.token import Token
from nodes.node import Node

class FunctionCallNode(Node):
    def __init__(self, name: Token, parameters: list):
        self.name = name
        self.parameters = parameters
