import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update, Message

# ===== Настройки =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан!")

WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# ===== Инициализация бота и диспетчера =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== Хэндлер сообщений =====
@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# ===== Функция для aiohttp сервера =====
async def handle_webhook(request):
    update = Update(**await request.json())
    await dp.feed_update(update)
    return web.Response(text="ok")

# ===== Настройка aiohttp =====
app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен на {WEBHOOK_URL}")

# ===== Запуск =====
if __name__ == "__main__":
    asyncio.run(on_startup())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
