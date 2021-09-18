from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Post joylash'),
            KeyboardButton('Yordam')
        ]
    ],
    resize_keyboard=True
)