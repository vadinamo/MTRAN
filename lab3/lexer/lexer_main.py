from lexer.functions import *
from entities.constants import *
from entities.token import Token


def get_tokens(path):
    code = get_file(path)

    var_tokens = {}
    constants = {}
    var_types_tokens = []
    key_word_tokens = []

    tokens = []

    space = False
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
            elif len(current) > 0 and current[0] == '"' and current[-1] == '"':
                constants[current] = 'STRING CONSTANT'
                tokens.append(Token(current, 'STRING CONSTANT'))
                current = ''
            elif len(current) > 0 and current[0] == "'" and current[-1] == "'":
                constants[current] = 'CHAR CONSTANT'
                tokens.append(Token(current, 'CHAR CONSTANT'))
                current = ''
            elif is_int(current):
                if not space and len(tokens) > 0 and (tokens[-1].word == '+' or tokens[-1].word == '-'):
                    current = tokens[-1].word + current
                tokens[-1] = Token(current, 'INT CONSTANT')
                current = ''
            elif is_float(current):
                if not space and len(tokens) > 0 and (tokens[-1].word == '+' or tokens[-1].word == '-'):
                    current = tokens[-1].word + current
                tokens[-1] = Token(current, 'FLOAT CONSTANT')
                current = ''
            elif is_valid_variable_name(current):
                var_type = ''
                for token in reversed(tokens):
                    if token.word != ',' and token.word in separators:  # not find
                        break
                    elif token.word in var_types:  # find a var type
                        var_type = token.word
                        break

                if len(var_type) > 0 and current in var_tokens.keys():
                    raise Exception('redefinition')
                else:
                    if current not in var_tokens.keys():
                        var_tokens[current] = var_type
                    tokens.append(Token(current, 'VARIABLE'))
                    current = ''


            if not char_read and not string_read:
                if not is_control_character(s) and s != ' ':
                    if s in separators:
                        tokens.append(Token(s, 'SEPARATOR'))
                        current = ''
                    elif space and s in operators and not ((s == '<' or s == '>') and tokens[-1].word == '#include'):
                        temp = s
                        if not space and len(tokens) > 0 and tokens[-1].word in operators + possible_operators:
                            temp = tokens[-1].word + s
                            if temp not in possible_operators:
                                raise Exception('jopa')
                            tokens.pop()

                        tokens.append(Token(temp, 'OPERATOR'))
                        current = ''
                    space = False
                else:
                    space = True
            else:
                current += s

        if s == '\n':
            row += 1
            column = 1
        else:
            column += 1
    return tokens
