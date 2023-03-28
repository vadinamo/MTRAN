from nodes.node import Node


class IfNode(Node):
    def __init__(self, condition: Node, body: Node, else_condition=None):
        self.condition = condition
        self.body = body
        self.else_condition = else_condition
