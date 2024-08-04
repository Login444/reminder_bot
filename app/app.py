import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types
from reminder import reminder_router

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(reminder_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
