from functions.lexer import Lexer
from nodes.nodes_module import *
from entities.constants import all_operators, ignore, libs, namespaces, unary_operators


class Parser:
    def __init__(self, lexer: Lexer):
        self._tokens = lexer.tokens
        self._position = 0

        self._key_words = lexer.key_word_tokens
        self._constants = lexer.constants_tokens.keys()
        self._variable_types = lexer.var_types_tokens
        self._variables = lexer.var_tokens.keys()
        self._functions = lexer.func_tokens.keys()

        self._current_function_type = ''

    def _match(self, expected: []) -> Token:
        if self._position < len(self._tokens):
            current_token = self._tokens[self._position]
            # print(current_token.word, expected, current_token.word in expected)
            if current_token.word in expected:
                self._position += 1
                return current_token

        return None

    def _get_prev(self):
        return self._tokens[self._position - 1].word

    def _require(self, expected):
        token = self._match(expected)
        if token is None:
            raise Exception(f'Expected {expected} after {self._get_prev()}')

        return token

    def _pick(self):
        return self._tokens[self._position].word

    def _parse_variable_or_constant(self) -> Node:
        constant = self._match(self._constants)
        if constant:
            return ConstantNode(constant)

        bool_not = self._match(['!'])
        if bool_not:
            return UnaryOperationNode(bool_not, self._parse_formula())
        var = self._match(self._variables)
        if var:
            var = VariableNode(var)

            bracket = self._match(['['])
            while bracket:
                index = self._parse_formula()
                var = BinaryOperationNode(bracket, var, index)
                self._require([']'])

                bracket = self._match(['['])

            return var

        if self._get_prev() != 'return' and self._current_function_type != 'VOID':
            raise Exception(f'Expected number or variable after {self._get_prev()}')

    def _parse_parentheses(self) -> Node:
        if self._match(['(']):
            node = self._parse_formula()
            self._require([')'])

            return node
        else:
            return self._parse_variable_or_constant()

    def _parse_formula(self) -> Node:
        left_node = self._parse_parentheses()
        operation = self._match(all_operators)

        while operation:
            if operation.word == '<<' or operation.word == '>>':
                self._position -= 1
                break
            elif operation.word in unary_operators:
                left_node = UnaryOperationNode(operation, left_node)
                operation = self._match(all_operators + [':'])
            else:
                right_node = self._parse_parentheses()
                left_node = BinaryOperationNode(operation, left_node, right_node)
                operation = self._match(all_operators + [':'])

        return left_node

    def _parse_array(self):
        self._require(['{'])

        result = []
        while True:
            if self._match(['{']):
                self._position -= 1
                result.append(self._parse_array())
            else:
                result.append(self._parse_formula())

            if self._require([',', '}']).word == '}':
                return result

    def _parse_variable_definition(self, variable_token):
        var = VariableNode(variable_token)
        result = []

        separators = [',', '=', '[', ';', '{']
        s = self._require(separators)
        while s:
            if s.word == '[':
                sizes = []

                bracket = s
                while bracket:
                    size = self._parse_formula()
                    sizes.append(size)
                    self._require([']'])
                    bracket = self._match(['['])

                var = ArrayDefinition(var, sizes)
                result.append(var)
            elif s.word == ',':
                var = VariableNode(self._require(self._variables))
            elif s.word == '=':
                if not isinstance(var, VariableNode):
                    raise Exception(f'Variable {var.variable.variable.word} was declared as an array')

                result.append(BinaryOperationNode(Token('=', 'OPERATION'), var, self._parse_formula()))
            elif s.word == '{':
                if not isinstance(var, ArrayDefinition):
                    raise Exception(f'Variable {var.variable.word} was not declared as an array')

                self._position -= 1
                result.append(BinaryOperationNode(Token('=', 'OPERATION'), result.pop(), Array(self._parse_array())))
            elif s.word == ';':
                return result

            s = self._require(separators)

    def _parse_cin(self):
        expression = []

        operation = self._match(['>>'])
        while operation:
            expression.append(self._parse_formula())
            operation = self._match(['>>'])

        self._require([';'])
        return CinNode(expression)

    def _parse_cout(self):
        expression = []

        operation = self._match(['<<'])
        while operation:
            endl = self._match(['endl'])
            expression.append(KeyWordNode(endl) if endl else self._parse_formula())

            operation = self._match(['<<'])

        self._require([';'])
        return CoutNode(expression)

    def _parse_while(self):
        self._require(['('])
        condition = None
        if self._pick() != ')':
            condition = self._parse_formula()
        self._require([')'])

        self._require(['{'])
        body = self.parse_block()
        self._require(['}'])

        return WhileNode(condition, body)

    def _parse_for(self):
        self._require(['('])
        begin = condition = step = None
        if self._pick() != ';':
            self._match(self._variable_types)
            begin = self._parse_formula()
        self._require([';'])

        if self._pick() != ';':
            condition = self._parse_formula()
        self._require([';'])

        if self._pick() != ')':
            step = self._parse_formula()
        self._require([')'])

        self._require(['{'])
        body = self.parse_block()
        self._require(['}'])

        return ForNode(begin, condition, step, body)

    def _parse_if_else_condition(self):
        self._require(['('])
        condition = self._parse_formula()
        self._require([')'])

        self._require(['{'])
        body = self.parse_block()
        self._require(['}'])

        if self._match(['else']):
            if self._match(['if']):
                else_condition = self._parse_if_else_condition()
            else:
                self._require(['{'])
                else_condition = self.parse_block()
                self._require(['}'])

            return IfNode(condition, body, else_condition)

        return IfNode(condition, body, None)

    def _parse_function_parameters(self, types=False):
        parameters = []

        if self._match([')']):
            self._position -= 1
            return parameters

        if types:
            self._require(self._variable_types)
        parameters.append(self._require(self._variables))

        comma = self._match([','])
        while comma:
            if types:
                self._require(self._variable_types)
            parameters.append(self._require(self._variables))
            comma = self._match([','])

        return parameters

    def _parse_function(self, function_token):
        self._require(['('])
        parameters = self._parse_function_parameters(types=True)
        self._require([')'])

        self._require(['{'])
        body = self.parse_block()
        self._require(['}'])

        if isinstance(body, StatementsNode) and body.nodes:
            return_type = function_token.token_type.split(' ')[0]
            if return_type != 'VOID':
                if not isinstance(body.nodes[-1], ReturnNode):
                    raise Exception(f'Function {function_token.word} has type {return_type} but returns nothing')
            else:
                if isinstance(body.nodes[-1], ReturnNode):
                    if not isinstance(body.nodes[-1].statement, KeyWordNode) and \
                            body.nodes[-1].statement.word.word != 'void':
                        raise Exception(f'Function {function_token.word} has type {return_type} but '
                                        f'has return statement')
                else:
                    body.nodes.append(ReturnNode(KeyWordNode(Token('void', 'VOID RETURN TYPE'))))

        self._current_function_type = function_token.token_type.split()[0]
        return FunctionNode(function_token, parameters, body)

    def _parse_function_call(self, function_token):
        self._require(['('])
        parameters = self._parse_function_parameters()
        self._require([')'])
        self._require([';'])

        return FunctionCallNode(function_token, parameters)

    def _parse_switch(self):
        self._require(['('])
        variable = self._require(self._variables)
        self._require([')'])

        self._require(['{'])
        body = self.parse_block()
        self._require(['}'])

        return SwitchNode(variable, body)

    def _parse_case(self):
        constant = self._parse_variable_or_constant()
        self._require([':'])

        return CaseNode(constant.constant)

    def _parse_key_word(self, key_word):
        self._require([':'] if key_word.word == 'default' else [';'])

        return KeyWordNode(key_word)

    def _parse_ignored_keywords(self, key_word):
        if key_word.word == '#include':
            self._require(libs)
        elif key_word.word == 'using':
            self._require(['namespace'])
            self._require(namespaces)
            self._require([';'])

        return None

    def _parse_return(self):
        statement = self._parse_formula()
        if not statement:
            statement = KeyWordNode(Token('void', 'VOID RETURN TYPE'))
        self._require([';'])

        return ReturnNode(statement)

    def _parse_expression(self) -> Node:
        key_word = self._match(self._key_words)
        if key_word:
            if key_word.word in ignore:
                return self._parse_ignored_keywords(key_word)
            elif key_word.word == 'case':
                return self._parse_case()
            elif key_word.word == 'default':
                return self._parse_key_word(key_word)
            elif key_word.word == 'cin':
                return self._parse_cin()
            elif key_word.word == 'cout':
                return self._parse_cout()
            elif key_word.word == 'for':
                return self._parse_for()
            elif key_word.word == 'if':
                return self._parse_if_else_condition()
            elif key_word.word == 'switch':
                return self._parse_switch()
            elif key_word.word == 'continue':
                return self._parse_key_word(key_word)
            elif key_word.word == 'break':
                return self._parse_key_word(key_word)
            elif key_word.word == 'while':
                return self._parse_while()
            elif key_word.word == 'return':
                return self._parse_return()

        if self._match(self._variables):
            self._position -= 1  # current position is variable
            var_node = self._parse_variable_or_constant()

            operation = self._match(all_operators)
            if operation:
                if operation.word in unary_operators:
                    self._require([';'])
                    return UnaryOperationNode(operation, var_node)
                right_formula_node = self._parse_formula()
                self._require([';'])
                return BinaryOperationNode(operation, var_node, right_formula_node)

        function_token = self._match(self._functions)
        if function_token:
            return self._parse_function_call(function_token)

        if self._match(self._variable_types):
            variable_token = self._match(self._variables)
            if variable_token:
                return self._parse_variable_definition(variable_token)

            function_token = self._match(self._functions)
            if function_token:
                return self._parse_function(function_token)

            raise Exception(f'Expected variable or function after {self._get_prev()}')

        if self._match(self._constants):
            raise Exception(f'Unexpected constant')

    def parse_block(self) -> Node:  # block parse
        root = StatementsNode()
        while self._position < len(self._tokens):
            if self._match(['}']):
                self._position -= 1

                return root

            code_string_node = self._parse_expression()
            if code_string_node:
                if isinstance(code_string_node, list):
                    for node in code_string_node:
                        root.add_node(node)
                else:
                    root.add_node(code_string_node)

        return root
