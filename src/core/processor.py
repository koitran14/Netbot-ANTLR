from antlr4 import *
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser

class CommandProcessor(CommandVisitor):
    def visitCommand(self, ctx: CommandParser.CommandContext):
        if ctx.order():
            return self.visitOrder(ctx.order())
        elif ctx.topup():
            return self.visitTopup(ctx.topup())
        elif ctx.greeting():
            return self.visitGreeting(ctx.greeting(0))  # Nếu chỉ greeting
        else:
            return {"intent": "unknown"}

    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        return {
            "intent": "greeting",
            "greeting": self._get_optional_text(ctx.GREETING())
        }

    def visitTopup(self, ctx: CommandParser.TopupContext):
        if ctx.AMOUNT() is None:
            return {"intent": "topup", "error": "Missing amount"}
        
        return {
            "intent": "topup",
            "topup_prefix": self._get_optional_text(ctx.TOPUP_PREFIX()),
            "amount": ctx.AMOUNT().getText(),
            "currency": self._get_optional_text(ctx.CURRENCY()),
            "polite": self._get_optional_text(ctx.POLITE())
        }

    def visitOrder(self, ctx: CommandParser.OrderContext):
        if ctx.AMOUNT() is None:
            return {"intent": "order", "error": "Missing amount"}
        if ctx.ITEM() is None:
            return {"intent": "order", "error": "Missing item"}

        return {
            "intent": "order",
            "order_prefix": self._get_optional_text(ctx.ORDER_PREFIX()),
            "amount": ctx.AMOUNT().getText(),
            "item": ctx.ITEM().getText(),
            "polite": self._get_optional_text(ctx.POLITE())
        }

    def _get_optional_text(self, token):
        return token.getText() if token else None
