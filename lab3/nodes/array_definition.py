from nodes.node import Node


class ArrayDefinition(Node):
    def __init__(self, variable: Node, sizes: list):
        self.variable = variable
        self.sizes = sizes
