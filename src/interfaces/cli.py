from src.core.parser import parse_command
from src.core.processor import CommandProcessor

def main():
    print("Chatbot for Order and Topup. Type 'quit' to exit.")
    while True:
        user_input = input ("You: ")
        if user_input.lower() == "quit":
            print("quit!")
            break
        try:
            
            # Parse the command using the parse_command function
            tree = parse_command(user_input.lower())
            
            # Process the command using the CommandProcessor class
            processor = CommandProcessor()
            result = processor.visit(tree)
            print("Result:", result)
        except Exception as e:
            print("Error:", str(e))
            
if __name__ == "__main__":
    main()
            
            