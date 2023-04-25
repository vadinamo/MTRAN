from nodes.node import Node


class VariableNode(Node):
    def __init__(self, variable):
        self.variable = variable
