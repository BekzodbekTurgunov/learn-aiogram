from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.misc.subscription import check
from keyboards.inline.subscribtion_inline import check_sub
from data.config import CHANNEL
from filters import PrivateFilter
from loader import dp, bot


@dp.message_handler(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message):
    channel_format = str()
    for channel in CHANNEL:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channel_format += f"<a href='{invite_link}'> {chat.title}</a>\n"
    await message.answer(
        f"Assalomu alaykum {message.from_user.full_name},\nKanaldan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        f"{channel_format}", reply_markup=check_sub,
        disable_web_page_preview=True)


@dp.callback_query_handler(text='check_subs')
async def check_subscription(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNEL:
        status = await check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title}</b> ga obunasiz\n\n"
        else:
            link = await channel.export_invite_link()
            result += f"<b>{channel.title}</b>ga obuna emassiz, <a href='{link}'>Obuna bo'ling</a>"
    await call.message.answer(result,disable_web_page_preview=True)
    await call.message.delete()
