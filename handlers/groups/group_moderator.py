import re
import asyncio
import datetime
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
from loader import dp
from filters import GroupFilter, AdminFilter


@dp.message_handler(GroupFilter(), Command('ro', prefixes='!/'), AdminFilter())
async def read_only(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    regex = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = regex.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5
    time = int(time)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
    try:
        await message.chat.restrict(member_id, can_send_messages=False, until_date=until_date)
        await message.reply_to_message.delete()
    except BadRequest as err:
        await message.answer(f"Xatolik  {err.args}")
        return
    test = await message.reply(f"foydalanuvchi {member.full_name} {time} minut davomnida yoza olmidi\nSabab: {comment}")
    service_msg = await message.answer(f"Xabar 5 secunda o'chiriladi")
    await asyncio.sleep(5)
    await message.delete()
    await service_msg.delete()
    await asyncio.sleep(5)
    await test.delete()


@dp.message_handler(GroupFilter(), Command('unro', prefixes='!/'), AdminFilter())
async def unro(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_other_messages=True,
        can_invite_users=True,
        can_send_media_messages=True,
        can_send_polls=False,
        can_pin_messages=False,
        can_change_info=False,
    )
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    active = await message.answer(f"Foydalanuvchi {member.get_mention()} faol xolatda!")
    # await message.delete()
    await asyncio.sleep(10)
    await active.delete()


@dp.message_handler(GroupFilter(), Command('ban', prefixes='!/'), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    await message.chat.kick(user_id=member_id)
    await message.reply(f"Foydalanuvchi {member.get_mention()} ban oldi.")
    await asyncio.sleep(10)
    await message.delete()


@dp.message_handler(GroupFilter(), Command('unban', prefixes='!/'), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    await message.chat.unban(user_id=member_id)
    unban = await message.reply(f"Foydalanuvchi {member.get_mention()} blockdan ozod qilindi.")
    await asyncio.sleep(20)
    await unban.delete()