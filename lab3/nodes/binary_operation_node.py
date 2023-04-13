from entities.token import Token
from nodes.node import Node


class BinaryOperationNode(Node):
    def __init__(self, operation: Token, left_node: Node, right_node: Node):
        self.operation = operation
        self.left_node = left_node
        self.right_node = right_node
