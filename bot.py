from turtle import title
from unicodedata import name
import discord  # requires "discord.py"
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv  # requires "dotenv"

import requests  # requires "requests"
from io import BytesIO
from PIL import Image  # requires "Pillow"
import asyncio

from github import Github
import random


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = commands.Bot(command_prefix=',', intents=intents, help_command=None)



@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print('{0.user} has connected to Discord '.format(client) + f'{guild.name}')

#============================================================#
# Utility Commands
#============================================================#


@client.command(name="credits", description="Displays the credits of the bot")
async def credits(ctx):
    embed = discord.Embed(
        title="Credits", description="This bot was made by Actronav and WokFriedE to do some random commands!", url="https://github.com/WokFriedE/Abyss-Bot-PY", color=discord.Color.dark_gold())
    await ctx.send(embed=embed)


@client.command(name="help", aliases=["h"], description="Shows the commands of the bot")
async def help(ctx):
    helpText = ''
    for command in client.commands:
        helpText += f'{command.name}'
        if(command.aliases != []):
            helpText += f' ({", ".join(command.aliases)})'
        helpText += f'\n{command.description}\n\n'
    embed = discord.Embed(title="Help", description=helpText,
                          color=discord.Color.dark_teal())
    await ctx.send(embed=embed)

#============================================================#
# Random Commands
#============================================================#


@client.command(name="ping", description="Pings the bot")
async def ping(ctx):
    await ctx.reply('pong')

@client.command()
async def test(ctx):
    await ctx.reply("a")

git = Github("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")
aghpbRepo = git.get_repo("cat-milk/Anime-Girls-Holding-Programming-Books")
list = ['AI', 'APL', 'ASM', 'Ada', 'Agda', 'Algorithms', 'Architecture', 'Beef', 'C#', 'C++', 'C', 'CSS', 'Cobol', 'Compilers', 'D', 'Dart', 'Delphi', 'Design Patterns', 'Editors', 'Elixir', 'Elm', 'F#', 'FORTH', 'Fortran', 'GDScript', 'Go', 'Haskell', 'HoTT', 'HolyC', 'Idris', 'Java', 'Javascript', 'Kotlin', 'Lisp', 'Lua', 'Math', 'Memes', 'Mixed', 'MongoDB', 'Nim', 'OCaml', 'Objective-C', 'Other', 'PHP', 'Perl', 'Personification', 'Prolog', 'Python', 'Quantum Computing', 'R', 'Racket', 'RayTracing', 'ReCT', 'Regex', 'Ruby', 'Rust', 'SICP', 'SQL', 'Scala', 'Shell', 'Smalltalk', 'Solidity', 'Swift', 'Systems', 'Typescript', 'Uncategorized', 'Unity', 'Unreal', 'V', 'VHDL', 'Verilog', 'Visual Basic', 'WebGL']

@client.command(name="study",  aliases=['s'])
async def study(ctx, *args):
    if len(args) > 1:
       await ctx.send("No more than one input allowed")
    elif len(args) < 1:
        fileSet = (aghpbRepo.get_contents(""))
        randImageSet = (aghpbRepo.get_contents((fileSet[random.randrange(0, len(fileSet))]).name) )
        await ctx.send(((randImageSet[random.randrange(0,len(randImageSet))]).html_url)  + "?raw=true")
    else:
        for x in list:
           if x == args[0]:
               imageSet = (aghpbRepo.get_contents(args[0]))
               await ctx.send(((imageSet[random.randrange(0, len(imageSet))]).html_url) + "?raw=true")
               return True

        await ctx.send("Invalid study material, use .studymaterials or .sm to find valid ones")

@client.command(name="studymaterials",  aliases=['sm'])
async def studymaterials(ctx):
    text = "```" + "\n".join(list) + "```"
    await ctx.send(text)

@client.command(name="say", description="Says something the user enters")
async def say(ctx, *arg):
    await ctx.send(" ".join(arg))
    await ctx.message.delete()

@client.command(name="add", description="Adds as many numbers together")
async def add(ctx, *args):
    try:
        args = [float(i) for i in args]
        await ctx.send(f'The sum is {round(sum(args),4)}')
    except:
        await ctx.send('Please enter numbers only')


@client.command(name="test", aliases=['t'], description="Just a test command")
async def test(ctx):
    print(client.emojis)
    await client.loop.create_task(newEmoji(ctx, "test", "https://cdn.discordapp.com/emojis/431642989660471297.webp?size=80&quality=lossless"))
    message = await ctx.send("<:white_check_mark:979970509204770817>")

#============================================================#
# Emote Commands
#============================================================#


@client.command(name="newEmoji", aliases=['ne'], description="Adds a new emote to the server")
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


@client.command(name="deleteEmoji", aliases=['e'], description="Removes an emote on the server")
async def deleteEmoji(ctx, emoji):
    if not ctx.author.guild_permissions.manage_emojis:
        await ctx.send('Invalid perms')
        return

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id

    try:
        emoji = emoji.split(':')[2].strip('>')
        emojiDel = await ctx.guild.fetch_emoji(int(emoji))
        try:
            message = await ctx.reply(f'Would you like to delete {emojiDel}')
            await message.add_reaction("✅")
            await client.wait_for(event='reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Invalid Timing')
        else:
            await ctx.send(f'deleted the emoji <:{emojiDel.name}:{emojiDel.id}>')
            await message.delete()
            await emojiDel.delete()
    except:
        await ctx.send('Not an emoji on this server')
        return


@ client.command(name="getEmoji", aliases=['ge'], description="Gets the URL of an emote")
async def getEmoji(ctx, emoji):
    try:
        emoji = emoji.split(':')[2].strip('>')
        emoji = await ctx.guild.fetch_emoji(int(emoji))
    except:
        await ctx.send('Not an emoji on this server')
        return
    await ctx.send(f'```{emoji.url}```')
    await ctx.send(emoji.url)

client.run(TOKEN)
