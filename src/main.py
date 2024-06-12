import asyncio
import sys
import logging

from dispatcher import *
from keyboards.responses import *
from db import db

session = db.create_database()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())