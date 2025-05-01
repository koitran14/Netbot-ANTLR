from src.interfaces.components.menu import MENU

def get_menu_item_name_by_id(menu_item_id):
    for category_items in MENU["food"].values():
        for item in category_items:
            if item['id'] == menu_item_id:
                return item['name']
    for category_items in MENU["drink"].values():
        for item in category_items:
            if item['id'] == menu_item_id:
                return item['name']
    return f"Unknown Item ID {menu_item_id}"

def get_menu_item_by_name(name):
    for category_items in MENU["food"].values():
        for item in category_items:
            if item["name"].lower() == name.lower():
                return item
    for category_items in MENU["drink"].values():
        for item in category_items:
            if item["name"].lower() == name.lower():
                return item
    return None