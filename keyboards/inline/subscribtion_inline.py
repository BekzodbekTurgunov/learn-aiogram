from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs")
        ]
    ]
)