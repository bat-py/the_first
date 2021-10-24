import logging
import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
import json
from button_creators import *
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sql_handler
from menus import products


#API_TOKEN = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
API_TOKEN = '1559565040:AAG97C16gpMUk4cZgElzGspPb8uplSCX0Ss'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


async def city_menu(message, from_where):
    """
    :param message:
    :param from_where: Тут ты должен передать 1 или 2.
        1 - генерируем список городов c callback_data "city_welcome+city_id
        2 - генерируем список городов с callback_data "city_location+city_id"

        #В данном случае мы меням replay кнопку "Товары" на "Товары ({Выбранный город})"
        #После этого отправим сообщение "Выбор сохранен" а потом сообщение "Выберите товар:" с инлайн кнопками
        #2 это - если пользователь который выбрал город из сообщении который вернул reply кнопка "Локации".
        #В данном случае мы отправим только сообщение "Выберите товар:" с инлайн кнопками
    :return:
    """
    which = ['city_welcome', 'city_location']

    # Gets list with dicts like:  [ {'id': 10, 'city': 'Уфа'}, {'id': 20, 'city': 'Челябинск'}, ... ]
    cities_list = sql_handler.get_cities_list()
    cities = [[i['city'], which[from_where-1]+str(i['id'])] for i in cities_list]
    ready_buttons = inline_keyboard_creator(cities)
    mesg = 'Выберите город:'
    await message.answer(text=mesg, reply_markup=ready_buttons)


async def balance_menu(message, from_where):
    """
    :param message:
    :param from_where: Тут ты должен передать 1 или 2.
        1 это - если пользователь нажал на inline кнопку "Баланс" который находится в сообщении /start
        2 это - если пользователь нажал на reply button кноку "Баланс" который находится в главном меню
    :return:
    """
    pass


# /READY
# Command "/start" handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not sql_handler.check_user_exists(message.chat.id):
        sql_handler.add_user(message.chat.id, message.chat.first_name)
        print()

    # Sends logo image
    await message.answer_photo(photo=open('images/logo.jpg', 'rb'))

    # Sends Welcome Message with two inline
    balance = sql_handler.get_balance(message.chat.id)
    balance_mesg = f'Баланс ({balance})'
    bot_support = 'https://t.me/iso_support_bot'
    gen_inline_keyboard_buttons = inline_keyboard_creator([ [balance_mesg, 'balance'],
                                                            [bot_mesg['bot_support'], bot_support]
                                                          ])
    await message.answer(bot_mesg['welcome'], parse_mode='html', reply_markup=gen_inline_keyboard_buttons)

    # Good luck and main menu reply keyboards
    buttons = main_menu_buttons(message.chat.id)
    await message.answer('Удачных покупок!', reply_markup=buttons)

    # Если до этого получил 50р по реф. коду, тогда этого сообщения не будет
    if not balance:
        # Do you wan't referral code?  inlinekeyboard: show referral code
        referral_code = inline_keyboard_creator([ ['Ввести реферальный код', 'referral_code'] ])
        await message.answer('Хотите ввести код реферала? После ввода кода реферала на ваш баланс будет начислено 50 руб',
                             reply_markup=referral_code)

    # Sends message("Выберите город:") to member with InlineKeyboards
    await city_menu(message, 1)
    

# /READY
@dp.message_handler(lambda mesg: mesg.text == 'Локации')
async def cities_menu(message: types.Message):
    # Sends message("Выберите город:") to member with InlineKeyboards
    await city_menu(message, 2)


@dp.message_handler(lambda mesg: mesg.text.startswith('Товары'))
async def products_menu(message: types.Message):
    pass


@dp.message_handler(lambda mesg: mesg.text == 'Профиль')
async def profile_menu(message: types.Message):
    pass


@dp.message_handler(lambda mesg: mesg.text == 'Баланс')
async def balance_menu(message: types.Message):
    pass


@dp.message_handler(lambda mesg: mesg.text.startswith('Отзывы'))
async def products_menu(message: types.Message):
    pass


@dp.message_handler(lambda mesg: mesg.text == 'Поддержка')
async def balance_menu(message: types.Message):
    pass


@dp.message_handler(lambda mesg: mesg.text == 'Заработать')
async def balance_menu(message: types.Message):
    pass


if __name__ == "__main__":
    # Регистрируем обработчики(handlers) модуля menus/products.py
    products.register_handlers_products(dp)

    executor.start_polling(dp, skip_updates=True)


