import customtkinter as ctk
import time
from datetime import datetime

from src.core.parser import parse_command
from src.core.processor import CommandProcessor
from src.interfaces.components.login import LoginFrame
from src.interfaces.components.menu import MenuPopup

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

# Sample user data (in a real app, this would be in a database)


class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Food Ordering Chatbot")
        self.geometry("800x600")
        self.minsize(400, 300)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize variables
        self.current_user = None
        self.order_in_progress = False
        
        # Show login frame initially
        self.show_login_frame()
    
    def show_login_frame(self):
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
    
    def on_login_success(self, username):
        self.current_user = username
        
        # Remove login frame
        self.login_frame.grid_forget()
        
        # Show chatbot frame
        self.show_chatbot_frame()
    
    def show_chatbot_frame(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        # Create user info frame
        self.user_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.user_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="new")
        self.user_frame.grid_columnconfigure(1, weight=1)
        
        self.user_label = ctk.CTkLabel(self.user_frame, text=f"Logged in as: {self.current_user}", 
                                      font=("Arial", 12))
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.logout_button = ctk.CTkButton(self.user_frame, text="Logout", 
                                         width=100, command=self.logout)
        self.logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Create chat display frame with scrollable frame
        self.chat_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Chat")
        self.chat_frame.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Create input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Create message input
        self.message_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message here...")
        self.message_input.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.message_input.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Initialize chat messages
        self.add_bot_message(f"Hello {self.current_user}! I'm your food ordering assistant. How can I help you today? You can ask about our menu or place an order.")
    
        self.main_frame.grid_rowconfigure(0, weight=0)  # User info frame doesn't need to expand
        self.main_frame.grid_rowconfigure(1, weight=1)  # Chat frame should expand to fill space
    
    def logout(self):
        # Clear current user
        self.current_user = None
        
        # Remove chatbot frame
        self.main_frame.grid_forget()
        
        # Show login frame
        self.show_login_frame()
    
    def add_user_message(self, message):
        """Add a user message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create message frame
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#dcf8c6", "#005c4b"))
        message_frame.grid(row=len(self.chat_frame.winfo_children()), column=0, padx=(50, 10), pady=5, sticky="e")
        
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
        
    def add_bot_message(self, message):
        """Add a bot message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create message frame
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#f0f0f0", "#343541"))
        message_frame.grid(row=len(self.chat_frame.winfo_children()), column=0, padx=(10, 50), pady=5, sticky="w")
        
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
        
    def get_bot_response(self, user_message):
        """Generate a response to the user message"""
        user_message_lower = user_message.lower()
        print(f"User message: {user_message_lower}")
        try: 
            # Parse the user input
            tree = parse_command(user_message_lower)
            print(f"Parsed tree: {tree.toStringTree() if tree else 'None'}")
            # Process the parsed tree
            processor = CommandProcessor()
            response = processor.visit(tree)
            
            order_details = processor.visitOrder()
            is_order = bool(order_details)
            
            if is_order:
                self.order_in_progress = True

            return response, is_order

        except Exception as e:
            # Handle parsing or processing errors
            print(f"Error processing message: {e}")
            return "Sorry, I didn't understand that. Can you please rephrase?", False
    
        
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
            
            # Get bot response
            bot_response, show_menu = self.get_bot_response(user_message)
            self.add_bot_message(bot_response)
            
            # Show menu if needed
            if show_menu:
                self.after(500, self.show_menu)
            
            # Scroll to the bottom to show the latest messages
            self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def show_menu(self):
        """Show the food and drink menu popup"""
        menu_popup = MenuPopup(self, self.on_order_complete)
        menu_popup.focus()
    
    def on_order_complete(self, order_details):
        """Handle completed order"""
        self.order_in_progress = False
        
        # Format order details for chat
        formatted_items = [
            f"{item} x{quantity}" for item, quantity in order_details["item_quantities"].items()
        ]
        items_text = ", ".join(formatted_items)

        # Format total
        total_text = f"${order_details['total']:.2f}"

        # Add confirmation message to chat
        confirmation = (
            f"Thank you for your order!\n\n"
            f"Items: {items_text}\n"
            f"Total: {total_text}\n\n"
            f"Your order will be ready soon!"
        )
        self.add_bot_message(confirmation)
        
        # Scroll to the bottom to show the latest messages
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
