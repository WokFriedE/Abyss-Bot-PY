import discord
from discord.ext import commands
import asyncio


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

    @commands.command()
    async def test1(self, ctx):
        id = ctx.message.author.id
        guild = ctx.message.guild.id

        def check(reaction, user):
            if(user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == msg.id):
                return True

        msg = await ctx.send("Test 1")
        await msg.add_reaction("✅")

        try:
            await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
        else:
            await msg.remove_reaction("✅", ctx.author)
        print(type(ctx.author), id, self.client.get_guild(guild).get_member(id))


def setup(client):
    client.add_cog(Tests(client))
