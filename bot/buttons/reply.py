from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import lang


def login_btn(language):

    frilanser_btn = KeyboardButton(text = lang[language]["firlanser"])
    buyurtmachi_btn = KeyboardButton(text = lang[language]["customer"])
    vakansiyalar_btn = KeyboardButton(text = lang[language]["vacancies"])
    til_btn = KeyboardButton(text = lang[language]["change_lang"])
    return ReplyKeyboardMarkup(keyboard=[[frilanser_btn, buyurtmachi_btn], [vakansiyalar_btn], [til_btn]], resize_keyboard=True)


def phone_btn():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="☎️ phone", request_contact=True)]], resize_keyboard=True)


