var_types = ['bool', 'char', 'int', 'float', 'double', 'string', 'void']
libs = ['<iostream>']
namespaces = ['std']
ignore = ['#include', 'using', 'namespace'] + libs + namespaces
key_words = ['for', 'while', 'continue', 'break', 'if', 'else', 'switch', 'case', 'return', 'cin', 'cout', 'endl',
             'default', 'new', 'true', 'false'] + ignore
operators = ['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '!', '?']
possible_operators = ['==', '!=', '+=', '-=', '*=', '/=', '<<', '>>', '&&', '||', '++', '--']
separators = [';', '{', '}', '(', ')', '[', ']', ',', ':']

all_operators = operators + possible_operators
