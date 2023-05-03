var_types = ['bool', 'char', 'int', 'float', 'string', 'void']
cast_var_types = {
    'bool': 'bool',
    'char': 'str',
    'int': 'int',
    'float': 'float',
    'string': 'str',
    'void': ''
}
libs = ['<iostream>']
namespaces = ['std']
ignore = ['#include', 'using', 'namespace'] + libs + namespaces
booleans = ['true', 'false']
key_words = ['for', 'while', 'continue', 'break', 'if', 'else', 'switch', 'case', 'return', 'cin', 'cout', 'endl',
             'default', 'new'] + ignore

operators = ['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '!', '?']
possible_operators = ['==', '!=', '+=', '-=', '*=', '/=', '<<', '>>', '&&', '||', '++', '--', '<=', '>=']
string_operators = ['==', '!=', '+=', '=', '+']
unary_operators = ['++', '--']
all_operators = operators + possible_operators

separators = [';', '{', '}', '(', ')', '[', ']', ',', ':']

logical_operators = ['<', '>', '&&', '||', '==', '!=', '<=', '>=']
calculation_operators = ['+', '-', '*', '/', '%', '=', '+=', '-=', '*=', '/=']

execute_command = '\n\nmain()'


def empty_array(shape):
    if not shape:
        return None

    if len(shape) == 1:
        return [0] * shape[0]

    return [empty_array(shape[1:]) for _ in range(shape[0])]
