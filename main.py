from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("✅ Бот работает! Привет!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
