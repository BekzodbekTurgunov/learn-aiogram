from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

post_call_back = CallbackData('create_post', 'action')

post_ky = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆗 Chop etish", callback_data=post_call_back.new(action='post')),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=post_call_back.new(action='cancel'))
        ]
    ]
)
