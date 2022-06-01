import discord
from discord import app_commands
from discord.ext import commands


class Interact(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="tests", aliases=['t'], description="Just a test command")
    async def test(self, interaction: discord.Interaction, num: int):
        await interaction.response.send_message(f'test {num}')


async def setup(client):
    await client.add_cog(Interact(client))
