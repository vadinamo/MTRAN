from lexer.functions import *
from entities.constants import *
from entities.token import Token


def get_tokens(path):
    code = get_file(path)

    var_tokens = {}
    constants = {}
    var_types_tokens = []
    key_word_tokens = []
    operator_tokens = []

    tokens = []

    current = ''
    string_read = False
    char_read = False

    row, column = 1, 1
    for s in code:
        if not is_control_character(s) and s not in separators and s not in operators and (
                s != ' ' or string_read or char_read):
            if s == '"' and not char_read:
                string_read = not string_read
            elif s == "'" and not string_read:
                char_read = not char_read

            current += s

        else:
            if current in var_types:
                var_types_tokens.append(current)
                tokens.append(Token(current, 'VARIABLE TYPE'))
                current = ''
            elif current in key_words:
                key_word_tokens.append(current)
                tokens.append(Token(current, 'KEY WORD'))
                current = ''
            elif (s == '<' or s == '>') and tokens[-1].word == '#include':
                current += s
        if s == '\n':
            row += 1
            column = 1
        else:
            column += 1

    return tokens
