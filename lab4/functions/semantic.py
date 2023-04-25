from nodes.nodes_module import *


class Semantic:
    def __init__(self):
        pass

    def get_type(self, token_type):
        current_type = token_type.split(' ')[0]

        if current_type == 'STRING' or current_type == 'CHAR':
            return 'STRING'
        elif current_type == 'INT' or current_type == 'FLOAT':
            return 'NUMERIC'
        else:
            return 'BOOLEAN'

    def compare_types(self, operation, first_type, second_type=None):
        pass

    def parse(self, root):
        pass
