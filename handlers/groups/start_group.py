from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import GroupFilter
from loader import dp


@dp.message_handler(GroupFilter(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Bot ishga tushirildi")
