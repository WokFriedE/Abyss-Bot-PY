import discord
from discord.ext import commands
from bot import createEmbeded


class Roles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="role", description="Creates a role\nrole (name)", aliases=['r'], usage="role <name>")
    async def role(self, ctx, name=""):
        if name == "":
            await ctx.send('Please provide a name')
            return

        ctx.guild.create_role(name=name)
        await ctx.send(embed=createEmbeded(f"Created role '{name}'", f"{ctx.author.mention} created role '{name}'", discord.Color.green()))

    @commands.command(name="roleEmojis", description="Gives someone the power to make emoji votes", aliases=['rE'], usage="roleEmojis @<user>")
    @commands.has_permissions(manage_roles=True)
    async def roleEmojis(self, ctx, user):

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

    @commands.command(name="roleRemoveEmojis", description="Removes the power to make emoji votes", aliases=['rRE'], usage="roleRemoveEmojis @<user>")
    @commands.has_permissions(manage_roles=True)
    async def roleRemoveEmojis(self, ctx, user):
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

    @commands.command(name="purgeRole", description="Purges a role", aliases=['pr'], usage="purgeRole <role>")
    async def purgeRole(self, ctx, roleDel):
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


def setup(client):
    client.add_cog(Roles(client))
