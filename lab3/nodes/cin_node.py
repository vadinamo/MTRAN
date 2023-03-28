from nodes.node import Node


class CinNode(Node):
    def __init__(self, expression: list):
        self.expression = expression
        