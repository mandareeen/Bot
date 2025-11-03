import asyncio
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хэндлер для команды /start
@dp.message()
async def start(message: types.Message):
    await message.reply("✅ Бот работает! Привет!")

async def main():
    try:
        # Запуск бота
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
