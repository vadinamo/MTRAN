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
    result = bracket_check(lines)
    if result:
        errors.append(result)

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

    print('-' * 10 + 'VARIABLES' + '-' * 10)
    for key in var_tokens.keys():
        print(f'{key}: {var_tokens[key]}')
    whitespaces()
    print('-' * 10 + 'INTEGERS' + '-' * 11)
    for token in integer_tokens:
        print(token)
    whitespaces()
    print('-' * 11 + 'FLOATS' + '-' * 12)
    for token in float_tokens:
        print(token)
    whitespaces()
    print('-' * 11 + 'STRINGS' + '-' * 11)
    for token in string_tokens:
        print(token)
    whitespaces()
    print('-' * 7 + 'VARIABLE TYPES' + '-' * 8)
    for token in var_types_tokens:
        print(token)
    whitespaces()
    print('-' * 10 + 'KEY WORDS' + '-' * 10)
    for token in key_word_tokens:
        print(token)
    whitespaces()
    print('-' * 10 + 'OPERATORS' + '-' * 10)
    for token in operator_tokens:
        print(token)
    whitespaces()

    print('-' * 11 + 'ERRORS' + '-' * 12)
    for error in errors:
        print(error)
    whitespaces()


if __name__ == '__main__':
    main()
