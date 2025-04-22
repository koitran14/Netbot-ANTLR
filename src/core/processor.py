from antlr4 import *
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        greeting = ctx.GREETING().getText()
        return {"intent": "GREETING", "message": f"Hi, what do you want? You said: {greeting}"} 

    def visitTopup(self, ctx: CommandParser.TopupContext):
        if not ctx.TOPUP_PREFIX():
            return {"intent": "TOPUP", "message":"Oops, it looks like you forgot to say how you'd like to top up! Try something like 'top up 50 usd'."}
       
        topup_prefix = ctx.TOPUP_PREFIX().getText()
        amount = ctx.AMOUNT().getText()
        
        if (not ctx.AMOUNT() or amount == "<missing AMOUNT>"):
            return {"intent": "TOPUP", "message":"Hmm, I need an amount to top up! Could you add something like '50' or '10.50'?"}

        try:
            float(amount)  # Ensure amount is a valid number
        except ValueError:
            return {"intent": "TOPUP", "message": f"Oh no, '{amount}' doesn't seem like a valid amount. Could you use a number like '50' or '10.50'?"}
        
    
        currency = ctx.CURRENCY().getText() if ctx.CURRENCY() else None  # Optional, check for None
        polite = ctx.POLITE().getText() if ctx.POLITE() else None  # Optional, check for None
        account_spec = ctx.account_spec()
        
        account = "my account"  # Default to user's account
        if account_spec:
            if account_spec.ACCOUNT_NAME():  # Named account
                account = account_spec.ACCOUNT_NAME().getText()
                
        return {"intent": "TOPUP", "message": f"You want to top up {amount} {currency}{account}{polite}!"}
    
    def visitOrder(self, ctx: CommandParser.OrderContext):
        if ctx.AMOUNT() is None:
            return {"intent": "order", "error": "Missing amount"}
        if ctx.ITEM() is None:
            return {"intent": "order", "error": "Missing item"}

        return {
            "intent": "ORDER",
            "message": f"You want to order {ctx.AMOUNT().getText()} of {ctx.ITEM().getText()}!"
        }