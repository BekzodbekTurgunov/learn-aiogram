from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNEL
from utils.misc.subscription import check
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.message.from_user.id
        else:
            return
        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        for channel in CHANNEL:
            status = await check(user_id=user, channel=channel)
            final_status *= status
            if not status:
                channel = await bot.get_chat(channel)
                link = await channel.export_invite_link()
                result += f"{channel.title} <a href='{link}'> obuna bo'lish</a>\n"
        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()
