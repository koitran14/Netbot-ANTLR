import sys
import os
from antlr4 import * 
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser

class CommandProcessor(CommandVisitor):
    def visitGreeting(self, ctx: CommandParser.GreetingContext):
        greeting = ctx.GREETING().getText()
        return {"intent": "greeting", "greeting": greeting }

    def visitTopup(self, ctx: CommandParser.TopupContext):
        topup_prefix = ctx.TOPUP_PREFIX().getText()
        amount = ctx.AMOUNT().getText()
        currency = ctx.CURRENCY().getText() if ctx.CURRENCY() else None  # Optional, check for None
        polite = ctx.POLITE().getText() if ctx.POLITE() else None  # Optional, check for None
        account_spec = ctx.account_spec()
        account = "my account"  # Default to user's account
        if account_spec:
            if account_spec.ACCOUNT_NAME():  # Named account
                account = account_spec.ACCOUNT_NAME().getText()
        return {
            "intent": "topup",
            "topup_prefix": topup_prefix,
            "amount": amount,
            "currency": currency,
            "polite": polite,
            "account": account,
        }