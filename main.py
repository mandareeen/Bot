import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# ======== Настройки ========
BOT_TOKEN = os.getenv("BOT_TOKEN")  # бот токен из Render Secrets
WEBHOOK_PATH = "/webhook"            # путь вебхука
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 10000))  # Render сам передаст порт через переменную PORT
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# ======== Инициализация бота и диспетчера ========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======== Хэндлер сообщений ========
@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# ======== Настройка вебхука ========
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен на {WEBHOOK_URL}")

# ======== Создаем aiohttp приложение ========
app = web.Application()
app.add_routes([web.post(WEBHOOK_PATH, dp.start_webhook)])  # вебхук будет слушать POST запросы

# ======== Запуск ========
if __name__ == "__main__":
    asyncio.run(on_startup())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
