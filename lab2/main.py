from tkinter import filedialog
from functions import *
from constants import *


def get_file():
    filetypes = (
        ('C++ files', '*.cpp'),
    )
    path = filedialog.askopenfilename(filetypes=filetypes)
    with open(path, 'r') as f:
        data = f.read()

    return data


def main():
    lines = get_file().split('\n')
    var_tokens = {}

    integer_tokens = []
    float_tokens = []
    string_tokens = []

    var_types_tokens = []
    key_word_tokens = []
    operator_tokens = []

    errors = []

    for row in range(len(lines)):
        current = ''
        prev_var_type = ''
        prev_is_operator = False
        string_started = False
        for column in range(len(lines[row])):
            s = lines[row][column]
            if column == len(lines[row]) - 1 and not (
                    whitespace_check(s)
                    or s in brackets.keys() or s in brackets.values()
                    or s == ',' or s == '"' or s == ":"):
                current += s

            if string_started or s == '"':
                current += s
                if s == '"':
                    if not string_started:
                        string_started = True
                    else:
                        prev_is_operator = False
                        string_started = False
                        string_tokens.append(current)
                        current = ''
            elif whitespace_check(s) or s in brackets.keys() or s in brackets.values() or s == ',' or column == len(
                    lines[row]) - 1:
                if current in var_types:
                    var_types_tokens.append(current)
                    prev_var_type = current
                    if prev_is_operator:
                        prev_is_operator = False
                        errors.append(operator_error(current, lines[row], row, column))
                elif current in key_words:
                    key_word_tokens.append(current)
                    if prev_is_operator and current != 'endl':
                        prev_is_operator = False
                        errors.append(operator_error(current, lines[row], row, column))
                elif current in operators:
                    operator_tokens.append(current)
                    if prev_is_operator:
                        errors.append(operator_error(current, lines[row], row, column))
                    prev_is_operator = True
                elif is_int(current):
                    integer_tokens.append(current)
                    prev_is_operator = False
                elif is_float(current):
                    float_tokens.append(current)
                    prev_is_operator = False
                elif current in functions:
                    prev_is_operator = False
                elif current in var_tokens:
                    prev_is_operator = False
                elif current != '':
                    prev_is_operator = False
                    if prev_var_type != '':
                        if current[0] == '_' or current[0].isalpha():
                            var_tokens[current] = prev_var_type
                        else:
                            errors.append(var_name_error(lines[row], row, column))

                        if column > len(lines[row]) - 1 and lines[row][column + 1:].strip()[0] != ',':
                            prev_var_type = ''
                    elif current != ':':
                        errors.append(lexical_error(current, lines[row], row, column))
                current = ''
            else:
                current += s

    result = bracket_check(lines)
    if result:
        errors.append(result)

    token_output('KEY WORDS', set(key_word_tokens))
    token_output('INTEGER CONSTANTS', integer_tokens)
    token_output('FLOAT CONSTANTS', float_tokens)
    token_output('STRING CONSTANTS', string_tokens)
    token_output('OPERATORS', set(operator_tokens))
    token_output('VARIABLE TYPES', set(var_types_tokens))
    token_output('VARIABLES', var_tokens)
    token_output('ERRORS', errors)


if __name__ == '__main__':
    main()
