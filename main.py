import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Получаем токен из переменных среды
API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN не задан!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Пример хэндлера /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот работает!")

# --- aiohttp сервер для Render ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def on_startup(app):
    # можно запускать background polling
    from aiogram import F
    import asyncio

    async def polling():
        await dp.start_polling(bot)

    app["polling_task"] = asyncio.create_task(polling())

async def on_cleanup(app):
    app["polling_task"].cancel()
    await bot.session.close()

app = web.Application()
app.router.add_get("/", handle)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

# Render назначает порт через переменную среды PORT
port = int(os.getenv("PORT", 8000))
web.run_app(app, port=port)
