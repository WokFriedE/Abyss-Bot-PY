from colorama import Fore
import discord
import os
from dotenv import load_dotenv, find_dotenv
from command_manager import commands

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD_ID")

client = discord.Client()

valid_channels = ['general', 'tst']
PREFIX = "!"


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print('{0.user} has connected to Discord '.format(client) + f'{guild.name}')


@client.event
async def on_message(message):
    if message.author == client.user or not(message.channel.name in valid_channels) or not(message.content.startswith(PREFIX)):
        return

    await commands(message, PREFIX)

client.run(TOKEN)
