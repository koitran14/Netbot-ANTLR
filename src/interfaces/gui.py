import customtkinter as ctk
import time
from datetime import datetime

from src.core.parser import parse_command
from src.core.processor import CommandProcessor

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Modern Chatbot")
        self.geometry("800x600")
        self.minsize(400, 300)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create chat display frame with scrollable frame
        self.chat_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Chat")
        self.chat_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Create input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Create message input
        self.message_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message here...")
        self.message_input.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.message_input.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Initialize message count
        self.message_count = 0
        
        # Add initial bot message
        self.add_bot_message("Hello! I'm your friendly chatbot assistant. How can I help you today?")
        
    def add_user_message(self, message):
        """Add a user message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create message frame
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#dcf8c6", "#005c4b"))
        message_frame.grid(row=self.message_count, column=0, padx=(50, 10), pady=5, sticky="e")
        
        # Add message text
        message_label = ctk.CTkLabel(
            message_frame, 
            text=message, 
            wraplength=400, 
            justify="left",
            text_color=("black", "white")
        )
        message_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Add timestamp
        time_label = ctk.CTkLabel(
            message_frame, 
            text=timestamp, 
            font=("Arial", 9),
            text_color=("gray50", "gray70")
        )
        time_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="e")
        
        # Increment the message count
        self.message_count += 1
        
    def add_bot_message(self, message):
        """Add a bot message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create message frame
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#f0f0f0", "#343541"))
        message_frame.grid(row=self.message_count, column=0, padx=(10, 50), pady=5, sticky="w")
        
        # Add message text
        message_label = ctk.CTkLabel(
            message_frame, 
            text=message, 
            wraplength=400, 
            justify="left",
            text_color=("black", "white")
        )
        message_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Add timestamp
        time_label = ctk.CTkLabel(
            message_frame, 
            text=timestamp, 
            font=("Arial", 9),
            text_color=("gray50", "gray70")
        )
        time_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="e")
        
        # Increment the message count
        self.message_count += 1
        
    def get_bot_response(self, user_message):
        # Check for keywords in the user message
        user_message_lower = user_message.lower()
        print(f"User message: {user_message_lower}")
        try: 
            # Parse the user input
            tree = parse_command(user_message_lower)
            print(f"Parsed tree: {tree.toStringTree() if tree else 'None'}")
            # Process the parsed tree
            processor = CommandProcessor()
            result = processor.visit(tree)
            print(f"Processing result: {result}")
            
            if result["intent"] == "greeting":
                return f"You said {result['greeting']}!"
            
            elif result["intent"] == "order":
                return f"You want to order {result['order']}!"
            
            elif result["intent"] == "topup":
                polite = f" ({result['polite']}))" if result['polite'] else ""
                currency = result['currency'] if result['currency'] else ""
                account = f" for account {result['account']}" if result['account'] != "my account" else ""
                return f"You want to top up {result['amount']} {currency}{account}{polite}!"
            
            else:
                return "I'm not sure how to respond to that. Can you try asking something else?"
        
        except Exception as e:
            # Handle parsing or processing errors
            print(f"Error processing message: {e}")
            return "Sorry, I didn't understand that. Can you please rephrase?"
                        
    def send_message(self, event=None):
        """Send a message and get a response"""
        user_message = self.message_input.get().strip()
        if user_message:
            # Add user message to chat
            self.add_user_message(user_message)
            
            # Clear input field
            self.message_input.delete(0, "end")
            
            # Update UI
            self.update()
            
            # Simulate bot "typing" with a small delay
            time.sleep(0.5)
            
            # Get and display bot response
            bot_response = self.get_bot_response(user_message)
            self.add_bot_message(bot_response)
            
            # Scroll to the bottom to show the latest messages
            self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()