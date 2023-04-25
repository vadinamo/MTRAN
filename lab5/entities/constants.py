var_types = ['bool', 'char', 'int', 'float', 'string', 'void']
libs = ['<iostream>']
namespaces = ['std']
ignore = ['#include', 'using', 'namespace'] + libs + namespaces
booleans = ['true', 'false']
key_words = ['for', 'while', 'continue', 'break', 'if', 'else', 'switch', 'case', 'return', 'cin', 'cout', 'endl',
             'default', 'new'] + ignore

operators = ['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '!', '?']
possible_operators = ['==', '!=', '+=', '-=', '*=', '/=', '<<', '>>', '&&', '||', '++', '--', '<=', '>=']
string_operators = ['==', '!=', '+=', '=']
unary_operators = ['++', '--']
all_operators = operators + possible_operators

separators = [';', '{', '}', '(', ')', '[', ']', ',', ':']

logical_operators = ['<', '>', '&&', '||', '==', '!=', '<=', '>=']
calculation_operators = ['+', '-', '*', '/', '%', '=', '+=', '-=', '*=', '/=']
