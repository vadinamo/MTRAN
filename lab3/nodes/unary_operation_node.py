from entities.token import Token
from nodes.node import Node


class UnaryOperationNode(Node):
    def __init__(self, operation: Token, element: Node):
        self.operation = operation
        self.element = element
