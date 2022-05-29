import discord
from discord.ext import commands
from bot import *


class Random_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping", description="Pings the bot")
    async def ping(self, ctx):
        await ctx.reply('pong')

    @commands.command(name="say", description="Says something the user enters")
    async def say(self, ctx, *arg):
        await ctx.send(" ".join(arg))
        await ctx.message.delete()

    @commands.command(name="add", description="Adds as many numbers together")
    async def add(self, ctx, *args):
        try:
            args = [float(i) for i in args]
            await ctx.send(f'The sum is {round(sum(args),4)}')
        except:
            await ctx.send('Please enter numbers only')

    #============================================================#
    # Utility Commands
    #============================================================#

    @commands.command(name="credits", description="Displays the credits of the bot")
    async def credits(self, ctx):
        embed = discord.Embed(
            title="Credits", description="This bot was made by Actronav and WokFriedE to do some random commands!", url="https://github.com/WokFriedE/Abyss-Bot-PY", color=discord.Color.dark_gold())
        await ctx.send(embed=embed)

    @commands.command(name="help", aliases=["h"], description="Shows the commands of the bot")
    async def help(self, ctx):
        helpText = ''
        for command in self.client.commands:
            helpText += f'{command.name}'
            if(command.aliases != []):
                helpText += f' [{", ".join(command.aliases)}]'
            helpText += f'\n{command.description}\n\n'
        await ctx.send(embed=createEmbeded(title="Help", desc=helpText, color=discord.Color.dark_teal()))


def setup(client):
    client.add_cog(Random_Commands(client))
