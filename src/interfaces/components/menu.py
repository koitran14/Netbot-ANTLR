import customtkinter as ctk

MENU = {
    "food": {
        "Main Dishes": [
            {"id": 1, "name": "Burger", "price": 8.99, "description": "Juicy beef patty with lettuce, tomato, and cheese"},
            {"id": 2, "name": "Pizza", "price": 12.99, "description": "Classic pepperoni pizza with mozzarella"},
            {"id": 4, "name": "Pasta", "price": 10.99, "description": "Spaghetti with marinara sauce"}
        ],
        "Sides": [
            {"id": 3, "name": "Salad", "price": 6.99, "description": "Fresh garden salad with vinaigrette"},
            {"id": 5, "name": "French Fries", "price": 3.99, "description": "Crispy golden fries with sea salt"},
            {"id": 6, "name": "Onion Rings", "price": 4.99, "description": "Crispy battered onion rings"}
        ],
        "Desserts": [
            {"id": 7, "name": "Cheesecake", "price": 5.99, "description": "New York style cheesecake"},
            {"id": 8, "name": "Ice Cream", "price": 4.49, "description": "Vanilla ice cream with chocolate sauce"},
            {"id": 9, "name": "Brownie", "price": 4.99, "description": "Warm chocolate brownie with walnuts"}
        ]
    },
    "drink": {
        "Hot Drinks": [
            {"id": 101, "name": "Coffee", "price": 3.49, "description": "Freshly brewed coffee"},
            {"id": 102, "name": "Tea", "price": 2.99, "description": "Hot tea with optional lemon or milk"},
            {"id": 103, "name": "Hot Chocolate", "price": 3.99, "description": "Rich hot chocolate with whipped cream"}
        ],
        "Cold Drinks": [
            {"id": 104, "name": "Soda", "price": 2.49, "description": "Cola, lemon-lime, or root beer"},
            {"id": 105, "name": "Iced Tea", "price": 2.99, "description": "Freshly brewed iced tea"},
            {"id": 106, "name": "Lemonade", "price": 3.49, "description": "Fresh squeezed lemonade"}
        ],
        "Smoothies": [
            {"id": 107, "name": "Fruit Smoothie", "price": 4.99, "description": "Blended fruits with yogurt"},
            {"id": 108, "name": "Protein Shake", "price": 5.99, "description": "Protein-rich shake with banana and milk"},
            {"id": 109, "name": "Green Smoothie", "price": 5.49, "description": "Spinach, kale, and fruit blend"}
        ]
    }
}


class MenuPopup(ctk.CTkToplevel):
    def __init__(self, master, on_order_complete):
        super().__init__(master)
        self.master = master
        self.on_order_complete = on_order_complete
        
        # Configure window
        self.title("Food & Drink Menu")
        self.geometry("700x600")
        self.resizable(True, True)
        
        # Make it modal
        self.transient(master)
        self.grab_set()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create title
        self.title_label = ctk.CTkLabel(self, text="Select Your Order", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Create tabs
        self.tabview.add("Food")
        self.tabview.add("Drinks")
        
        # Configure tab grid
        self.tabview.tab("Food").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Food").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Drinks").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Drinks").grid_rowconfigure(0, weight=1)
        
        # Create scrollable frames for each tab
        self.food_frame = ctk.CTkScrollableFrame(self.tabview.tab("Food"))
        self.food_frame.grid(row=0, column=0, padx=10, pady=4, sticky="nsew")
        self.food_frame.grid_columnconfigure(0, weight=1)
        
        self.drink_frame = ctk.CTkScrollableFrame(self.tabview.tab("Drinks"))
        self.drink_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.drink_frame.grid_columnconfigure(0, weight=1)
        
        # Create order summary frame
        self.order_frame = ctk.CTkFrame(self)
        self.order_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.order_frame.grid_columnconfigure(0, weight=1)
        
        self.order_label = ctk.CTkLabel(self.order_frame, text="Your Order:", font=("Arial", 16, "bold"))
        self.order_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.order_summary = ctk.CTkTextbox(self.order_frame, height=100)
        self.order_summary.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.order_summary.insert("1.0", "No items selected")
        self.order_summary.configure(state="disabled")
        
        self.total_label = ctk.CTkLabel(self.order_frame, text="Total: $0.00", font=("Arial", 16, "bold"))
        self.total_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        # Create buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", 
                                          fg_color="gray", hover_color="darkgray",
                                          command=self.cancel_order)
        self.cancel_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.confirm_button = ctk.CTkButton(self.button_frame, text="Confirm Order", 
                                           command=self.confirm_order)
        self.confirm_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Initialize variables
        self.item_quantities = {}  # Dictionary to store item quantities {item_id: quantity}
        
        # Populate menu items
        self.populate_menu()
        
    def populate_menu(self):
        # Populate food categories and items
        current_row = 0
        for category, items in MENU["food"].items():
            current_row = self.add_category(self.food_frame, category, current_row)
            for item in items:
                current_row = self.add_menu_item(self.food_frame, item, current_row)
            
            # Add a separator after each category except the last one
            if category != list(MENU["food"].keys())[-1]:
                separator = ctk.CTkFrame(self.food_frame, height=2, fg_color="gray70")
                separator.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
                current_row += 1
            
        # Populate drink categories and items
        current_row = 0
        for category, items in MENU["drink"].items():
            current_row = self.add_category(self.drink_frame, category, current_row)
            for item in items:
                current_row = self.add_menu_item(self.drink_frame, item, current_row)
            
            # Add a separator after each category except the last one
            if category != list(MENU["drink"].keys())[-1]:
                separator = ctk.CTkFrame(self.drink_frame, height=2, fg_color="gray70")
                separator.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
                current_row += 1
    
    def add_category(self, parent, category_name, row):
        """Add a category header to the menu"""
        category_label = ctk.CTkLabel(parent, text=category_name, 
                                     font=("Arial", 16, "bold"),
                                     fg_color=("#e0e0e0", "#2b2b2b"),
                                     corner_radius=6)
        category_label.grid(row=row, column=0, padx=5, pady=(15, 5), sticky="ew")
        return row + 1
    
    def add_menu_item(self, parent, item, row):
        """Add a menu item with quantity selector"""
        # Create frame for menu item
        item_frame = ctk.CTkFrame(parent)
        item_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Create item details
        name_label = ctk.CTkLabel(item_frame, text=f"{item['name']}", 
                                 font=("Arial", 14, "bold"))
        name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        price_label = ctk.CTkLabel(item_frame, text=f"${item['price']:.2f}", 
                                  font=("Arial", 14),
                                  text_color=("#2E7D32", "#4CAF50"))
        price_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="e")
        
        desc_label = ctk.CTkLabel(item_frame, text=item['description'], 
                                 wraplength=400,
                                 font=("Arial", 12))
        desc_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="w")
        
        # Create quantity selector frame
        quantity_frame = ctk.CTkFrame(item_frame)
        quantity_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="e")
        
        # Initialize quantity for this item
        self.item_quantities[item['id']] = 0
        
        # Create decrease button
        decrease_button = ctk.CTkButton(quantity_frame, text="-", width=30, height=30,
                                      command=lambda i=item: self.decrease_quantity(i))
        decrease_button.grid(row=0, column=0, padx=(0, 5))
        
        # Create quantity label
        quantity_label = ctk.CTkLabel(quantity_frame, text="0", width=30, height=30)
        quantity_label.grid(row=0, column=1, padx=5)
        
        # Store reference to the label for updating
        item['quantity_label'] = quantity_label
        
        # Create increase button
        increase_button = ctk.CTkButton(quantity_frame, text="+", width=30, height=30,
                                      command=lambda i=item: self.increase_quantity(i))
        increase_button.grid(row=0, column=2, padx=(5, 0))
        
        return row + 1
    
    def increase_quantity(self, item):
        """Increase the quantity of an item"""
        self.item_quantities[item['id']] += 1
        item['quantity_label'].configure(text=str(self.item_quantities[item['id']]))
        self.update_order_summary()
    
    def decrease_quantity(self, item):
        """Decrease the quantity of an item"""
        if self.item_quantities[item['id']] > 0:
            self.item_quantities[item['id']] -= 1
            item['quantity_label'].configure(text=str(self.item_quantities[item['id']]))
            self.update_order_summary()
    
    def update_order_summary(self):
        """Update the order summary based on selected items and quantities"""
        self.order_summary.configure(state="normal")
        self.order_summary.delete("1.0", "end")
        
        selected_items = []
        total = 0
        
        # Collect all food items with quantity > 0
        for category, items in MENU["food"].items():
            for item in items:
                quantity = self.item_quantities.get(item['id'], 0)
                if quantity > 0:
                    selected_items.append((item, quantity))
                    total += item['price'] * quantity
        
        # Collect all drink items with quantity > 0
        for category, items in MENU["drink"].items():
            for item in items:
                quantity = self.item_quantities.get(item['id'], 0)
                if quantity > 0:
                    selected_items.append((item, quantity))
                    total += item['price'] * quantity
        
        if not selected_items:
            self.order_summary.insert("1.0", "No items selected")
            self.total_label.configure(text="Total: $0.00")
        else:
            for item, quantity in selected_items:
                subtotal = item['price'] * quantity
                self.order_summary.insert("end", f"{quantity}x {item['name']} - ${subtotal:.2f}\n")
            
            self.total_label.configure(text=f"Total: ${total:.2f}")
        
        self.order_summary.configure(state="disabled")
    
    def cancel_order(self):
        self.destroy()
    
    def confirm_order(self):
        """Confirm the order and send details back to the chatbot"""
        selected_items = []
        total = 0
        
        # Collect all food items with quantity > 0
        for category, items in MENU["food"].items():
            for item in items:
                quantity = self.item_quantities.get(item['id'], 0)
                if quantity > 0:
                    for _ in range(quantity):
                        selected_items.append(item["name"])
                    total += item['price'] * quantity
        
        # Collect all drink items with quantity > 0
        for category, items in MENU["drink"].items():
            for item in items:
                quantity = self.item_quantities.get(item['id'], 0)
                if quantity > 0:
                    for _ in range(quantity):
                        selected_items.append(item["name"])
                    total += item['price'] * quantity
        
        if not selected_items:
            return
        
        # Create a more detailed order summary
        order_details = {
            "items": selected_items,
            "total": total,
            "item_quantities": {item["name"]: self.item_quantities.get(item['id'], 0) 
                               for category in MENU["food"].values() 
                               for item in category if self.item_quantities.get(item['id'], 0) > 0}
        }
        
        # Add drink quantities
        for category in MENU["drink"].values():
            for item in category:
                if self.item_quantities.get(item['id'], 0) > 0:
                    order_details["item_quantities"][item["name"]] = self.item_quantities.get(item['id'], 0)
                    
                    
        print("Order Details:", order_details)  # Debugging line
        
        self.on_order_complete(order_details)
        self.destroy()
