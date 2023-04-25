from nodes.nodes_module import *
from entities.constants import *


class Semantic:
    def __init__(self):
        pass

    def get_type(self, token_type):
        current_type = token_type.split(' ')
        if len(current_type) > 1:
            return current_type[0], current_type[1]  # data type, entity type

        return None

    def is_numeric(self, first_type, second_type):
        return first_type == 'INT' and second_type == 'FLOAT' or first_type == 'FLOAT' and \
            second_type == 'INT' or first_type == 'INT' and second_type == 'INT' or \
            first_type == 'FLOAT' and second_type == 'FLOAT'

    def analyze(self, root):
        if isinstance(root, Token):
            return self.get_type(root.token_type)
        elif isinstance(root, list):
            pass
        elif isinstance(root, StatementsNode):
            for node in root.nodes:
                return self.analyze(node)
        elif isinstance(root, UnaryOperationNode):
            pass
        elif isinstance(root, BinaryOperationNode):
            left = self.analyze(root.left_node)
            right = self.analyze(root.right_node)
            operation = root.operation.word

            if self.is_numeric(left[0], right[0]):
                return left[0], left[1]
            elif left[0] == 'STRING' and right[0] == 'STRING':
                if operation == '+':
                    return left[0], left[1]

                raise Exception('Only + available for STRING values')
            elif left[0] == 'BOOLEAN' and right[0] == 'BOOLEAN':
                if operation == '||' and operation == '&&':
                    return left[0], left[1]

                raise Exception('Only || or && available for BOOLEAN values')
            elif left[0] != right[0]:
                raise Exception(f'Cannot solve {left[0]} and {right[0]} types')

            return left[0], left[1]

        elif isinstance(root, VariableNode):
            return self.analyze(root.variable)
        elif isinstance(root, ConstantNode):
            return self.analyze(root.constant)
        elif isinstance(root, KeyWordNode):
            pass
        elif isinstance(root, CinNode):
            pass
        elif isinstance(root, CoutNode):
            pass
        elif isinstance(root, WhileNode):
            pass
        elif isinstance(root, ForNode):
            pass
        elif isinstance(root, IfNode):
            pass
        elif isinstance(root, FunctionNode):
            pass
        elif isinstance(root, FunctionCallNode):
            pass
        elif isinstance(root, SwitchNode):
            pass
        elif isinstance(root, CaseNode):
            pass
        elif isinstance(root, ArrayDefinition):
            pass
        elif isinstance(root, Array):
            pass
        elif isinstance(root, ReturnNode):
            pass

        return root
