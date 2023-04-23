from nodes.node import Node


class ArrayDefinition(Node):
    def __init__(self, variable: Node, sizes: list):
        self.variable = variable
        self.sizes = sizes
        self.elements = []

    def add_node(self, element: Node):
        self.elements.append(element)
