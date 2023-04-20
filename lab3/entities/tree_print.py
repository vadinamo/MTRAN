from nodes.nodes_module import *


def get_tree_list(node: Node):
    tree = []

    if not node:
        return

    if isinstance(node, StatementsNode):
        for n in node.nodes:
            tree.append(get_tree_list(n))
    elif isinstance(node, BinaryOperationNode):
        tree.append(get_tree_list(node.left_node))
        tree.append(node.operation.word)
        tree.append(get_tree_list(node.right_node))
    elif isinstance(node, VariableNode):
        tree.append(node.variable.word)
    elif isinstance(node, ConstantNode):
        tree.append(node.constant.word)
    elif isinstance(node, KeyWordNode):
        tree.append(node.word.word)
    elif isinstance(node, CinNode):
        tree.append('cin')
        result = []
        for e in node.expression:
            result.append(get_tree_list(e))
        tree.append(result)
    elif isinstance(node, CoutNode):
        tree.append('cout')
        result = []
        for e in node.expression:
            result.append(get_tree_list(e))
        tree.append(result)
    elif isinstance(node, WhileNode):
        tree.append('while')
        tree.append(get_tree_list(node.condition))
        tree.append(get_tree_list(node.body))


    if len(tree) > 1:
        return tree

    return tree[0]


def print_tree(node, level=0):
    if isinstance(node, list):
        for child in node:
            print_tree(child, level + 1)
    else:
        print("  " * level + str(node))