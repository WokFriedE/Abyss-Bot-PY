import discord
from discord.ext import commands
import requests


class MAL(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(MAL(client))
