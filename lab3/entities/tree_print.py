from nodes.nodes_module import *


def get_tree_list(node: Node):
    tree = []

    if not node:
        return

    if isinstance(node, StatementsNode):
        for n in node.nodes:
            tree.append(get_tree_list(n))
    elif isinstance(node, UnaryOperationNode):
        tree.append(get_tree_list(node.node))
        tree.append(node.operation.word)
    elif isinstance(node, BinaryOperationNode):
        tree.append(get_tree_list(node.left_node))
        tree.append(node.operation.word)
        tree.append(get_tree_list(node.right_node))
    elif isinstance(node, VariableNode):
        tree.append(node.variable.word)
    elif isinstance(node, ConstantNode):
        tree.append(node.constant.word)
    elif isinstance(node, KeyWordNode):
        tree.append([node.word.word])
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
    elif isinstance(node, ForNode):
        tree.append('for')
        tree.append(get_tree_list(node.begin))
        tree.append(get_tree_list(node.condition))
        tree.append(get_tree_list(node.step))
        tree.append(get_tree_list(node.body))
    elif isinstance(node, IfNode):
        tree.append('if')
        tree.append(get_tree_list(node.condition))
        tree.append(get_tree_list(node.body))
        tree.append('else')
        tree.append(get_tree_list(node.else_condition))
    elif isinstance(node, FunctionNode):
        tree.append(node.name.word)
        for p in node.parameters:
            tree.append([p.word])
        tree.append([get_tree_list(node.body)])
    elif isinstance(node, FunctionCallNode):
        tree.append(node.name.word)
        for p in node.parameters:
            tree.append([p.word])
    elif isinstance(node, SwitchNode):
        tree.append('switch')
        tree.append(node.variable.word)
        tree.append(get_tree_list(node.body))
    elif isinstance(node, CaseNode):
        tree.append('case')
        tree.append(node.variable.word)

    if len(tree) > 1:
        return tree

    return tree[0]


def print_tree(node, level=0):
    if isinstance(node, list):
        for child in node:
            print_tree(child, level + 1)
    else:
        print("  " * level + str(node))
