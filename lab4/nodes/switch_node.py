from entities.token import Token
from nodes.node import Node


class SwitchNode(Node):
    def __init__(self, variable: Token, body: Node):
        self.variable = variable
        self.body = body
