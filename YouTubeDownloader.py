import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from opencc import OpenCC

# Initialize the Pyrogram client with the new syntax for Pyrogram v2
app = Client(
    "YouTubeDownloader",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be|xvideos\.com|pornhub\.com"
              r"|xhamster\.com|xnxx\.com))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")

s2tw = OpenCC('s2tw.json').convert

START_MSG = """ Hai {}, 
Am a YouTube Downloader Bot I can Download Audio and Video From YouTube. 
Just Send Me a YouTube video link and Download. 
"""
ABOUT_MSG = """
Soon........................
.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="SEARCH🔎", switch_inline_query_current_chat="")
        ],[
        InlineKeyboardButton('ABOUT📕', callback_data='about')
        ]]
    )
ABOUT_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('HOME🏡', callback_data='home'),
        InlineKeyboardButton('CLOSE🔐', callback_data='close')
        ]]
    )

# Define callback query handlers using the new syntax
@app.on_callback_query()
async def callback_query_handler(bot, update):
    try:
        if update.data == "home":
            await update.message.edit_text(
                text=START_MSG.format(update.from_user.mention),
                reply_markup=START_BTN,
                disable_web_page_preview=True
            )
        elif update.data == "about":
            await update.message.edit_text(
                text=ABOUT_MSG,
                reply_markup=ABOUT_BTN,
                disable_web_page_preview=True
            )
    except Exception as e:
        print(e)

# Define message handlers
@app.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    try:
        await update.reply_text(
            text=START_MSG.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BTN
        )
    except Exception as e:
        print(e)

@app.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    try:
        await update.reply_text(
            text=ABOUT_MSG,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BTN
        )
    except Exception as e:
        print(e)

@app.on_message(filters.private
                   & filters.text
                   & ~filters.edited
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(_, message: Message):
    try:
        await message.reply_text(
            "**Choose download type:**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Audio",
                            callback_data="ytdl_audio"
                        ),
                        InlineKeyboardButton(
                            "Video",
                            callback_data="ytdl_video"
                        )
                    ]
                ]
            ),
            quote=True
        )
    except Exception as e:
        print(e)

# Callback query handlers
@app.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        # Remaining code...
    except Exception as e:
        print(e)

@app.on_callback_query(filters.regex("^ytdl_video$"))
async def callback_query_ytdl_video(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        # Remaining code...
    except Exception as e:
        print(e)

# Helper functions...

# Start the bot
app.run()
