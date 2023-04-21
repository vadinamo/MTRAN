var_types = ['bool', 'char', 'int', 'float', 'double', 'string', 'void']
ignore = ['#include', '<iostream>', 'using', 'namespace', 'std']
key_words = ['for', 'while', 'continue', 'break', 'if', 'else', 'switch', 'case', 'return', 'cin', 'cout', 'endl',
             'default', 'new', 'true', 'false'] + ignore
operators = ['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '!']
possible_operators = ['==', '!=', '+=', '-=', '*=', '/=', '<<', '>>', '&&', '||', '++', '--']
separators = [';', '{', '}', '(', ')', '[', ']', ',', ':']

all_operators = operators + possible_operators
