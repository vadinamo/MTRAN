from nodes.node import Node


class ConstantNode(Node):
    def __init__(self, constant):
        self.constant = constant
