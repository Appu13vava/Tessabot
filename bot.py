import os
import math
import logging
import datetime
import pytz
import logging.config
import asyncio

from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from database.ia_filterdb import Media
from typing import Union, Optional, AsyncGenerator
from utils import temp, __repo__, __license__, __copyright__, __version__
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, UPTIME, WEB_SUPPORT, LOG_MSG

# Configure logging
logging.config.fileConfig("logging.conf")
logging.getLogger(__name__).setLevel(logging.INFO)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Professor-Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats        

        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.id = me.id
        self.name = me.first_name
        self.mention = me.mention
        self.username = me.username
        self.log_channel = LOG_CHANNEL
        self.uptime = UPTIME

        curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        tame = curr.strftime('%I:%M:%S %p')
        logging.info(LOG_MSG.format(me.first_name, date, tame, __repo__, __version__, __license__, __copyright__))

        try:
            await self.send_message(
                LOG_CHANNEL,
                text=LOG_MSG.format(me.first_name, date, tame, __repo__, __version__, __license__, __copyright__),
                disable_web_page_preview=True
            )
        except Exception as e:
            logging.warning(f"Bot isn't able to send message to LOG_CHANNEL \n{e}")

        if bool(WEB_SUPPORT):
            app = web.Application(client_max_size=30000000)

            async def health_check(request):
                return web.Response(text="Bot is alive!", status=200)

            app.router.add_get("/", health_check)

            runner = web.AppRunner(app)
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", 8080).start()
            logging.info("Web response is running......🕸️")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1


bot = Bot()

def start_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help"),
         InlineKeyboardButton("About", callback_data="about")]
    ])

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    print("Start command received!")  # Debug print
    try:
        await message.reply_sticker("CAACAgUAAxkBAAEBVfFlnTD9i4c5DRM8K6MQN2aFFoyZuAACAwEAAvcCyFYybAIKq8ZECzQE")
        await message.reply_text(
            text=f"Hello <b>{message.from_user.first_name}</b>!\nI'm alive and ready to help.",
            reply_markup=start_markup(),
            parse_mode="html"
        )
    except Exception as e:
        print(f"Error in /start: {e}")

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        await callback_query.message.edit_text(
            "Here is how you can use me:\n\n"
            "/start - Show welcome message\n"
            "/help - Show this help message\n"
            "/about - About the bot",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])
        )
    elif data == "about":
        await callback_query.message.edit_text(
            "🤖 <b>Tessabot</b>\nA powerful autofilter Telegram bot.\n\nDeveloper: <a href='https://github.com/Appu13vava'>Appu13vava</a>\nVersion: 1.0\nLicense: GNU GPLv2",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])
        )
    elif data == "back":
        await callback_query.message.edit_text(
            text=f"Hello <b>{callback_query.from_user.first_name}</b>!\nI'm alive and ready to help.",
            reply_markup=start_markup(),
            parse_mode="html"
        )
    await callback_query.answer()


async def main():
    await bot.start()
    print("Bot is running...")
    await idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
