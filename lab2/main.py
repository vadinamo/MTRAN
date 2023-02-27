from tkinter import filedialog
from brace_check import *

var_types = ['bool', 'char', 'int', 'float', 'double', 'string']
key_words = ['#include', '<iostream>', '<math.h>', 'using', 'namespace',
             'std', 'for', 'while', 'do', 'continue', 'break',
             'if', 'else', 'switch', 'case', 'return',
             'cin', 'cout']
operators = ['+', '-', '*', '/', '%', '=', '==', '+=', '<<', '>>', '<', '>', '&&', '||', '&', '|']
functions = ['main', 'factorial', 'pow', 'abs']


def get_file():
    filetypes = (
        ('C++ files', '*.cpp'),
    )
    path = filedialog.askopenfilename(filetypes=filetypes)
    with open(path, 'r') as f:
        data = f.read()

    return data


def is_int(number_str):
    if not number_str:
        return False
    if not (number_str.isdigit() or (number_str[0] == '-' and number_str[1:].isdigit())):
        return False
    number = int(number_str)
    return number_str == str(number)


def is_float(number_str):
    if not number_str:
        return False
    try:
        float(number_str)
    except ValueError:
        return False
    return not (is_int(number_str) or (number_str[0] == '-' and is_int(number_str[1:])))


def whitespaces():
    print(29 * '-')


def whitespace_check(symbol):
    return symbol == ' ' or symbol == '\t' or symbol == ';'


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
                    or s == ',' or s == '"'):
                current += s

            if string_started or s == '"':
                current += s
                if s == '"':
                    if not string_started:
                        string_started = True
                    else:
                        string_started = False
                        string_tokens.append(current)
                        current = ''
            elif whitespace_check(s) or \
                    s in brackets.keys() or s in brackets.values() or \
                    s == ',' or column == len(lines[row]) - 1:
                if current in var_types:
                    var_types_tokens.append(current)
                    prev_var_type = current
                    if prev_is_operator:
                        prev_is_operator = False
                        errors.append(f'{row}, {column} Lexical error, unexpected {current} after operator:\n'
                                      f'{row}: {lines[row]}\n'
                                      f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                elif current in key_words:
                    key_word_tokens.append(current)
                    if prev_is_operator:
                        prev_is_operator = False
                        errors.append(f'{row}, {column} Lexical error, unexpected {current} after operator:\n'
                                      f'{row}: {lines[row]}\n'
                                      f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                elif current in operators:
                    operator_tokens.append(current)
                    if prev_is_operator:
                        errors.append(f'{row}, {column} Lexical error, unexpected {current} after operator:\n'
                                      f'{row}: {lines[row]}\n'
                                      f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
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
                            errors.append(
                                f'{row}, {column} Lexical error, var name should start with letter or _:\n'
                                f'{row}: {lines[row]}\n'
                                f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                        prev_var_type = ''
                    else:
                        errors.append(f'{row}, {column} Lexical error, unexpected {current}:\n'
                                      f'{row}: {lines[row]}\n'
                                      f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
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
