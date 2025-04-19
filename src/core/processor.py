import sys
import os
from antlr4 import * 
from src.generated.CommandVisitor import CommandVisitor
from src.generated.CommandParser import CommandParser

class CommandProcessor(CommandVisitor):
    def visitSchedule(self, ctx: CommandParser.ScheduleContext):
        day = ctx.day().getText()
        time = ctx.time().getText()
        return {"intent": "schedule", "day": day, "time": time}

    def visitCancel(self, ctx: CommandParser.CancelContext):
        day = ctx.day().getText()
        return {"intent": "cancel", "day": day}