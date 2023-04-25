from nodes.node import Node


class ReturnNode(Node):
    def __init__(self, statement: Node):
        self.statement = statement
