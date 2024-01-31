from aiogram.types import  CallbackQuery
from sqlalchemy import update
from bot.buttons.reply import login_btn
from db import User, session
from dispetcher import dp
from state import UsersState


@dp.callback_query(UsersState.change_lang)
async def change_hendler(call: CallbackQuery):
    query = update(User).values(lang = call.data).where(User.id == call.from_user.id)
    session.execute(query)
    session.commit()
    await call.message.delete()
    await call.message.answer("✅", reply_markup=login_btn(call.data))


