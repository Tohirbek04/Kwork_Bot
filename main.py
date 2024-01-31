import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.enums import ParseMode

from db import Base, engine
from dispetcher import TOKEN, dp
from bot.start import *
async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



