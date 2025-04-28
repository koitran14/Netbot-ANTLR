from antlr4 import *
from src.database.models.order import OrderModel
from src.database.models.order_item import OrderItemModel
from src.database.models.user import UserModel
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser
from src.hooks.session import get_current_user
from src.interfaces.components.menu import MENU
from src.database.client import pg_client

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

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        greeting = ctx.GREETING().getText()
        return {"intent": "GREETING", "message": f"Hi, what do you want? You said: {greeting}"}

    def visitTopup(self, ctx: CommandParser.TopupContext):
        current_user = get_current_user()
        if not ctx.TOPUP_PREFIX():
            return {"intent": "TOPUP", "message": "Please specify how much you want to top up."}
        
        amount_ctx = ctx.amount()
        if not amount_ctx:
            return {"intent": "TOPUP", "message": "Please provide a valid amount."}

        if amount_ctx.INTEGER():
            amount = int(amount_ctx.INTEGER().getText())
        else:
            amount = float(amount_ctx.FLOAT().getText())

        currency = ctx.CURRENCY().getText() if ctx.CURRENCY() else ""
        user_model = UserModel()
        updated = user_model.add_amount(current_user["username"], amount)

        if updated is None:
            return {"intent": "TOPUP", "message": "Failed to top up. Please try again."}
        
        return {
            "intent": "TOPUP",
            "message": f"Successfully topped up {amount} {currency}. New balance: {updated['amount']} $."
        }

    def visitOrder(self, ctx: CommandParser.OrderContext):
        current_user = get_current_user()

        # Xử lý nhiều item_quantity
        items = []
        total_price = 0

        for item_ctx in ctx.item_quantity():
            quantity = int(item_ctx.INTEGER().getText())
            item_name = item_ctx.ITEM().getText()

            menu_item = get_menu_item_by_name(item_name)
            if not menu_item:
                return {"intent": "ORDER", "message": f"Item '{item_name}' not found."}

            items.append((menu_item, quantity))
            total_price += menu_item['price'] * quantity

        try:
            # Insert orders
            order_query = """
                INSERT INTO orders (user_id, total_amount)
                VALUES (%s, %s)
                RETURNING id
            """
            new_order = pg_client.insert(order_query, (current_user["id"], total_price))

            # Insert từng món vào order_items
            for menu_item, quantity in items:
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

            item_list_text = ", ".join([f"{q} x {m['name']}" for m, q in items])

            return {
                "intent": "ORDER",
                "message": f"Created order #{new_order['id']} for {item_list_text}\nTotal: ${total_price:.2f}"
            }

        except Exception as e:
            print("Error inserting order:", str(e))
            return {"intent": "ORDER", "message": "Failed to create order."}

    def visitQuery_order(self, ctx: CommandParser.Query_orderContext):
        current_user = get_current_user()
        order_model = OrderModel()
        orders = order_model.list_by_user(current_user["id"])

        if not orders:
            return {"intent": "QUERY_ORDER", "message": "You haven't placed any orders yet."}

        order_item_model = OrderItemModel()
        response = "Here's your order history:\n"
        for order in orders:
            response += f"\nOrder #{order['id']} - {order['created_at'].strftime('%d/%m/%Y %H:%M')}\n"
            items = order_item_model.list_by_order(order['id'])

            for item in items:
                item_name = get_menu_item_name_by_id(item['menu_item_id'])
                response += f"   - {item_name} x{item['quantity']} (Price at order: ${item['price_at_order']:.2f})\n"

            response += f"    Total amount: ${order['total_amount']:.2f}\n"

        return {"intent": "QUERY_ORDER", "message": response}
