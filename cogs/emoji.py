import discord
from discord.ext import commands
from bot import *

import requests  # requires "requests"
from io import BytesIO
from PIL import Image  # requires "Pillow"
import asyncio


class Emoji(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="newEmoji", aliases=['ne'], description="Adds a new emote to the server")
    async def newEmoji(self, ctx, name, item):
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

    @commands.command(name="deleteEmoji", aliases=['de'], description="Removes an emote on the server")
    async def deleteEmoji(self, ctx, emoji):

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
                await self.client.wait_for(event='reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(embed=createEmbeded(title="Timeout", desc="Sorry but you ran out of time to delete this emoji", color=discord.Color.red(), image=emojiDel.url))
                await msg.delete()
            else:
                await ctx.send(embed=createEmbeded(title="Deleted Emoji", desc="Deleted the emoji", color=discord.Color.green(), image=emojiDel.url))
                await msg.delete()
        except:
            await ctx.send(embed=createEmbeded(title="Error", desc="Invalid Emoji", color=discord.Color.red()))
            return

    @commands.command(name="getEmoji", aliases=['ge'], description="Gets the URL of an emote")
    async def getEmoji(self, ctx, emoji):
        try:
            emoji = emoji.split(':')[2].strip('>')
            emoji = await ctx.guild.fetch_emoji(int(emoji))
        except:
            await ctx.send('Not an emoji on this server')
            return
        await ctx.send(embed=createEmbeded("Emoji", emoji.url, discord.Color.blue(), emoji.url))

    @commands.command(name="pollNewEmoji", description="Creates a poll to add an emote\npollNewEmoji (name) (emoji) (time)", aliases=['pne'])
    async def pollNewEmoji(self, ctx, name="", emoji="", seconds="20"):
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
            await self.client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
        except ValueError:
            await ctx.send('Invalid time given')
            return
        except asyncio.TimeoutError:
            if len(votes["yes"]) > len(votes["no"]):
                await self.client.loop.create_task(self.newEmoji(ctx, name=name, item=emoji))
                await msg.delete()
            else:
                await msg.edit(embed=createEmbeded(f"Failed to add the emoji '{name}'", f"Poll majority was not yes for '{name}'", discord.Color.red(), emoji))
                await msg.clear_reactions()
                return
        else:
            await msg.edit(embed=createEmbeded(f"Add the emoji '{name}'", f"Poll was exited for {name}", discord.Color.orange(), emoji))
            return

    @commands.command(name="pollDeleteEmoji", description="Creates a poll to delete an emote\npollDeleteEmoji (emoji) (time)", aliases=['pde'])
    async def pollNewEmoji(self, ctx, emoji="", seconds="20"):
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
            await self.client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
        except ValueError:
            await ctx.send('Invalid time given')
            return
        except asyncio.TimeoutError:
            if len(votes["yes"]) > len(votes["no"]):
                # Vote logic if pass
                await self.client.loop.create_task(self.deleteEmoji(ctx, f'<:{emoji.name}:{emoji.id}>'))
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


def setup(client):
    client.add_cog(Emoji(client))
