from aiogram import types
from loader import dp, bot
from filters import AdminFilter, GroupFilter
from aiogram.dispatcher.filters import Command
import io


@dp.message_handler(GroupFilter(), Command('set_photo', prefixes='!/', ), AdminFilter())
async def set_new_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(photo)
    #1-usul
    # await bot.set_chat_photo(message.chat.id, photo=input_file)
    await message.chat.set_photo(photo=input_file)


@dp.message_handler(GroupFilter(), Command('set_title', prefixes='!/', ), AdminFilter())
async def set_title(message: types.Message):
    title = message.reply_to_message
    if title:
        title = title.text
        await bot.set_chat_title(message.chat.id, title=title)
    else:
        await message.reply("Please reply to text for set title")


@dp.message_handler(GroupFilter(), Command('set_description', prefixes='!/', ), AdminFilter())
async def set_description(message: types.Message):
    description = message.reply_to_message
    if description:
        description = description.text
        # await bot.set_chat_description(message.chat.id, description=description)
        await message.chat.set_description(description=description)
    else:
        await message.reply("please reply to message for set description")
