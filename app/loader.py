import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from data.config import token, root_path, DATABASE_PATH, LOGGING_FILE_PATH
from utils.database import Database

logger = logging.getLogger('main')
logging.basicConfig(filename=root_path / LOGGING_FILE_PATH,
                    level=logging.INFO,
                    format='%(asctime)s | %(levelname)s - %(name)s: %(message)s')

default = DefaultBotProperties(parse_mode=ParseMode.HTML)

bot = Bot(token, default=default)
dp = Dispatcher()

connection = Database(DATABASE_PATH)
