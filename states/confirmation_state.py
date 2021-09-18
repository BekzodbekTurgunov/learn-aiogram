from aiogram.dispatcher.filters.state import State, StatesGroup


class ConfirmationPost(StatesGroup):
    newMessage = State()
    confirm = State()
