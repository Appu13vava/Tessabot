from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start(client, message):
    # Send a sticker first
    await message.reply_sticker("CAACAgUAAxkBAAEBVfFlnTD9i4c5DRM8K6MQN2aFFoyZuAACAwEAAvcCyFYybAIKq8ZECzQE")

    # Send a welcome message with inline buttons
    await message.reply_text(
        text=f"Hello **{message.from_user.first_name}**!\nI'm alive and ready to help.",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Help", callback_data="help"),
                InlineKeyboardButton("About", callback_data="about")
            ]]
        )
    )
