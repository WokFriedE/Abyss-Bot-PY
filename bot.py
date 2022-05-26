from colorama import Fore
import discord
import os
from dotenv import load_dotenv, find_dotenv
from command_manager import commands

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
client = discord.Client()

valid_channels = ['general', 'tst']
PREFIX = "!"


@client.event
async def on_ready():
    print('{0.user} has connected to Discord'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or not(message.channel.name in valid_channels) or message.content.startswith(PREFIX):
        return

    await commands(message)

client.run(TOKEN)
