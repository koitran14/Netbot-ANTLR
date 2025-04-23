from antlr4 import *
from src.database.models.user import UserModel
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser
from src.hooks import get_current_user

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        greeting = ctx.GREETING().getText()
        return {"intent": "GREETING", "message": f"Hi, what do you want? You said: {greeting}"} 

    def visitTopup(self, ctx: CommandParser.TopupContext):
        current_user = get_current_user()
        print(f"current_user_id: {current_user["id"]}")
        
        if not ctx.TOPUP_PREFIX():
            return {"intent": "TOPUP", "message": "Oops, it looks like you forgot to say how you'd like to top up! Try something like 'top up 50 usd'."}
        if not ctx.AMOUNT() or len(ctx.AMOUNT().getText()) == 0 or ctx.AMOUNT().getText() == "<missing AMOUNT>":
            return {"intent": "TOPUP", "message": "Hmm, I need an amount to top up! Could you add something like '50' or '10.50'?"}
        
        topup_prefix = ctx.TOPUP_PREFIX().getText()
        amount = ctx.AMOUNT().getText()
        
        try:
            float(amount)  # Ensure amount is a valid number
        except ValueError:
            return {"intent": "TOPUP", "message": f"Oh no, '{amount}' doesn't seem like a valid amount. Could you use a number like '50' or '10.50'?"}
        
        print(f"Currency: {ctx.CURRENCY()}")
        
        currency = ctx.CURRENCY().getText() if ctx.CURRENCY() else ""  # Optional, check for None
        polite = ctx.POLITE().getText() if ctx.POLITE() else ""  # Optional, check for None
        account_spec = ctx.account_spec()
                
        account = account_spec.ACCOUNT_NAME().getText() if account_spec and account_spec.ACCOUNT_NAME() else current_user["username"]
        account_message = account_spec.ACCOUNT_NAME().getText() if account_spec and account_spec.ACCOUNT_NAME() else "your account"

        # database execution to add amount
        user_model = UserModel()
        update_amount = user_model.add_amount(account, float(amount))

        if update_amount is None:
            return {"intent": "TOPUP", "message": "Hmm, I couldn't add that amount. Could you try again?"}
        return {
            "intent": "TOPUP",
            "message": f"Great!\n\nYou have successfully topped up {amount} {currency} to {account_message}.\n\nCurrent total: {update_amount['amount']} $.\n\nThank you!"
        }

    def visitOrder(self, ctx: CommandParser.OrderContext):
        current_user = get_current_user()

        if not ctx.INTEGER():
            return {"intent": "ORDER", "message": "Yeah sure, please select directly from the menu!"}
        if not ctx.ITEM():
            return {"intent": "ORDER", "message": "Hmm, maybe you'd like to order something from the menu? Please check!"}

        amount = ctx.INTEGER().getText()
        
        # Validate that the amount is a whole number (no decimal point)
        if '.' in amount:
            return {"intent": "ORDER", "message": "Oops, the quantity should be a whole number!"}

        return {
            "intent": "ORDER",
            "message": f"You want to order {amount} of {ctx.ITEM().getText()}!"
        }