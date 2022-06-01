import os
from dotenv import load_dotenv, find_dotenv  # requires "dotenv"
import discord
from discord.ext import commands

# Tokens
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AUTHOR = os.getenv("AUTHOR")

# Establishes bot
intents = discord.Intents.default()
client = commands.Bot(command_prefix=',', intents=intents)

#============================================================#
# Functions
#============================================================#


def createEmbeded(title="", desc="", color=discord.Color.teal(), image=None, url=""):
    embed = discord.Embed(title=title, description=desc, color=color, url=url)
    if image is not None:
        embed.set_image(url=image)
    return embed

#============================================================#
# Custom Help Command
#============================================================#


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embeded = discord.Embed(
            title="__Help__", description="Provides help commands\nhelp\nhelp <category>\nhelp <command>", color=discord.Color.dark_teal())
        for cog in mapping:
            embeded.add_field(name=f'''{str(cog.qualified_name if cog != None else None)}''', value="\n".join(
                "> " + client.command_prefix + command.name for command in mapping[cog]), inline=False)
        await self.get_destination().send(embed=embeded)

    async def send_cog_help(self, cog):
        embeded = discord.Embed(
            title=f"__Help for '{cog.qualified_name}'__", color=discord.Color.dark_teal())
        embeded.add_field(name=f"{str(cog.qualified_name if cog != None else None)}", value="\n".join(
            "> " + client.command_prefix + command.name for command in cog.get_commands()), inline=False)
        await self.get_destination().send(embed=embeded)

    async def send_command_help(self, command):
        embeded = discord.Embed(
            title=f"__Help for '{command.name}'__", description=str(command.description), color=discord.Color.dark_teal())
        if(command.aliases != []):
            embeded.add_field(name="Aliases", value=", ".join(
                command.aliases), inline=False)
        embeded.add_field(name="Usage", value=(str(
            command.usage) if command.usage != None else "Just use by iteself"), inline=False)

        await self.get_destination().send(embed=embeded)


client.help_command = CustomHelpCommand()

#============================================================#
# Cog Commands
#============================================================#


@ client.command(name="load", description="Loads a cog")
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


@ client.command(name="unload", description="Unloads a cog")
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


@ client.command(name="reload", description="Reloads all cogs")
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


#============================================================#
# Events and other commands for cogs
#============================================================#

@ client.command(name="possibleCategories", description="Reloads all cogs")
async def possibleCategories(ctx):
    await ctx.send(embed=createEmbeded("Possible Categories", "\n".join([cog[:-3] for cog in os.listdir('./cogs') if cog.endswith('.py')]), discord.Color.dark_teal()))


@ client.command(name="cogs", description="Shows the cogs of the bot")
async def cogs(ctx):
    await ctx.send(f'{", ".join(client.cogs)}')


@ client.event
async def on_ready():
    # Server check
    for guild in client.guilds:
        print('{0.user} has connected to Discord '.format(
            client) + f'{guild.name}')
    print(f'Logged in as {client.user} ({client.user.id})')
    print('------------------------------------')


@ client.event
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
    elif(isinstance(error, commands.DisabledCommand)):
        await ctx.reply(f"{error}")
    else:
        await ctx.reply("An error has occurd\n" + str(error))

client.run(TOKEN)
