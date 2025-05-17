from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot()  # Make sure this comes before the handlers

# Start menu buttons
def start_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help"),
         InlineKeyboardButton("About", callback_data="about")]
    ])

# /start command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    try:
        await message.reply_sticker("CAACAgUAAxkBAAEBVfFlnTD9i4c5DRM8K6MQN2aFFoyZuAACAwEAAvcCyFYybAIKq8ZECzQE")
        await message.reply_text(
            text=f"Hello <b>{message.from_user.first_name}</b>!\nI'm alive and ready to help.",
            reply_markup=start_markup(),
            parse_mode="html"
        )
    except Exception as e:
        print(f"Error in /start: {e}")

# Callback query handler
@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "help":
        await callback_query.message.edit_text(
            "Here is how you can use me:\n\n"
            "/start - Show welcome message\n"
            "/help - Show this help message\n"
            "/about - About the bot",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="back")]
            ])
        )

    elif data == "about":
        await callback_query.message.edit_text(
            "🤖 <b>Tessabot</b>\n"
            "A powerful autofilter Telegram bot.\n\n"
            "Developer: <a href='https://github.com/Appu13vava'>Appu13vava</a>\n"
            "Version: 1.0\n"
            "License: GNU GPLv2",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="back")]
            ])
        )

    elif data == "back":
        await callback_query.message.edit_text(
            text=f"Hello <b>{callback_query.from_user.first_name}</b>!\nI'm alive and ready to help.",
            reply_markup=start_markup(),
            parse_mode="html"
        )

    await callback_query.answer()
