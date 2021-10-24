from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *
from button_creators import *

# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


async def balance_menu(callback_query_or_message):
    """
    Эту функцию могут запустить 2 обработчика. Смотри внизу на register_handlers_products
    :param callback_query_or_message:
    :return:
    """

    balance = str(sql_handler.get_balance(callback_query_or_message.from_user.id))
    mesg = bot_mesg['balance_replenishment'].replace('xxx', balance)

    cancel_reply_button = reply_keyboard_creator([['Отменить']])

    await callback_query_or_message.bot.send_message(
        chat_id=callback_query_or_message.from_user.id,
        text=mesg,
        reply_markup=cancel_reply_button
    )


def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано Баланс
    :param dp:
    :return:
    """
    # Если пользователь нажал на inline кнопку "Баланс (50)" из wecome, callback_query_handler запустит balance_menu
    dp.register_callback_query_handler(
        balance_menu,
        lambda c: c.data == 'balance'
    )

    # Если пользователь нажал на reply кнопку "Баланс" из главного меню, message_handler запустит balance_menu
    dp.register_message_handler(
        balance_menu,
        lambda message: message.text == 'Баланс'
    )
