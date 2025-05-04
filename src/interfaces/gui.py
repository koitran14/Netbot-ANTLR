import customtkinter as ctk
import time
from datetime import datetime
from src.database.client import pg_client
from src.interfaces.components.menu import MENU, MenuPopup
from src.core.parser import parse_command
from src.core.processor import CommandProcessor
from src.hooks.session import clear_current_user, set_current_user
from src.interfaces.components.login import LoginFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Food Ordering Chatbot")
        self.geometry("800x600")
        self.minsize(400, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_user = None
        self.order_in_progress = False

        self.show_login_frame()

    def show_login_frame(self):
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
    
    def on_login_success(self, user): 
        """
            "id": result[0],
            "username": result[1],
            "password": result[2],  # You can omit this if you don't want to return it
            "total_amount": result[3],
            "orders": result[4]
        """       
        self.current_user = user
        set_current_user(user)
        self.login_frame.grid_forget()
        self.show_chatbot_frame()

    def show_chatbot_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.user_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.user_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="new")
        self.user_frame.grid_columnconfigure(1, weight=1)

        self.user_label = ctk.CTkLabel(self.user_frame, text=f"Logged in as: {self.current_user['username']}", font=("Arial", 12))
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.logout_button = ctk.CTkButton(self.user_frame, text="Logout", width=100, command=self.logout)
        self.logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.chat_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Chat")
        self.chat_frame.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message here...")
        self.message_input.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.message_input.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.add_bot_message(f"Hello {self.current_user['username']}! I'm your food ordering assistant. How can I help you today?")

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

    def logout(self):
        self.current_user = None
        clear_current_user()
        self.main_frame.grid_forget()
        self.show_login_frame()

    def add_user_message(self, message):
        timestamp = datetime.now().strftime("%H:%M")
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#dcf8c6", "#005c4b"))
        message_frame.grid(row=len(self.chat_frame.winfo_children()), column=0, padx=(50, 10), pady=5, sticky="e")

        message_label = ctk.CTkLabel(message_frame, text=message, wraplength=400, justify="left", text_color=("black", "white"))
        message_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        time_label = ctk.CTkLabel(message_frame, text=timestamp, font=("Arial", 9), text_color=("gray50", "gray70"))
        time_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="e")

    def add_bot_message(self, message):
        timestamp = datetime.now().strftime("%H:%M")
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color=("#f0f0f0", "#343541"))
        message_frame.grid(row=len(self.chat_frame.winfo_children()), column=0, padx=(10, 50), pady=5, sticky="w")

        message_label = ctk.CTkLabel(message_frame, text=message, wraplength=400, justify="left", text_color=("black", "white"))
        message_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        time_label = ctk.CTkLabel(message_frame, text=timestamp, font=("Arial", 9), text_color=("gray50", "gray70"))
        time_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="e")

    def get_bot_response(self, user_message):
        user_message_lower = user_message.lower()
        try:
            tree = parse_command(user_message_lower)
            processor = CommandProcessor()
            response = processor.visit(tree)
            is_order = response["intent"] == 'ORDER' and response.get("isMenuOpen", False)
            if is_order:
                self.order_in_progress = True
            return response["message"], is_order
        except Exception as e:
            print(f"Error processing message: {e}")
            return "Sorry, I didn't understand that. Can you please rephrase?", False

    def send_message(self, event=None):
        user_message = self.message_input.get().strip()
        if user_message:
            self.add_user_message(user_message)
            self.message_input.delete(0, "end")
            self.update()
            time.sleep(0.3)
            bot_response, show_menu = self.get_bot_response(user_message)
            self.add_bot_message(bot_response)
            if show_menu:
                self.show_menu()
            self.chat_frame._parent_canvas.yview_moveto(1.0)

    def show_menu(self):
        menu_popup = MenuPopup(self, self.on_order_complete, self.current_user)
        menu_popup.focus()

    def on_order_complete(self, order_details):
        self.order_in_progress = False

        formatted_items = [f"\n- {quantity} {item}" for item, quantity in order_details["item_quantities"].items()]
        items_text = ". ".join(formatted_items)

        try:
            # Insert order into orders table
            order_query = """
                INSERT INTO orders (user_id, total_amount)
                VALUES (%s, %s)
                RETURNING id
            """
            new_order = pg_client.insert(order_query, (self.current_user["id"], order_details["total"]))

            # Insert order items
            for item_name, quantity in order_details["item_quantities"].items():
                menu_item = next(
                    (item for category in list(MENU["food"].values()) + list(MENU["drink"].values())
                     for item in category if item['name'].lower() == item_name.lower()), None)

                if menu_item:
                    order_item_query = """
                        INSERT INTO order_items (order_id, menu_item_id, quantity, price_at_order)
                        VALUES (%s, %s, %s, %s)
                    """
                    pg_client.insert(order_item_query, (
                        new_order['id'],
                        menu_item['id'],
                        quantity,
                        menu_item['price']
                    ))
        except Exception as e:
            print("Failed to insert order into database:", str(e))

        total_text = f"${order_details['total']:.2f}"
        confirmation = (
            f"Thank you for your order!\n\n"
            f"Items: \n\n{items_text}\n"
            "\n--------------------\n"
            f"\nTotal: {total_text}\n\n"
            f"Your order will be ready soon!"
        )
        self.add_bot_message(confirmation)
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
