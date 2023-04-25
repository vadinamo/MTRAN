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

    def is_numeric(self, first_type, second_type='INT'):
        numeric = ['INT', 'FLOAT']
        return first_type in numeric and second_type in numeric

    def analyze(self, root):
        if root is None:
            return None
        if isinstance(root, Token):
            return self.get_type(root.token_type)
        elif isinstance(root, list):
            for element in root:
                self.analyze(element)
            return
        elif isinstance(root, StatementsNode):
            for node in root.nodes:
                self.analyze(node)
            return
        elif isinstance(root, UnaryOperationNode):
            left = root.node
            operation = root.operation
            if operation.word in unary_operators:
                if not isinstance(left, VariableNode):
                    raise Exception('++ and -- available only for variables')
                else:
                    left_type = self.get_type(left.variable.token_type)
                    if not self.is_numeric(left_type[0]):
                        raise Exception('++ and -- available only for numeric variables')

                    return left_type[0], left_type[1]
            elif operation.word == '!':
                left = self.analyze(left)
                if left[0] != 'BOOLEAN':
                    raise Exception('Cannot use ! operator with non BOOLEAN condition')

                return ['BOOLEAN', 'STATEMENT']
        elif isinstance(root, BinaryOperationNode):
            left = self.analyze(root.left_node)
            right = self.analyze(root.right_node)
            operation = root.operation.word

            if operation in logical_operators:
                return ['BOOLEAN', 'STATEMENT']
            elif left[0] == 'STRING' and right[0] == 'STRING':
                if operation in string_operators:
                    return left[0], left[1]
                raise Exception('Only + available for STRING values')
            elif left[0] == 'BOOLEAN' and right[0] == 'BOOLEAN':
                if operation == '||' and operation == '&&':
                    return left[0], left[1]
                raise Exception('Only || or && available for BOOLEAN values')
            elif left[0] != right[0]:
                raise Exception(f'Cannot solve {left[0]} and {right[0]} types')
            elif self.is_numeric(left[0], right[0]):
                return left[0], left[1]

            return left[0], left[1]
        elif isinstance(root, VariableNode):
            return self.analyze(root.variable)
        elif isinstance(root, ConstantNode):
            return self.analyze(root.constant)
        elif isinstance(root, KeyWordNode):
            return
        elif isinstance(root, CinNode):
            self.analyze(root.expression)
            return
        elif isinstance(root, CoutNode):
            self.analyze(root.expression)
            return
        elif isinstance(root, WhileNode):
            if root.condition and self.analyze(root.condition)[0] != 'BOOLEAN':
                raise Exception('Invalid WHILE condition')
            self.analyze(root.body)
            return
        elif isinstance(root, ForNode):
            if root.begin:
                begin = self.analyze(root.begin)

            if root.condition:
                condition = self.analyze(root.condition)
                if self.analyze(root.condition)[0] != 'BOOLEAN':
                    raise Exception('Invalid FOR condition')

            if root.step:
                step = self.analyze(root.step)
            self.analyze(root.body)

            return
        elif isinstance(root, IfNode):
            if self.analyze(root.condition)[0] != 'BOOLEAN':
                raise Exception('Invalid IF condition')
            self.analyze(root.body)
            self.analyze(root.else_condition)

            return
        elif isinstance(root, FunctionNode):
            self.analyze(root.body)

            return
        elif isinstance(root, FunctionCallNode):
            return self.get_type(root.name.token_type)
        elif isinstance(root, SwitchNode):
            pass
        elif isinstance(root, CaseNode):
            pass
        elif isinstance(root, ArrayDefinition):
            for size in root.sizes:
                if self.analyze(size)[0] != 'INT':
                    raise Exception('Only INT can be array size')

            return
        elif isinstance(root, Array):
            self.analyze(root.elements)

            return
        elif isinstance(root, ReturnNode):
            return

        return root
