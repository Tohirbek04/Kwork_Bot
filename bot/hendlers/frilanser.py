from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert, update

from bot.buttons.inline import prog_lang_ibtn
from bot.buttons.reply import login_btn, phone_btn
from bot.buttons.text import lang
from db import User, session, Firlanser, ProgLang, Customer
from dispetcher import dp
from state import FirlanserState

@dp.message(lambda msg: msg.text in ["🧑🏻‍💻 Men Firlanserman", "🧑🏻‍💻 I am Freelancer"])
async def firlanser_hendler(msg:Message, state:FSMContext):
    query = select(Firlanser).where(Firlanser.user_id == msg.from_user.id)
    firlanser = session.execute(query).fetchone()

    if not firlanser:
        query = select(User).where(User.id == msg.from_user.id)
        user = session.execute(query).fetchone()
        data = await state.get_data()
        data["user_lang"] = user[0].lang
        await state.set_data(data)
        await state.set_state(FirlanserState.full_name)
        await msg.answer(lang[data.get('user_lang')]["fullname"])
    else:
        query = select(User).where(User.id == msg.from_user.id)
        user = session.execute(query).fetchone()
        data = await state.get_data()
        data["user_lang"] = user[0].lang
        await msg.answer(text=lang[data.get('user_lang')]["firlanser_bot"], reply_markup=login_btn(data.get('user_lang')))


@dp.message(FirlanserState.full_name)
async def firlanser_fullname_hendler(msg: Message, state: FSMContext):
    data = await state.get_data()
    data["fullname"] = msg.text
    await state.set_data(data)
    await state.set_state(FirlanserState.prog_lang)
    await msg.answer(f"{lang[data.get('user_lang')]['prog_lang']}", reply_markup=prog_lang_ibtn())

@dp.callback_query(FirlanserState.prog_lang)
async def firlanser_prog_lang_hendler(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    query = select(ProgLang).where(ProgLang.id == str(call.data))
    proglang = session.execute(query).fetchone()
    data = await state.get_data()
    data["prog_lang"] = proglang[0].id
    await state.set_data(data)
    await state.set_state(FirlanserState.phone)
    await call.message.answer(text = lang[data.get('user_lang')]['phone_number'], reply_markup=phone_btn())


@dp.message(FirlanserState.phone)
async def firlanser_phone_hendler(msg: Message, state: FSMContext):
    data = await state.get_data()
    phone_number = msg.contact.phone_number
    query = update(User).values(phone = phone_number, full_name = data.get("fullname")).where(User.id == msg.from_user.id)
    session.execute(query)
    session.commit()
    query = insert(Firlanser).values(user_id = msg.from_user.id, prog_lang_id = data.get('prog_lang'))
    session.execute(query)
    session.commit()
    await msg.answer(text = lang[data.get('user_lang')]['firlanser_bot'], reply_markup=login_btn(data.get('user_lang'))) #TODO bu yerdayam login_btn ishlamayapti
    await state.clear()






