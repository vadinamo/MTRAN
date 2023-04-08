from lexer.lexer_main import get_tokens

tokens = get_tokens('/Users/vadinamo/Downloads/main.cpp')
for t in tokens:
    print(t.word, t.token_type)