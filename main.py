from aiogram import Bot, Dispatcher, executor, types
import os

TOKEN = os.getenv("BOT_TOKEN")  # ⚡ توکن فقط در Render ذخیره میشه، نه اینجا

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("سلام 👋\nربات RiseMind فعال شد 🤖")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.reply("دستورات:\n/start\n/help")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
