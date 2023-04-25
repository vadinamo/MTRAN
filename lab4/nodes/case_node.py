from entities.token import Token
from nodes.node import Node


class CaseNode(Node):
    def __init__(self, variable: Token):
        self.variable = variable
