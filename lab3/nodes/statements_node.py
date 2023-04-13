from nodes.node import Node


class StatementsNode(Node):
    def __init__(self):
        self.nodes = []

    def add_nodes(self, expression_node):
        self.nodes.append(expression_node)
