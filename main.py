import logging
import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sql_handler

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
def inline_keyboard_creator(buttons_list, row_width=2):
    """
    :param row_width: Columns count
    :param buttons_list: You should give lists. Every list is one button. List's structure: [button_text, callback_data]
    :return: Ready InlineKeyboardMarkup
    """

    ready_buttons = InlineKeyboardMarkup(row_width=row_width)

    for i in buttons_list:
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


def main_menu_buttons(message):
    feedback_count = 444
    buttons = [
        ['Локации', 'Товары ', 'Профиль'],
        ['Баланс', f'Отзывы ({feedback_count})', 'Поддержка'],
        ['Заработать']
    ]
    ready_buttons = reply_keyboard_creator(buttons)

    return ready_buttons


async def cities_menu(message):
    # Gets list with dicts like:  [ {'id': 10, 'city': 'Уфа'}, {'id': 20, 'city': 'Челябинск'}, ... ]
    cities_list = sql_handler.get_cities_list()
    cities = [[i['city'], 'main_menu_city'+str(i['id'])] for i in cities_list]
    ready_buttons = inline_keyboard_creator(cities)
    mesg = 'Выберите город:'
    # bot.send_message(chat_id=message.chat.id, text=mesg, reply_markup=ready_buttons)
    await message.answer(chat_id=message.chat.id, text=mesg, reply_markup=ready_buttons)
    print('hello')

# Command "/start" handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Sends logo image
    await message.answer_photo(photo=open('images/logo.jpg', 'rb'))

    # Sends Welcome Message with two inline
    balance = 0
    balance_mesg = f'Баланс ({balance})'
    bot_support = 'https://t.me/iso_support_bot'
    gen_inline_keyboard_buttons = inline_keyboard_creator([ [balance_mesg, 'balance'],
                                                            [bot_mesg['bot_support'], bot_support]
                                                          ])
    await message.answer(bot_mesg['welcome'], parse_mode='html', reply_markup=gen_inline_keyboard_buttons)

    # Good luck and main menu reply keyboards
    buttons = main_menu_buttons(message)
    await message.answer('Удачных покупок!', reply_markup=buttons)

    # Do you wan't referral code?  inlinekeyboard: show referral code
    referral_code = inline_keyboard_creator([ ['Ввести реферальный код', 'referral_code'] ])
    await message.answer('Хотите ввести код реферала? После ввода кода реферала на ваш баланс будет начислено 50 руб',
                         reply_markup=referral_code)

    # Sends message("Выберите город:") to member with InlineKeyboards
    cities_menu(message)



@dp.message_handler(lambda mesg: mesg.text == 'Локации')
async def cities_menu(message: types.Message):
    pass







# City menu InlineKeyboardCreate handler
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('city'))
async def callback_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'hello')
    #await callback_query.answer('hello')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)