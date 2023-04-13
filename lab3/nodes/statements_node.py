from nodes.node import Node


class StatementsNode(Node):
    def __init__(self):
        self.nodes = []

    def add_node(self, node: Node):
        self.nodes.append(node)
