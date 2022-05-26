import discord


async def commands(message, PREFIX):
    username = str(message.author).split("#")[0]
    # turns jaja#0000 to [jaja, 0000] and then [jaja]
    user_command = str(message.content).split(" ")[0].strip(PREFIX)
    args = str(message.content).split(" ")[1:]
    channel = str(message.channel)
    print(f"{username} said: {user_command} in {channel}")

    if user_command.lower() == "ping" and len(args) == 0:
        # ways to return a reply to a message
        # await message.channel.send("pong", reference=message)
        await message.reply("pong")
        return

    if user_command.lower() == "help" and len(args) == 0:
        await message.channel.send("ping\nhelp")
        return
