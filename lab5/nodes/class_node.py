from entities.token import Token
from nodes.node import Node


class ClassNode(Node):
    def __init__(self, class_variable: Token, objects: []):
        self.class_variable = class_variable
        self.objects = objects
