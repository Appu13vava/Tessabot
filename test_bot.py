from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

API_ID = 15917107
API_HASH = "8197e7638d58c92ae2504adba7c62117"
BOT_TOKEN = "7522921582:AAGkAbGufO0D0NRcwmxdXGgluCX0BtwgWs0"

app = Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_sticker("CAACAgUAAxkBAAEBVfFlnTD9i4c5DRM8K6MQN2aFFoyZuAACAwEAAvcCyFYybAIKq8ZECzQE")
    await message.reply_text(
        text=f"Hello {message.from_user.first_name}! I'm alive and ready to help.",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Help", callback_data="help"),
                InlineKeyboardButton("About", callback_data="about")
            ]]
        )
    )

@app.on_callback_query()
async def cb_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        await callback_query.message.edit_text("Help message here", reply_markup=None)
    elif data == "about":
        await callback_query.message.edit_text("About message here", reply_markup=None)
    await callback_query.answer()

async def main():
    await app.start()
    print("Bot started!")
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
