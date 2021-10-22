import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


