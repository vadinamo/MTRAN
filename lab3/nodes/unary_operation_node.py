from entities.token import Token
from nodes.node import Node


class UnaryOperationNode(Node):
    def __init__(self, operation: Token, node: Node):
        self.operation = operation
        self.node = node
