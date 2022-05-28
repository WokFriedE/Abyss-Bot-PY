from http.client import FORBIDDEN
import discord  # requires "discord.py"
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv  # requires "dotenv"

import requests  # requires "requests"
from io import BytesIO
from PIL import Image  # requires "Pillow"


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = commands.Bot(command_prefix=',', intents=intents)

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


@client.command(name="test", aliases=['t'])
async def test(ctx):
    print(client.emojis)


@client.command(name="newEmoji", aliases=['ne'])
async def newEmoji(ctx, name, item):
    response = requests.get(item)
    img = Image.open(BytesIO(response.content))

    try:
        img.seek(1)
    except EOFError:
        b = BytesIO()
        img.save(b, format="PNG")
        b_value = b.getvalue()
        emoji = await ctx.guild.create_custom_emoji(name=name, image=b_value)
        await ctx.send(f'created the emoji <:{name}:{emoji.id}>')
    else:
        await ctx.send('This server does not support gifs')
        return


@client.command(name="deleteEmoji", aliases=['e'])
async def deleteEmoji(ctx, emoji):
    if not ctx.author.guild_permissions.manage_emojis:
        await ctx.send('Invalid perms')
        return
    try:
        emoji = emoji.split(':')[2].strip('>')
        emojiDel = await ctx.guild.fetch_emoji(int(emoji))
        await ctx.send(f'deleted the emoji <:{emojiDel.name}:{emojiDel.id}>')
        await emojiDel.delete()
    except:
        await ctx.send('Not an emoji on this server')
        return


@client.command(name="getEmoji", aliases=['ge'])
async def getEmoji(ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)

client.run(TOKEN)
