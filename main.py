import logging
import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

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

    ready_buttons = InlineKeyboardMarkup(row_width=row_width)

    for i in args:
        if i[1].startswith('https://'):
            button = InlineKeyboardButton(i[0], url=i[1])
            ready_buttons.add(button)
        else:
            button = InlineKeyboardButton(i[0], callback_data=i[1])
            ready_buttons.add(button)

    return ready_buttons


# Creates ReplyKeyboardCreator
def reply_keyboard_creator(buttons_list):
    """
    :param args: Передаешь массивы, каждый массив это одна строка, в внутри массива будет еще массавы которые каждый
    :return:
    """

    ready_buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in buttons_list:
        row = [KeyboardButton(j) for j in i]
        ready_buttons.row(*row)

    return ready_buttons



# Command "/start" handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Sends logo image
    await message.answer_photo(photo=open('images/logo.jpg', 'rb'))

    # Sends Welcome Message with two inline
    balance = 0
    balance_mesg = f'Баланс ({balance})'
    bot_support = 'https://t.me/iso_support_bot'
    gen_inline_keyboard_buttons = inline_keyboard_creator([balance_mesg, 'welcome'],
                                                          [bot_mesg['bot_support'], bot_support])
    await message.answer(bot_mesg['welcome'], parse_mode='html', reply_markup=gen_inline_keyboard_buttons)

    # Good luck and main menu reply keyboards
    feedback_count = 444
    buttons = [
        ['Локации', 'Товары (Уфа)', 'Профиль'],
        ['Баланс', f'Отзывы ({feedback_count})', 'Поддержка'],
        ['Заработать']
    ]
    ready_buttons = reply_keyboard_creator(buttons)
    await message.answer('Удачных покупок!', reply_markup=ready_buttons)

    # Do you wan't referral code?  inlinekeyboard: show referral code
    referral_code = inline_keyboard_creator(['Ввести реферальный код', 'referral_code'])
    await message.answer('Хотите ввести код реферала? После ввода кода реферала на ваш баланс будет начислено 50 руб',
                         reply_markup=referral_code)

    choose_cities()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)