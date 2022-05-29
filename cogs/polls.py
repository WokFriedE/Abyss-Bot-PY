from http import client
import discord
from discord.ext import commands


class Polls():
    def __init__(self, client):
        self.client = client

    @commands.command(name="poll", description="Creates a poll")
    async def poll(self, ctx, question, content, *emojis):
        if(len(emojis) < 2):
            await ctx.send("You need at least two options")
            return
        if(all([emoji for emoji in emojis])):
            print("hi")


def setup(client):
    client.add_cog(Polls(client))
