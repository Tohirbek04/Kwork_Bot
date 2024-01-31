from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert, update

from bot.buttons.inline import customer_order
from bot.buttons.reply import phone_btn, login_btn
from bot.buttons.text import lang
from db import User, session, Customer, Product, Firlanser
from dispetcher import dp
from state import CustomerState


@dp.message(lambda msg: msg.text in ["👤 Men buyurtmachiman","👤 I am customer"])
async def customer_hendler(msg: Message, state: FSMContext):
    query = select(User).where(User.id == msg.from_user.id)
    user = session.execute(query).fetchone()
    query = select(Customer).where(Customer.user_id == msg.from_user.id)
    customer = session.execute(query).fetchone()
    if not customer:
        data = await state.get_data()
        data["user_lang"] = user[0].lang
        await state.set_data(data)
        await msg.answer(text = lang[data.get("user_lang")]['fullname'])
        await state.set_state(CustomerState.fullname)
    else:
        data = await state.get_data()
        data["user_lang"] = user[0].lang
        await state.set_data(data)
        await msg.answer(text=lang[data.get('user_lang')]['customer_bot'],reply_markup=customer_order(data.get('user_lang')))


@dp.message(CustomerState.fullname)
async def customer_fullname_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    data["fullname"] = msg.text
    await state.set_data(data)
    await state.set_state(CustomerState.phone)
    await msg.answer(text = lang[data.get('user_lang')]['phone_number'], reply_markup=phone_btn())

@dp.message(CustomerState.phone)
async def customer_phone_number_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    phone_number = msg.contact.phone_number
    query = update(User).values(phone = phone_number, full_name = data.get("fullname")).where(User.id == msg.from_user.id)
    session.execute(query)
    session.commit()
    query = insert(Customer).values(user_id = msg.from_user.id)
    session.execute(query)
    session.commit()
    await msg.answer(text=lang[data.get('user_lang')]['customer_bot'], reply_markup=customer_order(data.get('user_lang')))
    await state.clear()

@dp.callback_query(lambda call: call.data == "order")
async def order_hendler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    query = select(User).where(User.id == call.from_user.id)
    user = session.execute(query).fetchone()
    data = await state.get_data()
    data['user_lang'] = user[0].lang
    await state.set_data(data)
    await state.set_state(CustomerState.product_title)
    await call.message.answer(text = lang[data.get("user_lang")]['product_title'])

@dp.message(CustomerState.product_title)
async def product_description_handler(msg: Message, state:FSMContext):
    data = await state.get_data()
    data['product_title'] = msg.text
    await state.set_data(data)
    await state.set_state(CustomerState.product_description)
    await msg.answer(text=lang[data.get("user_lang")]['product_description'])

@dp.message(CustomerState.product_description)
async def product_description_handler(msg: Message, state:FSMContext):
    data = await state.get_data()
    data['product_description'] = msg.text
    await state.set_data(data)
    await state.set_state(CustomerState.product_price)
    await msg.answer(text=lang[data.get("user_lang")]['product_price'])


@dp.message(CustomerState.product_price)
async def product_price_handler(msg: Message, state:FSMContext):
    data = await state.get_data()

    query = select(Customer).where(Customer.user_id == msg.from_user.id)
    customer = session.execute(query).fetchone()
    query = insert(Product).values(title = data.get('product_title'), description = data.get('product_description'), price = msg.text, customer_id = customer[0].id)
    session.execute(query)
    session.commit()
    await msg.answer(text=lang[data.get('user_lang')]['save_product'], reply_markup=login_btn(data.get('user_lang')))
    await state.clear()


@dp.callback_query(lambda call: call.data == "back")
async def customer_back_callback(call:CallbackQuery):
    await call.message.delete()
    query = select(User).where(User.id == call.from_user.id)
    user = session.execute(query).fetchone()
    await call.message.answer("back", reply_markup=login_btn(user[0].lang))

@dp.callback_query(lambda call: call.data == "order_history")
async def order_history_callback(call:CallbackQuery):
    query = select(Customer).where(Customer.user_id == call.from_user.id)
    customer = session.execute(query).fetchone()
    products = customer[0].products
    query = select(User).where(User.id == call.from_user.id)
    user = session.execute(query).fetchone()
    if products:
        for product in products:
            vacancy_text = (f"{lang[user[0].lang]['product_id_text']} {product.id}.\n\n"
                            f"{lang[user[0].lang]['product_title_text']} {product.title}.\n\n"
                            f"{lang[user[0].lang]['product_description_text']} {product.description}.\n\n"
                            f"{lang[user[0].lang]['product_price_text']} {product.price}.\n"
                            f"{lang[user[0].lang]['product_status_text']} {product.status}")
            await call.message.answer(text=vacancy_text)
    else:
        await call.message.delete()
        await call.message.answer(text=lang[user[0].lang]['customer_product'])














