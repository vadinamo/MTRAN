from nodes.nodes_module import *
from math import ceil, floor


class PrintClass:
    def __init__(self):
        self.string_length = 40

    def _print_name(self, name):
        length = self.string_length - len(name)
        print('-' * ceil(length / 2) + name + '-' * floor(length / 2))

    def _get_tree_list(self, node):
        tree = []
        if node is None:
            return

        if isinstance(node, Token):
            return node.word
        elif isinstance(node, list):
            for n in node:
                tree.append([self._get_tree_list(n)])
        elif isinstance(node, StatementsNode):
            for n in node.nodes:
                tree.append(self._get_tree_list(n))
        elif isinstance(node, UnaryOperationNode):
            tree.append(self._get_tree_list(node.node))
            tree.append(node.operation.word)
        elif isinstance(node, BinaryOperationNode):
            tree.append(self._get_tree_list(node.left_node))
            tree.append(node.operation.word)
            tree.append(self._get_tree_list(node.right_node))
        elif isinstance(node, VariableNode):
            tree.append(node.variable.word)
        elif isinstance(node, ConstantNode):
            tree.append(node.constant.word)
        elif isinstance(node, KeyWordNode):
            tree.append(node.word.word)
        elif isinstance(node, CinNode):
            tree.append('cin')
            result = []
            tree.append(self._get_tree_list(node.expression))
            tree.append(result)
        elif isinstance(node, CoutNode):
            tree.append('cout')
            result = []
            tree.append(self._get_tree_list(node.expression))
            tree.append(result)
        elif isinstance(node, WhileNode):
            tree.append('while')
            tree.append(self._get_tree_list(node.condition))
            tree.append(self._get_tree_list(node.body))
        elif isinstance(node, ForNode):
            tree.append('for')
            tree.append(self._get_tree_list(node.begin))
            tree.append(self._get_tree_list(node.condition))
            tree.append(self._get_tree_list(node.step))
            tree.append(self._get_tree_list(node.body))
        elif isinstance(node, IfNode):
            tree.append('if')
            tree.append(self._get_tree_list(node.condition))
            tree.append(self._get_tree_list(node.body))

            if node.else_condition:
                tree.append('else')
                tree.append(self._get_tree_list(node.else_condition))
        elif isinstance(node, FunctionNode):
            tree.append('function')
            tree.append(node.name.word)
            tree.append(self._get_tree_list(node.parameters))
            tree.append([self._get_tree_list(node.body)])
        elif isinstance(node, FunctionCallNode):
            tree.append(node.name.word)
            tree.append(self._get_tree_list(node.parameters))
        elif isinstance(node, SwitchNode):
            tree.append('switch')
            tree.append(node.variable.word)
            tree.append(self._get_tree_list(node.body))
        elif isinstance(node, CaseNode):
            tree.append('case')
            tree.append(node.variable.word)
        elif isinstance(node, ArrayDefinition):
            tree.append(node.variable.variable.word)
            tree.append('size:')
            tree.append(self._get_tree_list(node.sizes))
        elif isinstance(node, Array):
            tree.append(self._get_tree_list(node.elements))
        elif isinstance(node, ReturnNode):
            tree.append('return')
            tree.append([self._get_tree_list(node.statement)])

        if len(tree) == 0 or len(tree) > 1:
            return tree

        return tree[0]

    def _print_node(self, node, level=0):
        if isinstance(node, list):
            for child in node:
                self._print_node(child, level + 1)
        else:
            print("  " * level + str(node))

    def print_tokens(self, tokens):
        self._print_name('TOKEN LIST')
        max_length = self.string_length
        for t in tokens:
            print(t.token_type + ' ' * (max_length - len(t.word + t.token_type)) + t.word)
        self._print_name('-' * self.string_length)

    def print_tree(self, root):
        self._print_name('ABSTRACT SYNTAX TREE')
        self._print_node(self._get_tree_list(root))
        self._print_name('-' * self.string_length)

    def print_code(self, code):
        self._print_name('ABSTRACT SYNTAX TREE')
        print(code)
        self._print_name('-' * self.string_length)
