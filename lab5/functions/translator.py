from functions.lexer import Lexer
from functions.parser import Parser
from functions.semantic import Semantic
from entities.print import PrintClass


class Translator:
    def __init__(self, path):
        printer = PrintClass()

        lexer = Lexer()
        tokens = lexer.get_tokens(path)
        printer.print_tokens(tokens)

        parser = Parser(lexer)
        tree = parser.parse_block()
        printer.print_tree(tree)

        semantic = Semantic()
        semantic.analyze(tree)
