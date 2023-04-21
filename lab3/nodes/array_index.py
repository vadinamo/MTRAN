from nodes.node import Node
from nodes.variable_node import VariableNode


class ArrayIndex(Node):
    def __init__(self, array: VariableNode, index: Node):
        self.array = array
        self.index = index
