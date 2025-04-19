from src.core.parser import parse_command
from src.core.processor import CommandProcessor

def main():
    print("Chatbot lịch hẹn. Nhập 'thoát' để dừng.")
    while True:
        user_input = input ("Bạn: ")
        if user_input.lower() == "thoát":
            print("Tạm biệt!")
            break
        try:
            
            # Parse the command using the parse_command function
            tree = parse_command(user_input)
            
            # Process the command using the CommandProcessor class
            processor = CommandProcessor()
            result = processor.visit(tree)
            print("Kết quả:", result)
        except Exception as e:
            print("Lỗi:", str(e))
            
if __name__ == "__main__":
    main()
            
            