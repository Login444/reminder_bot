from aiogram.filters import Filter
from aiogram import types


# Создаем свой класс фильтра типа чатов
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        """
        передаем список типов чата в котором будет работать тот или иной роутер
        :param chat_types:
        """
        self.chat_types = chat_types

    # переопределяем метод __call__:
    async def __call__(self, message: types.Message) -> bool:
        """
        передаем сообщение, далее из сообщения вытягиваем тип чата в котором оно отправлено
        если тип чата указа в переменной объекта, то будет возвращено True
        :param message:
        :return: True
        """
        return message.chat.type in self.chat_types
