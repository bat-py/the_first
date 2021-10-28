import logging
import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from button_creators import *
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sql_handler
import cancel_order_system_handlers
from menus import products
from menus import balance
from menus import earn
from menus import profile
import admin_panel
from menus import feedbacks
from aiogram.dispatcher.filters.state import State, StatesGroup


API_TOKEN = sql_handler.get_bot_api()
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# /READY
async def city_menu(message, from_where):
    """
    Генерирует сообщение "Выберите город:" с inline кнопками городов
    :param message:
    :param from_where: Тут ты должен передать 1 или 2.
        1 - генерируем список городов c callback_data "city_welcome+city_id
        2 - генерируем список городов с callback_data "city_location+city_id"
    :return:
    """
    which = ['city_welcome', 'city_location']

    # Gets list with dicts like:  [ {'id': 10, 'city': 'Уфа'}, {'id': 20, 'city': 'Челябинск'}, ... ]
    cities_list = sql_handler.get_cities_list()
    cities = [[i['city'], which[from_where-1]+str(i['id'])] for i in cities_list]
    ready_buttons = inline_keyboard_creator(cities)
    mesg = 'Выберите город:'
    await message.bot.send_message(
        message.from_user.id,
        text=mesg, reply_markup=ready_buttons)


# /READY
async def send_welcome(message):
    """
    :param message:
    :return: Welcome message and main menu reply buttons
    """
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    # Sends logo image
    await message.bot.send_photo(
        message.from_user.id,
        photo=open('images/logo.jpg', 'rb'))

    # Sends Welcome Message with two inline
    balance = sql_handler.get_balance(message.from_user.id)
    balance_mesg = f'Баланс ({balance})'
    bot_support = 'https://t.me/iso_support_bot'
    gen_inline_keyboard_buttons = inline_keyboard_creator([ [balance_mesg, 'balance'],
                                                            [bot_mesg['bot_support'], bot_support]
                                                          ])
    await message.bot.send_message(
        message.from_user.id,
        bot_mesg['welcome'], parse_mode='html', reply_markup=gen_inline_keyboard_buttons)

    # Good luck and main menu reply keyboards
    buttons = main_menu_buttons(message.from_user.id)
    await message.bot.send_message(
        message.from_user.id,
        'Удачных покупок!', reply_markup=buttons)

    # Если до этого получил 50р по реф. коду, тогда этого сообщения не будет
    if not balance:
        # Do you wan't referral code?  inlinekeyboard: show referral code
        referral_code = inline_keyboard_creator([ ['Ввести реферальный код', 'referral_code'] ])
        await message.bot.send_message(
            message.from_user.id,
            'Хотите ввести код реферала? После ввода кода реферала на ваш баланс будет начислено 50 руб',
            reply_markup=referral_code)

    # Sends message("Выберите город:") to member with InlineKeyboards
    await city_menu(message, 1)


# /READY
# Command "/start" handler
@dp.message_handler(commands=['start'], state='*')
async def start_command_handler(message: types.Message, state: FSMContext):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    await state.finish()
    await send_welcome(message)


# /READY
@dp.message_handler(lambda mesg: mesg.text == 'Локации')
async def cities_menu(message: types.Message):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    # Sends message("Выберите город:") to member with InlineKeyboards
    await city_menu(message, from_where=2)


@dp.message_handler(lambda mesg: mesg.text.startswith('Товары'))
async def products_menu(message: types.Message):
    """
    Запустится когда пользователь нажал на reply кнопку Товары из главного меню
    :param message:
    :return:
    """
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    # Проверим пользователь до этого сохранил ли кокой-нибудь город. Ну короче если кнопка выглядит так "Товары (Уфа)"
    user_city = sql_handler.get_user_city(message.chat.id)

    # Запустим функцию который отправит сообщение "Выберите товар:" если было нажата на кнопку как "Товары (Воронеж)"
    if user_city:
        await products.waiting_for_product_type(message, user_city['city_id'])
    # Если у польз. нету сохраненного города(тоесть нажал на кнопку "Товары") тогда отправим сообщение "Выберите город:"
    else:
        await city_menu(message, from_where=2)


# /READY
@dp.message_handler(commands=['support'])
@dp.message_handler(lambda mesg: mesg.text == 'Поддержка')
async def balance_menu(message: types.Message, state: FSMContext):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    await state.finish()
    await message.answer(bot_mesg['support_menu'])


# /READY
@dp.message_handler(lambda mesg: mesg.text == 'Отменить' or mesg.text == 'Назад', state='*')
async def cancel_button_handler(message: types.Message, state: FSMContext):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    await state.finish()
    await send_welcome(message)


# /READY
async def i_dont_understant(message: types.Message):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    await message.answer('Я не понял вашу команду, нажмите /start')


if __name__ == "__main__":
    # Регистрируем обработчики(handlers) системы "Отмена заявок"
    cancel_order_system_handlers.register_cancel_system_handlers(dp)

    # Регистрируем обработчики(handlers) панели админа
    admin_panel.register_handlers_admin_panel(dp)

    # Регистрируем обработчики(handlers) модуля menus/products.py
    products.register_handlers_products(dp)

    # Регистрируем обработичи(handlers) модуля menus/profile.py
    profile.register_handlers_profile(dp)

    # Регистрируем обработичи(handlers) модуля menus/balance.py
    balance.register_handlers_balance(dp)

    # Регистрируем обработичи(handlers) модуля menus/feedbacks.py
    feedbacks.register_handlers_products(dp)

    # Регистрируем обработичи(handlers) модуля menus/earn.py
    earn.register_handlers_earn(dp)

    dp.register_message_handler(
        i_dont_understant
    )

    executor.start_polling(dp, skip_updates=True)


