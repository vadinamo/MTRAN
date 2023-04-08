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
