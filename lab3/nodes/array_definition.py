from nodes.node import Node


class ArrayDefinition(Node):
    def __init__(self):
        self.elements = []

    def add_node(self, element: Node):
        self.elements.append(element)
