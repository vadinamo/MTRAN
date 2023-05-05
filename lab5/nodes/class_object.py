from entities.token import Token
from nodes.node import Node


class ClassObject(Node):
    def __init__(self, class_variable: Token, parameters: []):
        self.class_variable = class_variable
        self.parameters = parameters
