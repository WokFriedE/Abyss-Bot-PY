import discord
from discord.ext import commands


class Tests(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Test cog is ready')

    @commands.command(name="test", aliases=['t'], description="Just a test command")
    async def test(self, ctx):
        # Get the command from another cog
        newEmoji = self.client.get_command("newEmoji")
        await self.client.loop.create_task(newEmoji(ctx, "test", "https://cdn.discordapp.com/emojis/431642989660471297.webp?size=80&quality=lossless"))
        message = await ctx.send("<:white_check_mark:979970509204770817>")


def setup(client):
    client.add_cog(Tests(client))
