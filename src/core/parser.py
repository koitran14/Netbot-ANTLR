from antlr4 import *
from src.generated.CommandLexer import CommandLexer
from src.generated.CommandParser import CommandParser

def parse_command(input_text):
    """
    Phân tích lệnh chatbot và trả về cây cú pháp.
    """
    input_stream = InputStream(input_text)
    lexer = CommandLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CommandParser(stream)
    tree = parser.command()  # Gọi quy tắc gốc 'command'
    return tree