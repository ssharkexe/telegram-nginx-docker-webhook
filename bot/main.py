import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.executor import start_webhook

# global variable to switch between polling|webhook for debug/local start
IS_WEBHOOK = 1

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
NGINX_HOST = os.environ.get('NGINX_HOST') 

# webhook settings
WEBHOOK_HOST = f'https://{NGINX_HOST}'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0' 
WEBAPP_PORT = 3001

# bot initialization
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# webhook startup & shutdown
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print(f'Telegram servers now send updates to {WEBHOOK_URL}. Bot is online')

async def on_shutdown(dp):
    await bot.delete_webhook()

# echo handler function
async def start_command_handler(message: types.Message):
    await message.reply('Hey there! I am a simple echo-bot, ready to deploy you projects.')

# bot startup
if __name__ == '__main__':
    dp.register_message_handler(start_command_handler, content_types=['text'])
    if IS_WEBHOOK == 1:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,)
    else:
        executor.start_polling(dp, skip_updates=True)