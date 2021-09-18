from aiogram import types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.confirmation_state import ConfirmationPost
from keyboards.inline.post_keyboard import post_ky, post_call_back
from utils.notify_admins import on_startup_notify


@dp.message_handler(commands='create_post')
@dp.message_handler(Text('Post joylash'))
async def create_post_handler(message: types.Message):
    await message.answer("please write definition your product which you want to sold", reply_markup=ReplyKeyboardRemove())
    await ConfirmationPost.newMessage.set()


@dp.message_handler(state=ConfirmationPost.newMessage, content_types=types.ContentTypes.ANY)
async def confirmation_post(message: types.Message, state: FSMContext):
    await state.update_data(post=message.text, mention=message.from_user.get_mention())
    await message.reply("do you want to send post?", reply_markup=post_ky)
    await ConfirmationPost.next()


@dp.callback_query_handler(post_call_back.filter(action='post'), state=ConfirmationPost.confirm)
async def send_to_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("You have send successfully your product.")
    async with state.proxy() as data:
        text = data.get('post')
        mention = data.get('mention')
    await state.finish()
    await call.message.delete()
    await on_startup_notify(dp, f"Foydalanuvchi {mention}, quyidagi textni chop etmoqchi:")
    await bot.send_message(ADMINS[0], text, parse_mode='HTML', reply_markup=post_ky)
    await call.answer(cache_time=60, show_alert=True)


@dp.callback_query_handler(post_call_back.filter(action='cancel'), state=ConfirmationPost.confirm)
async def send_to_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("You have canceled your post.")
    await state.finish()
    await call.message.delete()
    await call.answer(cache_time=60, show_alert=True)


@dp.callback_query_handler(post_call_back.filter(action='post'), user_id=ADMINS)
async def post_channel(call: CallbackQuery):
    await call.answer("chop etishga ruhsat berdingiz", show_alert=True)
    message = await call.message.edit_reply_markup()
    # it is working when channel id giver correctly
    # channel = 'channelID'
    # await message.send_copy(chat_id=channel)


@dp.callback_query_handler(post_call_back.filter(action='cancel'), user_id=ADMINS)
async def post_channel(call: CallbackQuery):
    await call.answer("chop etishga ruhsat bermadingiz", show_alert=True)
    await call.message.edit_reply_markup()