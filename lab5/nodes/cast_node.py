from nodes.node import Node
from entities.token import Token


class CastNode(Node):
    def __init__(self, cast_type: Token, expression):
        self.cast_type = cast_type
        self.expression = expression
