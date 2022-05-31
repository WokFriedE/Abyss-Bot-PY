import discord
from discord.ext import commands
from github import Github
import random
from bot import *
import os


class Github_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.git = Github(os.getenv('GITHUB_TOKEN'))
        self.aghpbRepo = self.git.get_repo(
            "cat-milk/Anime-Girls-Holding-Programming-Books")
        self.gitList = []
        self.gitList = [i.name for i in self.aghpbRepo.get_contents(
            "/") if i.type == "dir" and i.name not in self.gitList and i.name != "Uncategorized"]

    @commands.command(name="study",  aliases=['s'], description="Gets a random image from the Github repo", usage="study\nstudy <category>")
    async def study(self, ctx, *args):
        if len(args) > 1:
            await ctx.send("No more than one input allowed")
        elif len(args) < 1:
            fileSet = (self.aghpbRepo.get_contents(""))
            randImageSet = (self.aghpbRepo.get_contents(
                (fileSet[random.randrange(0, len(fileSet))]).name))
            image_url = (
                (randImageSet[random.randrange(0, len(randImageSet))]).html_url)
            await ctx.send(embed=createEmbeded(title="Random Image", desc="", color=discord.Color.blue(), image=(image_url + "?raw=true"), url=image_url))
        else:
            for x in self.gitList:
                if x == args[0]:
                    imageSet = (self.aghpbRepo.get_contents(args[0]))
                    image_url = (
                        (imageSet[random.randrange(0, len(imageSet))]).html_url)
                    await ctx.send(embed=createEmbeded(title="Random Image", desc=f"from {args[0]}", color=discord.Color.blue(), image=(image_url + "?raw=true"), url=image_url))
                    return True

            await ctx.send("Invalid study material, use .studymaterials or .sm to find valid ones")

    @commands.command(name="studymaterials",  aliases=['sm'], description="Lists the \"study materials\"", usage="studymaterials")
    async def studymaterials(self, ctx):
        text = "```" + "\n".join(self.gitList) + "```"
        await ctx.send(text)


def setup(client):
    client.add_cog(Github_Commands(client))
