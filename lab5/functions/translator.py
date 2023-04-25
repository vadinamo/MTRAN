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

        self.tree = tree
        self.execute()

    def _create_code(self, node, depth=0):
        if isinstance(node, Token):
            return node.word
        elif isinstance(node, list):
            pass
        elif isinstance(node, StatementsNode):
            result = ''
            for entity in node.nodes:
                result += depth * '\t' + f'{self._create_code(entity)}\n'

            return result
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
            pass
        elif isinstance(node, CinNode):
            pass
        elif isinstance(node, CoutNode):
            pass
        elif isinstance(node, WhileNode):
            pass
        elif isinstance(node, ForNode):
            pass
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
        print(self._create_code(self.tree))
