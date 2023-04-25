from nodes.node import Node


class WhileNode(Node):
    def __init__(self, condition: Node, body: Node):
        self.condition = condition
        self.body = body
