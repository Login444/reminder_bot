from typing import re
import asyncio

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from datetime import datetime, timedelta
from aiogram.types import MessageEntity
from chat_filter import ChatTypeFilter

reminder_router = Router()
reminder_router.message.filter(ChatTypeFilter(['group']))


messages_from_user = {}


def converter_duration(deadline: str) -> timedelta:
    interval = int(deadline[:-1])
    duration = deadline[-1]

    match duration.lower():
        case 'h':
            return timedelta(hours=interval)
        case 'd':
            return timedelta(days=interval)
        case 'w':
            return timedelta(weeks=interval)
        case 'm':
            return timedelta(days=interval * 30)
        case _:
            raise ValueError("Неверный формат длительности")


@reminder_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Бот запущен и готов к работе.")


@reminder_router.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer("Напишите задачу и отправьте её боту.\n"
                         "В следующем сообщении напишите боту в формате:\n"
                         "'@reminder_bir_chatbot ctrl 5d'\n"
                         "Где 5 - интервал, d - продолжительность (дни)\n"
                         "h - часы\n d - дни\n w - недели\n m - месяцы")


@reminder_router.message(F.text.startswith('@reminder_bir_chatbot ctrl'))
async def set_reminder(message: types.Message):
    try:
        duration = converter_duration(message.text.split()[-1])
    except ValueError:
        await message.answer("Неверный формат длительности")
        return

    remind_time = datetime.now() + duration
    last_message = messages_from_user[message.from_user.id]
    await message.reply(text=f'Задача #{last_message}# принята\n'
                             f'Напомню о ней в {remind_time.strftime("%H:%M %d/%m/%Y")}')

    await asyncio.sleep(duration.total_seconds())
    await message.reply(text=f'Задача #{message_from_user}')


@reminder_router.message()
async def save_msg(message: types.Message):
    user_id = message.from_user.id
    messages_from_user[user_id] = message.text
