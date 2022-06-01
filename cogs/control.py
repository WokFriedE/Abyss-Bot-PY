from cgitb import enable
import discord
from discord.ext import commands
from bot import *
import os
import json


class Control(commands.Cog):
    __required_roles = True
    __have_whitelist = False

    def __init__(self, client):
        self.client = client
        self.json_info = {}

    def updateSettings(self):
        with open("settings.json", "r") as f:
            self.json_info = json.load(f)
        f.close()

    def saveSettings(self):
        with open("settings.json", "w") as f:
            json.dump(self.json_info, f)
        f.close()

    def getWhitelist(self, guild):
        self.updateSettings()
        return self.json_info[str(guild.id)]["whitelist"]

    @commands.Cog.listener()
    async def on_ready(self):
        if(not os.path.exists("settings.json")):
            with open("settings.json", "w") as f:
                for guild in self.client.guilds:
                    self.json_info[str(guild.id)] = {
                        "haveWhitelist": False,
                        "whitelist": [],
                        "requireRoles": True
                    }
                json.dump(self.json_info, f)
            f.close()
            print("Created settings.json")
        elif(os.path.exists("settings.json")):
            with open("settings.json", "r") as f:
                self.json_info = json.load(f)
            f.close()

            for guild in self.client.guilds:
                if (str(guild.id) not in self.json_info):
                    x = str(guild.id)
                    self.json_info[str(guild.id)] = {
                        "haveWhitelist": False,
                        "whitelist": [],
                        "requireRoles": True
                    }
            self.saveSettings()
            print("Loaded settings.json")

    @commands.command(name="set", description="Sets a setting for the bot", usage="set <setting: requireRole/requireWhitelist>")
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, setting=""):
        info = self.json_info[str(ctx.guild.id)]
        if setting == "requireRoles":
            info["requireRoles"] = not self.json_info[str(
                ctx.guild.id)]["requireRoles"]
            await ctx.send("Require roles is now " + "enabled" if info["requireRoles"] else "disabled")
        elif setting == "requireWhitelist":
            info["haveWhitelist"] = not self.json_info[str(
                ctx.guild.id)]["haveWhitelist"]
            await ctx.send("Whitelist is now " + "enabled" if info["haveWhitelist"] else "disabled")
        elif setting == "":
            await ctx.send("Please specify a setting: `requireRoles`, `requireWhitelist`")
            return
        else:
            await ctx.send("An error has occured")
            return
        self.saveSettings()

        global __have_whitelist
        __have_whitelist = info["haveWhitelist"]

    @commands.command(name="checkSettings", description="displays the settings of the bot")
    async def checkSettings(self, ctx):
        self.updateSettings()
        info = self.json_info[str(ctx.guild.id)]

        embeded = discord.Embed(
            title="Settings", description="These are the settings for the bot", color=discord.Color.dark_teal())
        embeded.add_field(name="Require roles for emoji votes",
                          value="Enabled" if info["requireRoles"] else "Disabled")
        whitelist_info = "Enabled" if info["haveWhitelist"] else "Disabled"
        for channel in info["whitelist"]:
            if(channel not in ctx.guild.channels):
                whitelist_info += "\n" + channel + " (Channel not found)"
            whitelist_info += f"\n{ctx.guild.get_channel(int(channel)).name}: {str(channel)}"
        embeded.add_field(name="Require channel whitelist for emoji votes",
                          value=whitelist_info)
        await ctx.send(embed=embeded)

    @commands.command(name="addChannelEmoji", aliases=["ace"], description="Adds a channel to emoji polling, uses current channel", usage="addChannelEmoji", enabled=__have_whitelist)
    @commands.has_permissions(manage_channels=True)
    async def addChannelEmoji(self, ctx):
        info = self.json_info[str(ctx.guild.id)]["whitelist"]

        if(str(ctx.channel.id) in info):
            await ctx.reply(f"{ctx.channel.name} is in the whitelist")
            return

        self.updateSettings()
        info.append(str(ctx.channel.id))
        self.json_info[str(ctx.guild.id)]["whitelist"] = info
        self.saveSettings()
        await ctx.reply(f"{ctx.channel.name} added from whitelist")

    @commands.command(name="removeChannelEmoji", aliases=["rce"], description="Removes a channel to emoji polling, uses current channel", usage="addChannelEmoji", enabled=__have_whitelist)
    @commands.has_permissions(manage_channels=True)
    async def removeChannelEmoji(self, ctx):
        info = self.json_info[str(ctx.guild.id)]["whitelist"]

        if(str(ctx.channel.id) not in info):
            await ctx.reply(f"{ctx.channel.name} is not in the whitelist")
            return

        self.updateSettings()
        info.remove(str(ctx.channel.id))
        self.json_info[str(ctx.guild.id)]["whitelist"] = info
        self.saveSettings()
        await ctx.reply(f"{ctx.channel.name} removed from whitelist")

    @commands.command(name="clearWhitelist", aliases=["clrw"], description="Checks the whitelist", usage="checkWhitelist", enabled=__have_whitelist)
    @commands.has_permissions(manage_channels=True)
    async def clearWhitelist(self, ctx):
        info = self.getWhitelist(ctx.guild)
        info.clear()
        self.json_info[str(ctx.guild.id)]["whitelist"] = info
        self.saveSettings()
        await ctx.reply(f"Whitelist cleared for {ctx.guild.name}")
        return


def setup(client):
    client.add_cog(Control(client))
