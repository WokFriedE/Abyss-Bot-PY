import discord
from command import Command


#===============================================================#
# main function driver
#===============================================================#

async def main(m, PREFIX):
    # creates global variables
    global user_command
    global args
    global message
    message = m

    # assigns all the values for this function
    username = str(message.author).split("#")[0]
    user_command = str(message.content).split(" ")[0].strip(PREFIX)
    args = str(message.content).split(" ")[1:]
    channel = str(message.channel)
    print(f"{username} said: {user_command} in {channel}")

    commands = []
    # generates command
    commands.append(Command("ping", "pong", ping))
    commands.append(
        Command('help', 'returns a list of commands', help(commands)))
    commands.append(Command('say', 'returns a list of commands', say))
    commands.append(Command('add', 'returns a list of commands', add))

    print("Bot loaded", len(commands), "commands")

    # runs the commands
    for command in commands:
        await command.run()

#===============================================================#
# command definitions/functions
#===============================================================#


async def ping():
    if user_command.lower() == "ping" and len(args) == 0:
        await message.reply("pong")
        return


async def help(commands):
    if user_command.lower() == "help" and len(args) == 0:
        text = "```\n"
        for command in commands:
            text += f"{command.name}: {command.description}\n"
        text += '```'
        await message.channel.send(text)
        return


async def say():
    if user_command.lower() == "say" and len(args):
        await message.delete()
        text = " ".join(args)
        await message.channel.send(text)
        return


async def add():
    if user_command.lower() == "add":
        sum = 0
        try:
            for arg in args:
                sum += int(arg)
        except:
            await message.channel.send("Please enter numbers only")
            return
        await message.channel.send(f"Sum is {sum}")
        return
