
from aiogram.filters import CommandStart
from bot.buttons.inline import lang_ibtn
from bot.buttons.reply import login_btn
from bot.hendlers import *
from bot.buttons.language_sttengs import *
from state import UsersState
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:

    await message.answer(f"Assalomu aleykum.\nKwork botiga xush kelibsiz !\nWelcome to aur Kwork bot !")
    query = select(User).where(User.id == message.from_user.id)
    user = session.execute(query).fetchone()
    await state.set_state(UsersState.lan)
    if not user:
        await state.set_state(UsersState.lan)
        await message.answer("Tilni tanlang\nselect a language", reply_markup=lang_ibtn())
    else:
        await message.answer(f"{lang[user[0].lang]['menu']}", reply_markup=login_btn(user[0].lang))

@dp.callback_query(UsersState.lan)
async def user_lang_hendler(call: CallbackQuery, state:FSMContext):
    await call.message.delete()
    query = insert(User).values(id = call.from_user.id, lang = call.data)
    session.execute(query)
    session.commit()
    await call.message.answer(f"{lang[call.data]['menu']}", reply_markup=login_btn(call.data))

@dp.message(lambda msg: msg.text in [lang['uz']['change_lang'], lang['en']['change_lang']])
async def change_lang_hendler(msg: Message, state: FSMContext):
    await msg.delete()
    query = select(User).where(User.id == msg.from_user.id)
    user = session.execute(query).fetchone()
    await state.set_state(UsersState.change_lang)
    await msg.answer(f"{lang[user[0].lang]['change_lang']}", reply_markup=lang_ibtn())













