from discord import commands


async def main(message, PREFIX):
    username = str(message.author).split("#")[0]
    # turns jaja#0000 to [jaja, 0000] and then [jaja]
    user_command = str(message.content).split(" ")[0].strip(PREFIX)
    args = str(message.content).split(" ")[1:]
    channel = str(message.channel)
    print(f"{username} said: {user_command} in {channel}")

    commands = ['ping', 'help', 'say', 'add']

    if user_command.lower() == "ping" and len(args) == 0:
        # ways to return a reply to a message
        # await message.channel.send("pong", reference=message)
        await message.reply("pong")
        return

    elif user_command.lower() == "help" and len(args) == 0:
        text = "```\n" + "\n".join(commands) + '```'
        await message.channel.send(text)
        return

    elif user_command.lower() == "say" and len(args):
        await message.delete()
        text = " ".join(args)
        await message.channel.send(text)
        return

    elif user_command.lower() == "add":
        sum = 0
        try:
            for arg in args:
                sum += int(arg)
        except:
            await message.channel.send("Please enter numbers only")
            return
        await message.channel.send(f"Sum is {sum}")
        return
