import discord


async def commands(message):
    username = str(message.author).split("#")[0]
    # turns jaja#0000 to [jaja, 0000] and then [jaja]
    user_message = str(message.content)
    channel = str(message.channel)
    print(f"{username} said: {user_message} in {channel}")

    if user_message.lower() == "ping":
        # ways to return a reply to a message
        # await message.channel.send("pong", reference=message)
        await message.reply("pong")
        return

    if user_message.lower() == "help":
        await message.channel.send("ping\nhelp")
        return
