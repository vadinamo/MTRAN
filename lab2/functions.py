import math

from constants import var_types, key_words, functions

brackets = {
    '(': ')',
    '{': '}',
    '[': ']'
}


def bracket_check(lines):
    stack = []
    for row in range(len(lines)):
        for column in range(len(lines[row])):
            s = lines[row][column]
            if s in brackets.keys():
                stack.append(s)
            elif s in brackets.values():
                if len(stack) == 0 or brackets[stack[-1]] != s:
                    return f'{row}, {column} Bracket error, expected {brackets[stack[-1]]}\n' \
                           f'{row + 1}: {lines[row]}\n' \
                           f'{" " * (len((row + 1).__str__()) + 1 + column)} ^'
                else:
                    stack.pop()

    if len(stack) != 0:
        return f'{len(lines)}, 0 Bracket error, expected {brackets[stack[-1]]}\n' \
               f'{len(lines)}: {lines[len(lines) - 1]}\n' \
               f'{" " * (len((len(lines) - 1).__str__()) + 1)} ^'

    return True


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
    print(30 * '-')


def whitespace_check(symbol):
    return symbol == ' ' or symbol == '\t' or symbol == ';'


def operator_error(current, line, row, column):
    return (f'{row}, {column} Lexical error, unexpected "{current}" after operator:\n'
            f'{row}: {line}\n'
            f'{" " * (len((row + 1).__str__()) + 1 + column)}^')


def var_name_error(line, row, column):
    return (f'{row}, {column} Lexical error, var name should start with letter or _:\n'
            f'{row}: {line}\n'
            f'{" " * (len((row + 1).__str__()) + 1 + column)}^')


def lexical_error(current: str, line, row, column):
    mean = ''
    for value in var_types + key_words + functions:
        if current.__contains__(value):
            mean = f', maybe you mean "{value}"'
            break
    return (f'{row}, {column} Lexical error, unexpected "{current}"{mean if mean != "" else ""}:\n'
            f'{row}: {line}\n'
            f'{" " * (len((row + 1).__str__()) + 1 + column)}^')


def token_output(name: str, token_collection):
    length = 30 - len(name)
    print('-' * math.floor(length / 2) + name.upper() + '-' * math.ceil(length / 2))
    for token in token_collection:
        print(token)
    whitespaces()
