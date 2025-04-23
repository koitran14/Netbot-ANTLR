from src.database.models.user import UserModel
from src.database.models.order import OrderModel
from src.database.models.order_item import OrderItemModel
from src.database.client import pg_client

def main():
    user_model = UserModel()
    order_model = OrderModel()
    order_item_model = OrderItemModel()

    # Create a user
    # user = user_model.create("demo", "demo")
    # print(f"Created user: {user}")
    # user1 = user_model.create("khoitran1403", "khoitran1403")
    # print(f"Created user: {user1}")

    # Create an order
    order = order_model.create(1, 12.48)  # Burger + Coffee
    print(f"Created order: {order}")

    # Add order items
    order_item1 = order_item_model.create(order["id"], 1, 1, 8.99)  # Burger
    order_item2 = order_item_model.create(order["id"], 101, 1, 3.49)  # Coffee
    print(f"Created order items: {order_item1}, {order_item2}")

    # Retrieve order with items
    order_details = order_model.read(order["id"])
    order_items = order_item_model.list_by_order(order["id"])
    print(f"Order details: {order_details}")
    print(f"Order items: {order_items}")

    # List user's orders
    user_orders = order_model.list_by_user(1)
    print(f"User's orders: {user_orders}")

    # Verify user's order count
    updated_user = user_model.read(1)
    print(f"Updated user: {updated_user}")

    # Clean up connections
    pg_client.close_all()

if __name__ == "__main__":
    main()