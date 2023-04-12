import re


def get_file(path):
    with open(path, 'r') as f:
        data = f.read()

    return data


def is_control_character(symbol):
    return symbol == '\t' or symbol == '\n'


def is_valid_variable_name(name):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


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