import discord


class Command:
    def __init__(self, name, description, function):
        self.name = name
        self.description = description
        self.functionRun = function

    async def run(self):
        await self.functionRun()
