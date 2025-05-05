import random
from antlr4 import *
from src.database.models.menu import get_menu_item_by_name, get_menu_item_name_by_id
from src.database.models.topup import TopupModel
from src.database.models.order import OrderModel
from src.database.models.order_item import OrderItemModel
from src.database.models.user import UserModel
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser
from src.hooks.session import get_current_user
from src.database.client import pg_client

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        greeting = ctx.GREETING().getText().lower()
        current_user = get_current_user()
        username = current_user['username']
        
        greeting_responses = {
            "hello": [
                f"Hello, {username}! Great to see you!",
                f"Hi {username}! Ready to get started?"
            ],
            "hi": [
                f"Hi {username}! Excited to help you today!",
                f"Hey {username}, what's up?"
            ],
            "hey": [
                f"Hey {username}! What's on your mind?",
                f"Yo {username}, let's make something happen!"
            ],
            "good morning": [
                f"Good morning, {username}! Perfect time for a coffee!",
                f"Morning {username}! Ready to kickstart your day?"
            ],
            "good afternoon": [
                f"Good afternoon, {username}! Hungry for some pizza?",
                f"Hey {username}, happy afternoon! What's next?"
            ]
        }
         
        default_responses = [
            f"Hey {username}, nice to hear from you!",
            f"Hi {username}! What's up today?",
            f"Hello {username}, ready to dive in?"
        ]
        
        response_options = greeting_responses.get(greeting, default_responses)
        greeting_message = random.choice(response_options)
        
        services_intro = (
            "\n\nYou can order something tasty like coffee or pizza, "
            "top up your account with some dollars, "
            "or check your top-up history. Just let me know what you want to do!"
        )
         
        return {
            "intent": "GREETING",
            "message": f"{greeting_message}{services_intro}"
        }

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
            return {"intent": "TOPUP", "message": "Hmm, I couldn’t find a valid amount. Please try again with a number like '50' or '10.50'."}
        
        try:
            float(amount) 
        except ValueError:
            return {"intent": "TOPUP", "message": f"Oh no, '{amount}' doesn’t seem like a valid amount. Could you use a number like '50' or '10.50'?"}
        
        print(f"Currency: {ctx.CURRENCY()}")
        
        if not ctx.CURRENCY():
            return {"intent": "TOPUP", "message": f"Invalid currrency. We only allow to topup in dollars or usd. Please try again!"}
        
        currency = ctx.CURRENCY().getText() if ctx.CURRENCY() else ""  # Optional
        
        polite = ctx.POLITE().getText() if ctx.POLITE() else ""  # Optional
        account_spec = ctx.account_spec()
        account = current_user['username']
        account_message = "your account"
        accId = current_user['id']
        user_model = UserModel()
        
        if account_spec and account_spec.ACCOUNT_NAME():
            account = account_spec.ACCOUNT_NAME().getText()
            account_message = f"{account}'s account"
            if account != current_user["username"]:
                target_user = user_model.read(account)
                if not target_user:
                    return {
                        "intent": "TOPUP",
                        "message": f"Sorry, I couldn’t find an account for '{account}'. Please check the username and try again!"
                    }
                                        
            accId = target_user["id"]
            
        topup_model = TopupModel()
        topup_model.add_topup(accId, float(amount))
        update_amount = user_model.read(account)

        if update_amount is None:
            return {"intent": "TOPUP", "message": "Hmm, I couldn’t add that amount. Could you try again?"}
        return {
            "intent": "TOPUP",
            "message": f"Great!\n\nYou have successfully topped up {amount} {currency} to {account_message}.\n\nCurrent total: {update_amount['total_amount']} $.\n\nThank you!"
        }

    def visitOrder(self, ctx: CommandParser.OrderContext):
        current_user = get_current_user()

        # Xử lý nhiều item_quantity
        items = []
        total_price = 0
        
        if not ctx.item_quantity() or len(ctx.item_quantity()) == 0:
            return {"intent": "ORDER", "message": "Yeah sure, here's your menu.", "isMenuOpen": True}

        for item_ctx in ctx.item_quantity():
            if not item_ctx.INTEGER() or not item_ctx.ITEM():
                return {"intent": "ORDER", "message": "Yeah sure, here's your menu.", "isMenuOpen": True}

            quantity = int(item_ctx.INTEGER().getText())
            item_name = item_ctx.ITEM().getText().lower()

            menu_item = get_menu_item_by_name(item_name)
            if not menu_item:
                return {"intent": "ORDER", "message": f"Item '{item_name}' not found. Please check the menu again!", "isMenuOpen": True}

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

             # Format items_text with each item on a new line
            items_text = "\n".join([f"- {q} {m['pluralName'] if q != 1 else m['name']}" for m, q in items])

            # Create confirmation message using the template
            confirmation = (
                f"Thank you for your order!\n\n"
                f"Items: \n\n{items_text}\n"
                "\n--------------------\n"
                f"\nTotal: ${total_price:.2f}\n\n"
                f"Your order will be ready soon!"
            )
            
            return {
                "intent": "ORDER",
                "message": confirmation
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

        
    def visitTopupQuery(self, ctx: CommandParser.TopupQueryContext):
        current_user = get_current_user()  # Assumes returns {'id': BIGINT, 'username': str, 'uuid': UUID, ...}
        print(f"current_user_id: {current_user['id']}")

        query_type = "all"
        if ctx.query_type():
            query_type_text = ctx.query_type().getText()
            if query_type_text == 'latest' or query_type_text =='newest':
                query_type = "latest"
            elif query_type_text == 'oldest':
                query_type = "oldest"
            elif query_type_text == 'all':
                query_type = "all"
            else:
                return {
                    "intent": "QUERY_TOPUP",
                    "message": "I didn’t understand the query type. Could you use 'latest', 'oldest', or 'all' topups?"
                }

        polite = ctx.POLITE().getText() if ctx.POLITE() else ""  # Optional
        account_spec = ctx.account_spec()
        account = current_user['username']
        account_message = "your account"
        user = current_user
        user_model = UserModel()
        
        if account_spec and account_spec.ACCOUNT_NAME():
            account = account_spec.ACCOUNT_NAME().getText()
            account_message = f"{account}'s account"
            if account != current_user["username"]:
                target_user = user_model.read(account)
                if not target_user:
                    return {
                        "intent": "TOPUP",
                        "message": f"Sorry, I couldn’t find an account for '{account}'. Please check the username and try again!"
                    }
                                        
            user = target_user

        # Database execution to fetch top-up history
        topup_model = TopupModel()
        topups = topup_model.get_by_user(user['id'], query_type)  # Placeholder for DB executor

        if not topups:
            return {
                "intent": "QUERY_TOPUP",
                "message": f"Looks like there are no top-ups for {account_message} yet. Try topping up first!"
            }

        # Format the response based on query_type
        intro_messages = [
            f"Here’s the top-up history for {account_message}:",
            f"Let me show you the top-up details for {account_message}:",
            f"Got the top-up history for {account_message} right here:"
        ]
        response_message = f"{random.choice(intro_messages)}\n\n"

        if query_type == "latest":
            topup = topups[0]
            response_message += (
                f"\n===================================\n\n"
                f"   Latest Top-up:\n\n"
                f"   Amount: {topup['amount']:.2f} {topup['currency'].upper()}\n"
                f"   Date: {topup['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
        elif query_type == "oldest":
            topup = topups[0]
            response_message += (
                f"\n===================================\n\n"
                f"   Oldest Top-up:\n\n"
                f"   Amount: {topup['amount']:.2f} {topup['currency'].upper()}\n"
                f"   Date: {topup['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
        else:  # all
            if len(topups) == 1:
                topup = topups[0]
                response_message += (
                    f"\n===================================\n\n"
                    f"   Only Top-up:\n\n"
                    f"   Amount: {topup['amount']:.2f} {topup['currency'].upper()}\n"
                    f"   Date: {topup['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
            else:
                response_message += f"\n===================================\n\n"
                response_message += f"All Top-ups ({len(topups)}):\n\n"

                for i, topup in enumerate(topups, 1):
                    response_message += (
                        f"{i}.  Amount: {topup['amount']:.2f} {topup['currency'].upper()}\n"
                        f"      Date: {topup['created_at'].strftime('%Y-%m-%d %H:%M:%S')} \n\n"
                    )
        response_message += f"\n===================================\n"

        response_message += f"\nTotal Balance: {user['total_amount']:.2f} USD\n"
        if polite:
            polite_closures = ["You’re very welcome! 😊", "Happy to help! 😄", "My pleasure! ✨"]
            response_message += f"\n{random.choice(polite_closures)}"
        else:
            response_message += "\nPlease check!"

        return {
            "intent": "QUERY_TOPUP",
            "message": response_message
        }