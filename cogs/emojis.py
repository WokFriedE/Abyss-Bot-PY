import discord
from discord.ext import commands
from bot import *

import requests  # requires "requests"
from io import BytesIO
from PIL import Image  # requires "Pillow"
import asyncio


class Emojis(commands.Cog):
    __requireRole = True

    def __init__(self, client):
        self.client = client
        self.polls = {}

    #============================================================#
    # Functions for emojis
    #============================================================#

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
        finally:
            if msg.id in self.polls:
                self.polls.pop(msg.id)

    #============================================================#
    # Simple add, remove, get emojis
    #============================================================#

    @commands.command(name="addEmoji", aliases=['addE'], description="Adds a new emote to the server")
    @commands.has_permissions(manage_emojis=True)
    async def addEmoji(self, ctx, name, emoji):
        await self.newEmoji(ctx, name, emoji)

    @commands.command(name="removeEmoji", aliases=['removeE'], description="Removes an emote on the server")
    @commands.has_permissions(manage_emojis=True)
    async def remove_emoji(self, ctx, name, emoji):
        await self.deleteEmoji(ctx, name, emoji)

    @commands.command(name="getEmoji", aliases=['ge'], description="Gets the URL of an emote")
    async def getEmoji(self, ctx, emoji):
        try:
            emoji = emoji.split(':')[2].strip('>')
            emoji = await ctx.guild.fetch_emoji(int(emoji))
        except:
            await ctx.send('Not an emoji on this server')
            return
        await ctx.send(embed=createEmbeded("Emoji", emoji.url, discord.Color.blue(), emoji.url))

    @commands.command()
    async def checkPolls(self, ctx):
        await ctx.send(self.polls)

    #============================================================#
    # Polling commands for adding and removing emojis
    #============================================================#

    @commands.command(name="pollNewEmoji", description="Creates a poll to add an emote\npollNewEmoji (name) (emoji) (time: optional)", aliases=['pne'])
    @commands.has_role("emojiRole" if __requireRole else "")
    async def pollNewEmoji(self, ctx, name="", emoji="", seconds="20"):
        if seconds == 0:
            await ctx.reply('Please provide a time')
            return

        def check(reaction, user):
            if(user == ctx.author and str(reaction.emoji) == "💣"):
                return user == ctx.author and str(reaction.emoji) == "💣" and reaction.message.id == msg.id
            elif(user == ctx.author and str(reaction.emoji) == "🔚"):
                raise asyncio.TimeoutError("User ended poll")

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
            self.polls[msg.id] = {'yes': [], 'no': []}
            await self.client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
        except ValueError:
            await ctx.send('Invalid time given')
            return
        except asyncio.TimeoutError:
            if len(self.polls[msg.id]["yes"]) > len(self.polls[msg.id]["no"]):
                await self.client.loop.create_task(self.newEmoji(ctx, name=name, item=emoji))
                await msg.delete()
            else:
                await msg.edit(embed=createEmbeded(f"Failed to add the emoji '{name}'", f"Poll majority was not yes for '{name}'", discord.Color.red(), emoji.url))
                await msg.clear_reactions()
                return
        else:
            await msg.edit(embed=createEmbeded(f"Add the emoji '{name}'", f"Poll was exited for {name}", discord.Color.orange(), emoji.url))
            await msg.clear_reactions()
            return
        finally:
            if msg.id in self.polls:
                self.polls.pop(msg.id)

    @commands.command(name="pollDeleteEmoji", description="Creates a poll to delete an emote\npollDeleteEmoji (emoji) (time: optional)", aliases=['pde'])
    @commands.has_role("emojiRole" if __requireRole else "")
    async def pollDeleteEmoji(self, ctx, emoji="", seconds="20"):
        if seconds == 0:
            await ctx.reply('Please provide a time')
            return

        def check(reaction, user):
            if(user == ctx.author and str(reaction.emoji) == "💣"):
                return user == ctx.author and str(reaction.emoji) == "💣" and reaction.message.id == msg.id
            elif(user == ctx.author and str(reaction.emoji) == "🔚"):
                raise asyncio.TimeoutError("User ended poll")

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
            self.polls[msg.id] = {'yes': [], 'no': []}
            await self.client.wait_for(event="reaction_add", check=check, timeout=float(seconds))
        except ValueError:
            await ctx.send('Invalid time given')
            return
        except asyncio.TimeoutError:
            if len(self.polls[msg.id]["yes"]) > len(self.polls[msg.id]["no"]):
                # Vote logic if pass
                await self.client.loop.create_task(self.deleteEmoji(ctx, f'<:{emoji.name}:{emoji.id}>'))
                await msg.delete()
                return
            else:
                # Vote logic if not yes
                await msg.edit(embed=createEmbeded(f"Failed to remove the emoji '{emoji.name}'", f"Poll majority was not yes for '{emoji.name}'", discord.Color.red(), emoji.url))
                await msg.clear_reactions()
                return
        else:
            # If force exited
            await msg.edit(embed=createEmbeded(f"Remove the emoji '{emoji.name}'", f"Poll was exited for {emoji.name}", discord.Color.orange(), emoji.url))
            await msg.clear_reactions()
            return
        finally:
            if msg.id in self.polls:
                self.polls.pop(msg.id)

    #============================================================#
    # Listeners for reactions to polls
    #============================================================#

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.client.get_user(payload.user_id):
            return

        if payload.message_id in self.polls:
            channel = self.client.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            if str(payload.emoji) == "✅":
                self.polls[payload.message_id]["yes"].append(payload.user_id)
                if(payload.user_id in self.polls[payload.message_id]["no"]):
                    await msg.remove_reaction("❌", payload.member)
            elif str(payload.emoji) == "❌":
                self.polls[payload.message_id]["no"].append(payload.user_id)
                if(payload.user_id in self.polls[payload.message_id]["yes"]):
                    await msg.remove_reaction("✅", payload.member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if self.client.get_user(payload.user_id):
            return

        if payload.message_id in self.polls:
            if str(payload.emoji) == "✅":
                self.polls[payload.message_id]["yes"].remove(payload.user_id)
            elif str(payload.emoji) == "❌":
                self.polls[payload.message_id]["no"].remove(payload.user_id)


def setup(client):
    client.add_cog(Emojis(client))
