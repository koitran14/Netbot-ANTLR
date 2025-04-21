from antlr4 import *
from src.generated.CommandLexer import CommandLexer
from src.generated.CommandParser import CommandParser
from src.core.processor import CommandProcessor

def parse_command(input_text: str):
    input_stream = InputStream(input_text)
    lexer = CommandLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CommandParser(stream)
    tree = parser.command()
    visitor = CommandProcessor()
    result = visitor.visit(tree)
    return result

def main():
    print("Chatbot demo ANTLR. Nhập 'thoát' để dừng.")
    while True:
        s = input("Bạn: ")
        if s.strip().lower() == 'thoát':
            break
        try:
            result = parse_command(s)
            print("➡ Kết quả:", result)
        except Exception as e:
            print("❌ Lỗi:", str(e))

if __name__ == '__main__':
    main()
