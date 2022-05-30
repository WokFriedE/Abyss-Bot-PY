import discord  # requires "discord.py"
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv  # requires "dotenv"


# Tokens
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AUTHOR = os.getenv("AUTHOR")

# Establishes bot
intents = discord.Intents.default()
client = commands.Bot(command_prefix=',', intents=intents, help_command=None)

#============================================================#
# Functions
#============================================================#


def createEmbeded(title="", desc="", color=discord.Color.teal(), image=None, url=""):
    embed = discord.Embed(title=title, description=desc, color=color, url=url)
    if image is not None:
        embed.set_image(url=image)
    return embed

#============================================================#
# Initialization Code
#============================================================#


@client.command()
async def load(ctx, extension):
    if(not ctx.author.guild_permissions.administrator):
        await ctx.reply("You do not have permission to use this command.")
        return
    extension = extension.lower()
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}')
    except:
        await ctx.send(f'Could not load {extension}')


@client.command()
async def unload(ctx, extension):
    if(not ctx.author.guild_permissions.administrator):
        await ctx.reply("You do not have permission to use this command.")
        return
    extension = extension.lower()
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}')
    except:
        await ctx.send(f'Could not unload {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command(name="reload", description="Reloads all cogs")
async def reload(ctx):
    if(not ctx.author.guild_permissions.administrator):
        await ctx.reply("You do not have permission to use this command.")
        return
    for filename in os.listdir('./cogs'):
        try:
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
        except:
            continue
    await ctx.send('Reloaded all cogs')


@client.command(name="possibleCategories", description="Reloads all cogs")
async def possibleCategories(ctx):
    await ctx.send(embed=createEmbeded("Possible Categories", "\n".join([cog[:-3] for cog in os.listdir('./cogs') if cog.endswith('.py')]), discord.Color.dark_teal()))


@client.event
async def on_ready():
    # Server check
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print('{0.user} has connected to Discord '.format(client) + f'{guild.name}')


@client.command(name="cogs", description="Shows the cogs of the bot")
async def cogs(ctx):
    await ctx.send(f'{", ".join(client.cogs)}')


@client.event
async def on_command_error(ctx, error):
    if(isinstance(error, commands.CommandNotFound)):
        await ctx.reply("Command not found.")
    elif(isinstance(error, commands.MissingRequiredArgument)):
        await ctx.reply("Missing required argument.")
    elif(isinstance(error, commands.TooManyArguments)):
        await ctx.reply("Too many arguments.")
    elif(isinstance(error, commands.BadArgument)):
        await ctx.reply("Bad argument.")
    elif(isinstance(error, commands.CheckFailure)):
        await ctx.reply(f"{error}")
    else:
        await ctx.reply("An error has occurd\n" + error)

client.run(TOKEN)
