import discord
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv
from github import Github
import random

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents=intents)

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

client.run(TOKEN)
