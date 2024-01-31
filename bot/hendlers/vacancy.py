from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from bot.buttons.inline import vacancy_receive
from bot.buttons.reply import login_btn
from bot.buttons.text import lang
from db import Product, session, User, Firlanser
from dispetcher import dp
from state import FirlanserState


@dp.message(lambda msg: msg.text in ["💼 Vakasiyalar/Vakansiya joylashtirish", "💼 Apply Vacancy/Vacancies"])
async def vacancy_hendler(msg: Message, state: FSMContext):
    query = select(Firlanser).where(Firlanser.user_id == msg.from_user.id)
    user = session.execute(query).fetchone()
    if user:
        query = select(Product)
        products = session.execute(query).fetchall()
        query = select(User).where(User.id == msg.from_user.id)
        user = session.execute(query).fetchone()
        if products:
            for product in products:
                if product[0].status == "sent":
                    vacancy_text = (f"{lang[user[0].lang]['product_id_text']} {product[0].id}.\n\n"
                                    f"{lang[user[0].lang]['product_title_text']} {product[0].title}.\n\n"
                                    f"{lang[user[0].lang]['product_description_text']} {product[0].description}.\n\n\n\n"
                                    f"{lang[user[0].lang]['product_price_text']} {product[0].price}.\n"
                                    f"{lang[user[0].lang]['product_status_text']} {product[0].status}")
                    await msg.answer(text = vacancy_text, reply_markup = vacancy_receive(user[0].lang))
        else:
            await msg.answer(text=lang[user[0].lang]['check_product'])

    else:
        await msg.answer(text = lang[user[0].lang]['vacancy_firlanser'], reply_markup=login_btn(user[0].lang))


@dp.callback_query(lambda call: call.data == "receive")
async def receive_hendler(call: CallbackQuery, state: FSMContext):
    query = select(User).where(User.id == call.from_user.id)
    user = session.execute(query).fetchone()
    await state.set_state(FirlanserState.product_id)
    await call.message.answer(text=lang[user[0].lang]['place_product_id'])

@dp.message(FirlanserState.product_id)
async def firlanser_receive_hendler(msg: Message, state: FSMContext):
    query = select(User).where(User.id == msg.from_user.id)
    user = session.execute(query).fetchone()

    send_message = (f"{lang[user[0].lang]['product_status_text2']}\n"
                    f"freelanser :  {user[0].full_name}.\n"
                    f"📞 : {user[0].phone}\n"
                    f"telegram id : {msg.from_user.id}")

    query = update(Product).values(status = send_message).where(Product.id == int(msg.text))
    session.execute(query)
    session.commit()
    await msg.answer("👨🏻‍💻", reply_markup=login_btn(user[0].lang))






