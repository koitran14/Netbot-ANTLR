from antlr4 import *
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        """
        Returns all parameters from the GreetingContext.
        
        Args:
            ctx: CommandParser.GreetingContext
            
        Returns:
            dict: Dictionary containing intent and parsed parameters
        """
        return {
            "intent": "GREETING",
            "params": {
                "greeting": ctx.GREETING().getText() if ctx.GREETING() else None
            }
        }

    def visitTopup(self, ctx: CommandParser.TopupContext):
        """
        Returns all parameters from the TopupContext.
        
        Args:
            ctx: CommandParser.TopupContext
            
        Returns:
            dict: Dictionary containing intent and parsed parameters
        """
        params = {}
        
        # TOPUP_PREFIX
        params["topup_prefix"] = ctx.TOPUP_PREFIX().getText() if ctx.TOPUP_PREFIX() else None
        
        # Amount (INTEGER or FLOAT)
        amount_ctx = ctx.amount()
        if amount_ctx:
            integer_node = amount_ctx.INTEGER()
            float_node = amount_ctx.FLOAT()
            
            if integer_node:
                if isinstance(integer_node, list):
                    integer_node = integer_node[0] if integer_node else None
                params["amount"] = integer_node.getText() if integer_node else None
                params["amount_type"] = "INTEGER"
            elif float_node:
                if isinstance(float_node, list):
                    float_node = float_node[0] if float_node else None
                params["amount"] = float_node.getText() if float_node else None
                params["amount_type"] = "FLOAT"
        
        # CURRENCY
        params["currency"] = ctx.CURRENCY().getText() if ctx.CURRENCY() else None
        
        # POLITE
        params["polite"] = ctx.POLITE().getText() if ctx.POLITE() else None
        
        # Account specification
        account_spec = ctx.account_spec()
        if account_spec:
            if account_spec.ACCOUNT_NAME():
                params["account_name"] = account_spec.ACCOUNT_NAME().getText()
            elif account_spec.getText().startswith("to my account"):
                params["account_name"] = "my account"
            else:
                params["account_name"] = None
        
        return {
            "intent": "TOPUP",
            "params": params
        }

    def visitOrder(self, ctx: CommandParser.OrderContext):
        """
        Returns all parameters from the OrderContext.
        
        Args:
            ctx: CommandParser.OrderContext
            
        Returns:
            dict: Dictionary containing intent and parsed parameters
        """
        params = {}
        
        # ORDER_PREFIX
        params["order_prefix"] = ctx.ORDER_PREFIX().getText() if ctx.ORDER_PREFIX() else None
        
        # ITEMS LIST (replaces single quantity & item)
        items = []
        item_orders = ctx.item_order_list().item_order() if ctx.item_order_list() else []

        for item_ctx in item_orders:
            quantity = int(item_ctx.INTEGER().getText())
            item = item_ctx.ITEM().getText()
            items.append({"quantity": quantity, "item": item})

        params["items"] = items

        
        # POLITE
        params["polite"] = ctx.POLITE().getText() if ctx.POLITE() else None
        
        return {
            "intent": "ORDER",
            "params": params
        }