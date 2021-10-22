import logging

import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
import json

API_TOKEN = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# Creates InlineKeyboardMarkup
def inline_keyboard_creator(*args, row_width=2):
    """
    :param row_width: Columns count
    :param args: You should give lists. Every list is one button. List's structure: [button_text, callback_data]
    :return: Ready InlineKeyboardMarkup
    """

    buttons = []
    print(args)
    for i in args:
        print(i)
        if i[1].startswith('tg://'):
            button = aiogram.types.InlineKeyboardButton(i[0], url=i[1])
        else:
            button = aiogram.types.InlineKeyboardButton(i[0], callback_data=i[1])

        buttons.append(button)

    ready_buttons = aiogram.types.InlineKeyboardMarkup(row_width=row_width, inline_keyboard=buttons)

    return ready_buttons


# Command "/start" handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Sends logo image
    await message.answer_photo(photo=open('images/logo.jpg', 'rb'))

    # Sends Welcome Message with two inline
    balance = '0'
    bot_support = 'tg://iso_support_bot'
    buttons = inline_keyboard_creator([balance, 'welcome'],
                                      [bot_mesg['bot_support'], bot_support])
    gen_inline_keyboard_buttons = inline_keyboard_creator(buttons)

    await message.answer(bot_mesg['welcome'], parse_mode='html', reply_markup=gen_inline_keyboard_buttons)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)