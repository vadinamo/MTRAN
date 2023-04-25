from nodes.node import Node


class ForNode(Node):
    def __init__(self, begin: Node, condition: Node, step: Node, body: Node):
        self.begin = begin
        self.condition = condition
        self.step = step
        self.body = body
