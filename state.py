from aiogram.fsm.state import State, StatesGroup


class UsersState(StatesGroup):
    lan = State()
    phone = State()
    change_lang = State()
    firlanser = State()

class FirlanserState(StatesGroup):
    full_name = State()
    phone = State()
    prog_lang = State()
    product_id = State()

class CustomerState(StatesGroup):
    fullname = State()
    phone = State()
    product_title = State()
    product_price = State()
    product_description = State()


