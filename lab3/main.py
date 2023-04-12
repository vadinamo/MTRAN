from lexer.lexer_main import get_tokens

tokens = get_tokens('/Users/vadinamo/Downloads/main.cpp')
max_length = max(len(t.word + t.token_type) for t in tokens)
for t in tokens:
    print(t.token_type + ' ' * (max_length - len(t.word + t.token_type)) + t.word)