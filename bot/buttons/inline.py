from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from bot.buttons.text import lang
from db import ProgLang, session

def lang_ibtn():
    uz = InlineKeyboardButton(text = "🇺🇿 Uzbek", callback_data="uz")
    en = InlineKeyboardButton(text = "🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", callback_data="en")
    return InlineKeyboardMarkup(inline_keyboard=[[uz], [en]])


def prog_lang_ibtn():
    query = select(ProgLang)
    data = session.execute(query).fetchall()
    design = []
    row = []
    for i in data:
        row.append(InlineKeyboardButton(text = f"{i[0].name}", callback_data=f"{i[0].id}"))
        if len(row) == 2:
            design.append(row)
            row = []
    if row:
        design.append(row)
    return InlineKeyboardMarkup(inline_keyboard=design)


def customer_order(language):
    order = InlineKeyboardButton(text=lang[language]["order"], callback_data="order")
    order_history = InlineKeyboardButton(text=lang[language]["order_history"], callback_data="order_history")
    back = InlineKeyboardButton(text="🔙 Back", callback_data="back")
    return InlineKeyboardMarkup(inline_keyboard=[[order], [order_history], [back]])


def vacancy_receive(language):
    a = InlineKeyboardButton(text = lang[language]["receive"], callback_data="receive")
    return InlineKeyboardMarkup(inline_keyboard=[[a]])




