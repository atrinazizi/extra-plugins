
from bing_image_urls import bing_image_urls
from config import BANNED_USERS
from ATMusic import app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto


@app.on_message(filters.command(["image"], prefixes=["/", "!", "."]) & ~BANNED_USERS)
async def image_from_bing(_, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("<b>give image name for search 🔍</b>")

    if message.reply_to_message and message.reply_to_message.text:
        query = message.reply_to_message.text
    else:
        query = " ".join(message.command[1:])

    messagesend = await message.reply_text("<b>🔍 searching for images...</b>")

    media_group = []
    for url in bing_image_urls(query, limit=6):
        media_group.append(InputMediaPhoto(media=url))
    await messagesend.edit(f"<b>uploading...</b>")
    try:
        await app.send_media_group(message.chat.id, media_group)
        await messagesend.delete()
    except Exception as e:
        await messagesend.edit(e)
