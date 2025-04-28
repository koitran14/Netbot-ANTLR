from antlr4 import *
from src.core.parser import parse_command
from src.core.processor import CommandProcessor

def main():
    print(" Chatbot for Order and Topup. Type 'quit' to exit.")
    processor = CommandProcessor()

    while True:
        user_input = input("👤 You: ")
        if user_input.lower() == "quit":
            print("Bye!")
            break

        try:
            # Parse the command using parse_command function
            tree = parse_command(user_input.lower())
            if not tree:
                print(" Could not understand your input.")
                continue

            # Process the command
            result = processor.visit(tree)

            # Pretty print based on intent
            if isinstance(result, dict) and "message" in result:
                print("", result["message"])
            else:
                print(" Sorry, I didn't understand that.")

        except Exception as e:
            print(" Error:", str(e))

if __name__ == "__main__":
    main()
