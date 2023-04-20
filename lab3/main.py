from functions.lexer import Lexer
from functions.parser import Parser
from entities.tree_print import print_tree, get_tree_list

lexer = Lexer()
# tokens = lexer.get_tokens('/Users/vadinamo/Downloads/main.cpp')
tokens = lexer.get_tokens('/Users/vadinamo/Downloads/test1.cpp')
max_length = max(len(t.word + t.token_type) for t in tokens) + 1
for t in tokens:
    print(t.token_type + ' ' * (max_length - len(t.word + t.token_type)) + t.word)

lexer.tokens.pop(0)
parser = Parser(lexer)
print_tree(get_tree_list(parser.parse_code()))