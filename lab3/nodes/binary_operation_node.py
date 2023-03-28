from entities.token import Token
from nodes.node import Node


class BinaryOperationNode(Node):
    def __init__(self, operation: Token, first_element: Node, second_element: Node):
        self.operation = operation
        self.first_element = first_element
        self.second_element = second_element
