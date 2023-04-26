from functions.lexer import Lexer
from functions.parser import Parser
from functions.semantic import Semantic
from entities.print import PrintClass
from nodes.nodes_module import *
from entities.constants import execute_command


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

    def _translate_statement(self, node, depth):
        result = ''
        for entity in node.nodes:
            result += depth * '\t' + f'{self._create_code(entity, depth)}\n'

        return result[:-1]

    def _translate_binary_operation(self, node):
        left = self._create_code(node.left_node)
        right = self._create_code(node.right_node)

        operation = node.operation.word
        if operation == '&&':
            operation = 'and'
        elif operation == '||':
            operation = 'or'

        if isinstance(node.left_node, BinaryOperationNode):
            left = '(' + left + ')'
        if isinstance(node.right_node, BinaryOperationNode):
            right = '(' + right + ')'

        return f'{left} {operation} {right}'

    def _translate_key_word(self, node):
        if node.word.word == 'endl':
            return '"\\n"'

    def _translate_cin(self, node):
        expression = f'{self._create_code(node.expression[0])}'
        data_type = node.expression[0].variable.token_type.split()[0].lower()
        inputs = 'input()' if data_type != 'int' and data_type != 'float' else f'{data_type}(input())'
        for var in node.expression[1:]:
            expression += f', {self._create_code(var)}'
            data_type = var.variable.token_type.split()[0].lower()
            inputs += ', input()' if data_type != 'int' and data_type != 'float' else f', {data_type}(input())'

        return expression + ' = ' + inputs

    def _translate_cout(self, node):
        expression = f'print({self._create_code(node.expression[0])}'
        for val in node.expression[1:]:
            expression += f', {self._create_code(val)}'

        return expression + ')'

    def _translate_while(self, node, depth):
        result = '\t' * depth + f'while({self._create_code(node.condition)}):\n'
        result += self._create_code(node.body, depth + 1)

        return result

    def _translate_for(self, node, depth):
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

        return f'for {variable} in range({loop_range}, {step}):\n' + self._create_code(node.body, depth + 1)

    def _translate_if_condition(self, node, depth):
        result = f'if {self._create_code(node.condition)}:\n'
        result += self._create_code(node.body, depth + 1)

        if node.else_condition:
            statement = self._create_code(node.else_condition, depth)

            word = ''
            for i in range(2):
                word += statement[i]
            if word == 'if':
                statement = '\t' * depth + 'elif' + statement[2:]
            else:
                new_statement = ''
                for s in statement.split('\n'):
                    new_statement += f'\t{s}\n'

                statement = '\t' * depth + 'else:\n' + new_statement

            result += f'\n{statement}'
        return result

    def _translate_function(self, node, depth):
        result = f'def {node.name.word}('
        if node.parameters:
            for p in node.parameters:
                result += f'{self._create_code(p)}, '
            result = result[:-2]
        result += '):\n' + self._create_code(node.body, depth + 1)
        return result

    def _translate_function_call(self, node):
        result = f'{node.name.word}('
        if node.parameters:
            for p in node.parameters:
                result += f'{self._create_code(p)}, '
            result = result[:-2]
        result += ')'
        return result

    def _translate_return(self, node):
        if isinstance(node.statement, Token) and node.statement.word == 'void':
            statement = ''
        else:
            statement = self._create_code(node.statement)
        return 'return ' + (statement if statement else '')

    def _create_code(self, node, depth=0):
        if isinstance(node, Token):
            return node.word
        if isinstance(node, StatementsNode):
            return self._translate_statement(node, depth)
        elif isinstance(node, UnaryOperationNode):
            pass
        elif isinstance(node, BinaryOperationNode):
            return self._translate_binary_operation(node)
        elif isinstance(node, VariableNode):
            return node.variable.word
        elif isinstance(node, ConstantNode):
            return node.constant.word
        elif isinstance(node, KeyWordNode):
            return self._translate_key_word(node)
        elif isinstance(node, CinNode):
            return self._translate_cin(node)
        elif isinstance(node, CoutNode):
            return self._translate_cout(node)
        elif isinstance(node, WhileNode):
            return self._translate_while(node, depth)
        elif isinstance(node, ForNode):
            return self._translate_for(node, depth)
        elif isinstance(node, IfNode):
            return self._translate_if_condition(node, depth)
        elif isinstance(node, FunctionNode):
            return self._translate_function(node, depth)
        elif isinstance(node, FunctionCallNode):
            return self._translate_function_call(node)
        elif isinstance(node, SwitchNode):
            pass
        elif isinstance(node, CaseNode):
            pass
        elif isinstance(node, ArrayDefinition):
            pass
        elif isinstance(node, Array):
            pass
        elif isinstance(node, ReturnNode):
            return self._translate_return(node)

    def execute(self):
        exec(self._create_code(self.tree) + execute_command)
