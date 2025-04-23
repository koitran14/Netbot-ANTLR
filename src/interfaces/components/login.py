import customtkinter as ctk
from src.database.models.user import UserModel

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create login form
        self.login_label = ctk.CTkLabel(self, text="Login to Food Ordering System", font=("Arial", 20))
        self.login_label.grid(row=0, column=0, padx=20, pady=(40, 20))
        
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(20, 10), sticky="ew")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="ew")
        self.password_entry.bind("<Return>", self.login)
        
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=30, pady=(20, 10))
        
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=4, column=0, padx=30, pady=(10, 20))
        
        # Demo credentials label
        self.demo_label = ctk.CTkLabel(self, text="Demo credentials: username 'demo', password 'demo'", 
                                      font=("Arial", 12), text_color="gray")
        self.demo_label.grid(row=5, column=0, padx=30, pady=(30, 20))
        
    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_model = UserModel()
        
        verify = user_model.auth_login(username, password)
        
        if verify is not None:
            self.on_login_success(verify)
        else:
            self.status_label.configure(text="Invalid username or password")
            self.password_entry.delete(0, "end")