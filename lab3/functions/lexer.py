from entities.constants import *
from entities.token import Token
import re


class Lexer:
    def __init__(self):
        self.var_tokens = {}
        self.func_tokens = {}
        self.constants_tokens = {}
        self.var_types_tokens = []
        self.key_word_tokens = []

        self.tokens = []

    @staticmethod
    def get_file(path):
        with open(path, 'r') as f:
            data = f.read()

        return data

    @staticmethod
    def is_control_character(symbol):
        return symbol == '\t' or symbol == '\n'

    @staticmethod
    def is_valid_variable_name(name):
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name))

    @staticmethod
    def is_int(number_str):
        if not number_str:
            return False
        if not (number_str.isdigit() or (number_str[0] == '-' and number_str[1:].isdigit())):
            return False
        number = int(number_str)
        return number_str == str(number)

    def is_float(self, number_str):
        if not number_str:
            return False
        try:
            float(number_str)
        except ValueError:
            return False
        return not (self.is_int(number_str) or (number_str[0] == '-' and self.is_int(number_str[1:])))

    def is_signed(self, space):
        return not space and len(self.tokens) > 0 and (self.tokens[-1].word == '+' or self.tokens[-1].word == '-')

    @staticmethod
    def __get_line(code, row):
        return code.split('\n')[row - 1]

    def get_tokens(self, path):
        code = self.get_file(path)

        space = False
        current = ''
        string_read = False
        char_read = False

        row, column = 1, 1
        for s in code:
            if not self.is_control_character(s) and s not in separators and s not in operators and (
                    s != ' ' or string_read or char_read):
                if s == '"' and not char_read:
                    string_read = not string_read
                elif s == "'" and not string_read:
                    char_read = not char_read

                current += s

            else:
                if current in var_types:
                    self.var_types_tokens.append(current)
                    self.tokens.append(Token(current, 'VARIABLE TYPE'))
                    current = ''
                elif current in key_words:
                    self.key_word_tokens.append(current)
                    self.tokens.append(Token(current, 'KEY WORD'))
                    current = ''
                elif (s == '<' or s == '>') and self.tokens[-1].word == '#include':
                    current += s
                elif len(current) > 0 and current[0] == '"' and current[-1] == '"':
                    self.constants_tokens[current] = 'STRING CONSTANT'
                    self.tokens.append(Token(current, 'STRING CONSTANT'))
                    current = ''
                elif len(current) > 0 and current[0] == "'" and current[-1] == "'":
                    self.constants_tokens[current] = 'CHAR CONSTANT'
                    self.tokens.append(Token(current, 'CHAR CONSTANT'))
                    current = ''
                elif self.is_int(current):
                    if self.is_signed(space):
                        current = self.tokens[-1].word + current
                        self.tokens.pop()
                    self.constants_tokens[current] = 'INT CONSTANT'
                    self.tokens.append(Token(current, 'INT CONSTANT'))
                    current = ''
                elif self.is_float(current):
                    if self.is_signed(space):
                        current = self.tokens[-1].word + current
                        self.tokens.pop()
                    self.constants_tokens[current] = 'FLOAT CONSTANT'
                    self.tokens.append(Token(current, 'FLOAT CONSTANT'))
                    current = ''
                elif self.is_valid_variable_name(current):
                    var_type = ''
                    for token in reversed(self.tokens):
                        if token.word != ',' and token.word in separators:  # not find
                            break
                        elif token.word in var_types:  # find a var type
                            var_type = token.word
                            break

                    # if len(var_type) > 0 and (current in self.var_tokens.keys() or current in self.func_tokens.keys()):
                    #     raise Exception(f'\n[{row}, {column}] LexicalError, redefinition of name "{current}":\n'
                    #                     f'[{row}]: {self.__get_line(code, row)}\n'
                    #                     f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                    # else:
                    if current not in self.var_tokens.keys():
                        if len(var_type) == 0:
                            raise Exception(
                                f'\n[{row}, {column}] LexicalError, unexpected "{current}":\n'
                                f'[{row}]: {self.__get_line(code, row)}\n'
                                f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                        self.var_tokens[current] = var_type
                    self.tokens.append(Token(current, 'VARIABLE'))
                    current = ''

                if not char_read and not string_read:
                    if not self.is_control_character(s) and s != ' ':
                        if s in separators:
                            if s == '(' and len(self.tokens) > 0 and self.tokens[-1].word in self.var_tokens.keys():
                                self.tokens[-1].token_type = 'FUNCTION'
                                self.func_tokens[self.tokens[-1].word] = self.var_tokens[self.tokens[-1].word]
                                del self.var_tokens[self.tokens[-1].word]
                            self.tokens.append(Token(s, 'SEPARATOR'))
                        elif s in operators and not ((s == '<' or s == '>') and self.tokens[-1].word == '#include'):
                            temp = s
                            if not space and len(self.tokens) > 0 and self.tokens[
                                -1].word in operators + possible_operators:
                                temp = self.tokens[-1].word + s
                                if temp not in possible_operators:
                                    raise Exception(
                                        f'\n[{row}, {column}] LexicalError, invalid operator "{temp}":\n'
                                        f'[{row}]: {self.__get_line(code, row)}\n'
                                        f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                                self.tokens.pop()
                            self.tokens.append(Token(temp, 'OPERATOR'))
                            current = ''

                        space = False
                    else:
                        if len(current.replace(" ", "").replace("\t", "").replace("\n", "")) > 0:
                            raise Exception(f'\n[{row}, {column}] LexicalError, invalid variable name "{current}":\n'
                                            f'[{row}]: {self.__get_line(code, row)}\n'
                                            f'{" " * (len((row + 1).__str__()) + 1 + column)}^')
                        space = True
                else:
                    current += s

            if s == '\n':
                row += 1
                column = 1
            else:
                column += 1

        return self.tokens
