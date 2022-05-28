import discord
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

valid_channels = ['general', 'tst']


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print('{0.user} has connected to Discord '.format(client) + f'{guild.name}')


@client.command()
async def ping(ctx):
    await ctx.reply('pong')


@client.command()
async def say(ctx, *arg):
    await ctx.send(" ".join(arg))
    await ctx.message.delete()


@client.command()
async def add(ctx, *args):
    try:
        args = [int(i) for i in args]
        await ctx.send(f'The sum is {sum(args)}')
    except:
        await ctx.send('Please enter numbers only')


client.run(TOKEN)
