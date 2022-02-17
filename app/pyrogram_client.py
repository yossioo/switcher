from pyrogram import Client, filters

app = Client("bot")


@app.on_message(filters.private)
async def hello(client, message):
    sender = message.from_user.first_name
    text = message.text
    print(f"Got message from {sender}:\n\t=> {text}")
    await message.reply("Hello from Pyrogram!")


app.run()
