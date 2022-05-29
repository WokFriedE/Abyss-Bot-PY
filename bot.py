import discord  # requires "discord.py"
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv  # requires "dotenv"

import requests  # requires "requests"
from io import BytesIO
from PIL import Image  # requires "Pillow"
import asyncio

from github import Github  # requires "pyGithub"
import random


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
# Functions Commands
#============================================================#


def createEmbeded(title=None, desc=None, color=None, image=None, url=None):
    embed = discord.Embed(title=title, description=desc, color=color)
    if image is not None:
        embed.set_image(url=image)
    return embed


@client.event
async def on_ready():
    # Server check
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
            helpText += f' [{", ".join(command.aliases)}]'
        helpText += f'\n{command.description}\n\n'
    await ctx.send(embed=createEmbeded(title="Help", desc=helpText, color=discord.Color.dark_teal()))

#============================================================#
# Random Commands
#============================================================#


@client.command(name="ping", description="Pings the bot")
async def ping(ctx):
    await ctx.reply('pong')


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
# Random Github image Commands
#============================================================#

git = Github(GITHUB_TOKEN)
aghpbRepo = git.get_repo("cat-milk/Anime-Girls-Holding-Programming-Books")
gitList = []
gitList = [i.name for i in aghpbRepo.get_contents(
    "/") if i.type == "dir" and i.name not in gitList and i.name != "Uncategorized"]


@client.command(name="study",  aliases=['s'], description="Gets a random image from the Github repo")
async def study(ctx, *args):
    if len(args) > 1:
        await ctx.send("No more than one input allowed")
    elif len(args) < 1:
        fileSet = (aghpbRepo.get_contents(""))
        randImageSet = (aghpbRepo.get_contents(
            (fileSet[random.randrange(0, len(fileSet))]).name))
        await ctx.send(((randImageSet[random.randrange(0, len(randImageSet))]).html_url) + "?raw=true")
    else:
        for x in gitList:
            if x == args[0]:
                imageSet = (aghpbRepo.get_contents(args[0]))
                await ctx.send(((imageSet[random.randrange(0, len(imageSet))]).html_url) + "?raw=true")
                return True

        await ctx.send("Invalid study material, use .studymaterials or .sm to find valid ones")


@client.command(name="studymaterials",  aliases=['sm'], description="Lists the \"study materials\"")
async def studymaterials(ctx):
    text = "```" + "\n".join(gitList) + "```"
    await ctx.send(text)

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
        await ctx.send(embed=createEmbeded(title="Added Emoji", desc=f"The emoji: {emoji.name}, was successfully added!", color=discord.Color.green(), image=emoji.url))
    else:
        await ctx.send(embed=createEmbeded(title="Error", desc="This server does not support gifs", color=discord.Color.red()))
        return


@client.command(name="deleteEmoji", aliases=['de'], description="Removes an emote on the server")
async def deleteEmoji(ctx, emoji):

    def check(reaction, user):
        if(user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == msg.id):
            return True
        elif (user == ctx.author and str(reaction.emoji) == "❌" and reaction.message.id == msg.id):
            raise asyncio.TimeoutError("Cancelled")
    try:
        emoji = emoji.split(':')[2].strip('>')
        emojiDel = await ctx.guild.fetch_emoji(int(emoji))
        try:
            msg = await ctx.reply(embed=createEmbeded(title="Delete Emoji?", desc=f"Do you want to delete {emojiDel.name}", color=discord.Color.blurple(), image=emojiDel.url))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await client.wait_for(event='reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=createEmbeded(title="Timeout", desc="Sorry but you ran out of time to delete this emoji", color=discord.Color.red(), image=emojiDel.url))
            await msg.delete()
        else:
            await ctx.send(embed=createEmbeded(title="Deleted Emoji", desc="Deleted the emoji", color=discord.Color.green(), image=emojiDel.url))
            await msg.delete()
    except:
        await ctx.send(embed=createEmbeded(title="Error", desc="Invalid Emoji", color=discord.Color.red()))
        return


@client.command(name="getEmoji", aliases=['ge'], description="Gets the URL of an emote")
async def getEmoji(ctx, emoji):
    try:
        emoji = emoji.split(':')[2].strip('>')
        emoji = await ctx.guild.fetch_emoji(int(emoji))
    except:
        await ctx.send('Not an emoji on this server')
        return
    await ctx.send(embed=createEmbeded("Emoji", emoji.url, discord.Color.blue(), emoji.url))


@client.command(name="pollNewEmoji", description="Creates a poll to add an emote\npollNewEmoji (name) (emoji) (time)", aliases=['pne'])
async def pollNewEmoji(ctx, name="", emoji="", seconds="20"):
    if seconds == 0:
        await ctx.reply('Please provide a time')
        return

    if len(list(filter(lambda role: role.name == "emojiRole", ctx.author.roles))) == 0:
        await ctx.send('You do not have the required permissions')
        return

    votes = {"yes": [], "no": []}

    def check(reaction, user):
        if(user == ctx.author and str(reaction.emoji) == "💣"):
            return user == ctx.author and str(reaction.emoji) == "💣" and reaction.message.id == msg.id
        elif(user == ctx.author and str(reaction.emoji) == "🔚"):
            raise asyncio.TimeoutError("User ended poll")
        elif(str(reaction.emoji) == "✅" and user not in votes["yes"]):
            votes["yes"].append(user)
            if(user in votes["no"]):
                votes["no"].remove(user)
            return False
        elif(str(reaction.emoji) == "❌" and user not in votes["no"]):
            votes["no"].append(user)
            if(user in votes["yes"]):
                votes["yes"].remove(user)
            return False

    try:
        try:
            emoji = emoji.split(':')[2].strip('>')
            emoji = await ctx.guild.fetch_emoji(int(emoji))
            emoji = emoji.url
        except IndexError:
            if(emoji.lower().find('.png') == -1 and emoji.lower().find('.webp') == -1 and emoji.lower().find('.jpg') == -1):
                await ctx.send('Not an emoji that can be added')
                return

        msg = await ctx.send(embed=createEmbeded(f"Add the emoji '{name}'", f"Would you like to add '{name}' to the server?\n{ctx.author.mention} can exit the poll using 💣 or end it using 🔚", discord.Color.blurple(), emoji))
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("💣")
        await msg.add_reaction("🔚")
        await client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
    except ValueError:
        await ctx.send('Invalid time given')
        return
    except asyncio.TimeoutError:
        if len(votes["yes"]) > len(votes["no"]):
            await client.loop.create_task(newEmoji(ctx, name=name, item=emoji))
            await msg.delete()
        else:
            await msg.edit(embed=createEmbeded(f"Failed to add the emoji '{name}'", f"Poll majority was not yes for '{name}'", discord.Color.red(), emoji))
            await msg.clear_reactions()
            return
    else:
        await msg.edit(embed=createEmbeded(f"Add the emoji '{name}'", f"Poll was exited for {name}", discord.Color.orange(), emoji))
        return


@client.command(name="pollDeleteEmoji", description="Creates a poll to delete an emote\npollDeleteEmoji (emoji) (time)", aliases=['pde'])
async def pollNewEmoji(ctx, emoji="", seconds="20"):
    if seconds == 0:
        await ctx.reply('Please provide a time')
        return

    if len(list(filter(lambda role: role.name == "emojiRole", ctx.author.roles))) == 0:
        await ctx.send('You do not have the required permissions')
        return

    votes = {"yes": [], "no": []}

    def check(reaction, user):
        if(user == ctx.author and str(reaction.emoji) == "💣"):
            return user == ctx.author and str(reaction.emoji) == "💣" and reaction.message.id == msg.id
        elif(user == ctx.author and str(reaction.emoji) == "🔚"):
            raise asyncio.TimeoutError("User ended poll")
        elif(str(reaction.emoji) == "✅" and user not in votes["yes"]):
            votes["yes"].append(user)
            if(user in votes["no"]):
                votes["no"].remove(user)
            return False
        elif(str(reaction.emoji) == "❌" and user not in votes["no"]):
            votes["no"].append(user)
            if(user in votes["yes"]):
                votes["yes"].remove(user)
            return False

    try:
        try:
            emoji = emoji.split(':')[2].strip('>')
            emoji = await ctx.guild.fetch_emoji(int(emoji))
        except IndexError:
            await ctx.send('Not an emoji that can be deleted')
            return

        msg = await ctx.send(embed=createEmbeded(f"Remove the emoji '{emoji.name}'", f"Would you like to add '{emoji.name}' to the server?\n{ctx.author.mention} can exit the poll using 💣 or end it using 🔚", discord.Color.blurple(), emoji.url))
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("💣")
        await msg.add_reaction("🔚")
        await client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
    except ValueError:
        await ctx.send('Invalid time given')
        return
    except asyncio.TimeoutError:
        if len(votes["yes"]) > len(votes["no"]):
            # Vote logic if pass
            await client.loop.create_task(deleteEmoji(ctx, f'<:{emoji.name}:{emoji.id}>'))
            await msg.delete()
        else:
            # Vote logic if not yes
            await msg.edit(embed=createEmbeded(f"Failed to remove the emoji '{emoji.name}'", f"Poll majority was not yes for '{emoji.name}'", discord.Color.red(), emoji.url))
            await msg.clear_reactions()
            return
    else:
        # If force exited
        await msg.edit(embed=createEmbeded(f"Remove the emoji '{emoji.name}'", f"Poll was exited for {emoji.name}", discord.Color.orange(), emoji))
        return

#============================================================#
# Role Commands
#============================================================#


@client.command(name="role", description="Creates a role\nrole (name)", aliases=['r'])
async def role(ctx, name=""):
    if name == "":
        await ctx.send('Please provide a name')
        return

    ctx.guild.create_role(name=name)
    await ctx.send(embed=createEmbeded(f"Created role '{name}'", f"{ctx.author.mention} created role '{name}'", discord.Color.green()))


@client.command(name="roleEmojis", description="Gives someone the power to make emoji votes", aliases=['rE'])
async def role(ctx, user):
    if(not ctx.author.guild_permissions.manage_roles):
        await ctx.reply('You do not have the perms to use this command')
        return

    try:
        try:
            user = await ctx.guild.fetch_member(int(user.strip('<@>')))
        except:
            await ctx.send('Invalid user')
            return
        else:
            # adds role if doesnt exist
            if("emojiRole" not in [role.name for role in ctx.guild.roles]):
                await ctx.guild.create_role(name="emojiRole")

            # Checks if user has the role
            if(len(list(filter(lambda role: role.name == "emojiRole", user.roles))) == 0):
                await user.add_roles([role for role in ctx.guild.roles if role.name == "emojiRole"][0])
                await ctx.send(embed=createEmbeded(f"Gave {user.name} the perms for emojis", f"{ctx.author.mention} gave {user.mention} the power to make emoji votes", discord.Color.green()))
            else:
                await ctx.send(embed=createEmbeded(f"{user.name} already has the perms for emojis", f"{ctx.author.mention} tried to give {user.mention} the power to make emoji votes", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=createEmbeded(f"Failed to add {user.name} the perms for emojis", f"{ctx.author.mention} failed to add {user.mention} the power to make emoji votes", discord.Color.red()))
        print(e)
        return


@client.command(name="roleRemoveEmojis", description="Removes the power to make emoji votes", aliases=['rRE'])
async def role(ctx, user):
    if(not ctx.author.guild_permissions.manage_roles):
        await ctx.reply('You do not have the perms to use this command')
        return

    try:
        try:
            user = await ctx.guild.fetch_member(int(user.strip('<@>')))
            if(len(list(filter(lambda role: role.name == "emojiRole", user.roles))) == 0):
                await ctx.send(embed=createEmbeded(f"{user.name} does not have the role", f"{ctx.author.mention} tried to remove {user.mention} the power to make emoji votes", discord.Color.red()))
                return
        except:
            ctx.send(embed=createEmbeded(f"Error Removing {user.name} the perms for emojis",
                     f"{ctx.author.mention} failed to remove {user.mention} the power to make emoji votes", discord.Color.red()))
            return
        else:
            await user.remove_roles([role for role in ctx.guild.roles if role.name == "emojiRole"][0])
            await ctx.send(embed=createEmbeded(f"Removed {user.name} the perms for emojis", f"{ctx.author.mention} removed {user.mention} the power to make emoji votes", discord.Color.green()))
    except:
        await ctx.send(embed=createEmbeded(f"Failed to remove {user.name} the perms for emojis", f"{ctx.author.mention} failed to remove {user.mention} the power to make emoji votes", discord.Color.red()))
        return


@client.command(name="purgeRole", description="Purges a role", aliases=['pr'])
async def purgeRole(ctx, roleDel):
    if(not ctx.author.guild_permissions.manage_roles):
        await ctx.reply('You do not have the perms to use this command')
        return
    try:
        roleDel = ctx.guild.get_role(int(roleDel.strip('<@&>')))
    except Exception as e:
        await ctx.send(embed=createEmbeded(f"Failed to purge role", f"{ctx.author.mention} failed to purge role", discord.Color.red()))
        print(e)
        return
    else:
        await roleDel.delete()
        await ctx.send(embed=createEmbeded(f"Purged role", f"{ctx.author.mention} purged role", discord.Color.green()))

client.run(TOKEN)
