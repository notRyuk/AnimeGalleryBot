import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID', None)
api_hash = os.environ.get('API_HASH', None)
bot_token = os.environ.get('BOT_TOKEN', None)

tg_client = TelegramClient('anime_gallery_bot', api_id, api_hash).start(bot_token=bot_token)
