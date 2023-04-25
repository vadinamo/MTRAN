from functions.lexer import Lexer
from functions.parser import Parser
from functions.semantic import Semantic
from entities.print import PrintClass
from nodes.nodes_module import *


class Translator:
    def __init__(self, path):
        printer = PrintClass()

        lexer = Lexer()
        tokens = lexer.get_tokens(path)
        printer.print_tokens(tokens)

        parser = Parser(lexer)
        tree = parser.parse_block()
        printer.print_tree(tree)

        semantic = Semantic()
        semantic.analyze(tree)

        printer.print_code(self._create_code(tree))
        self.tree = tree
        self.execute()

    def _create_code(self, node, depth=0):
        if isinstance(node, Token):
            return node.word
        if isinstance(node, StatementsNode):
            result = ''
            for entity in node.nodes:
                result += depth * '\t' + f'{self._create_code(entity)}\n'

            return result[:-1]
        elif isinstance(node, UnaryOperationNode):
            pass
        elif isinstance(node, BinaryOperationNode):
            left = self._create_code(node.left_node)
            operation = node.operation.word
            right = self._create_code(node.right_node)

            if isinstance(node.left_node, BinaryOperationNode):
                left = '(' + left + ')'
            if isinstance(node.right_node, BinaryOperationNode):
                right = '(' + right + ')'

            return f'{left} {operation} {right}'
        elif isinstance(node, VariableNode):
            return node.variable.word
        elif isinstance(node, ConstantNode):
            return node.constant.word
        elif isinstance(node, KeyWordNode):
            if node.word.word == 'endl':
                return '"\\n"'
        elif isinstance(node, CinNode):
            expression = f'{self._create_code(node.expression[0])}'
            data_type = node.expression[0].variable.token_type.split()[0].lower()
            inputs = 'input()' if data_type != 'int' and data_type != 'float' else f'{data_type}(input())'
            for var in node.expression[1:]:
                expression += f', {self._create_code(var)}'
                data_type = var.variable.token_type.split()[0].lower()
                inputs += ', input()' if data_type != 'int' and data_type != 'float' else f', {data_type}(input())'

            return expression + ' = ' + inputs
        elif isinstance(node, CoutNode):
            expression = f'print({self._create_code(node.expression[0])}'
            for val in node.expression[1:]:
                expression += f', {self._create_code(val)}'

            return expression + ')'
        elif isinstance(node, WhileNode):
            result = '\t' * depth + f'while({self._create_code(node.condition)}):\n'
            result += self._create_code(node.body, depth + 1)

            return result
        elif isinstance(node, ForNode):
            if not node.begin:
                result = '\t' * depth + f'while(True):\n'
                result += self._create_code(node.body, depth + 1)

                return result

            if isinstance(node.begin, BinaryOperationNode):
                variable = f'{node.begin.left_node.variable.word}'
                begin = node.begin.right_node.constant.word
            else:
                raise Exception('Invalid FOR variable define')

            if isinstance(node.condition, BinaryOperationNode):
                operation = node.condition.operation.word
                end = self._create_code(node.condition.right_node)
                if operation == '<':
                    loop_range = f'{begin}, {end}'
                elif operation == '<=':
                    loop_range = f'{begin}, {end} + 1'
                elif operation == '>':
                    loop_range = f'{end}, {begin}'
                elif operation == '>=':
                    loop_range = f'{end}, {begin} - 1'
                else:
                    raise Exception('Invalid FOR condition define')
            else:
                raise Exception('Invalid FOR condition define')

            if isinstance(node.step, UnaryOperationNode):
                step = '-1' if node.step.operation.word == '--' else '1'
            elif isinstance(node.step, BinaryOperationNode) and node.step.operation == '+=':
                step = self._create_code(node.step.right_node)
            elif isinstance(node.step, BinaryOperationNode) and node.step.operation == '-=':
                step = f'-{self._create_code(node.step.right_node)}'
            else:
                raise Exception('Invalid FOR step define')

            return f'for {variable} in range({loop_range}, {step}):\n' + self._create_code(node.body, depth+1)

        elif isinstance(node, IfNode):
            pass
        elif isinstance(node, FunctionNode):
            pass
        elif isinstance(node, FunctionCallNode):
            pass
        elif isinstance(node, SwitchNode):
            pass
        elif isinstance(node, CaseNode):
            pass
        elif isinstance(node, ArrayDefinition):
            pass
        elif isinstance(node, Array):
            pass
        elif isinstance(node, ReturnNode):
            pass

    def execute(self):
        exec(self._create_code(self.tree))
