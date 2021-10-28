from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *
import json

with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# States in profile menu
class ProfileMenuStates(StatesGroup):
    waiting_for_coupon_code = State()


async def profile_menu(message: types.Message):
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    # Если пользователь за последный час открыл заявку на попол или покупку, тогда отправим "Необходимо отменить тек..."
    check_member_order_exist = sql_handler.check_member_order_exist(message.from_user.id)

    if check_member_order_exist:
        await message.bot.send_message(message.from_user.id, bot_mesg['you_should_cancel_order_of_refill'])
        return

    user_id = str(message.from_user.id)
    balance = str(sql_handler.get_balance(user_id))

    mesg = bot_mesg['profile_menu'] \
        .replace('***profile_id***', user_id)\
        .replace('***balance***', balance)

    inline_buttons = [
        ['История заказов', 'order_history'],
        ['Пополнить баланс', 'balance_button_in_profile_menu'],
        ['Заработать', 'earn_button_in_profile_menu'],
        ['Активировать купон', 'activate_coupon']
    ]

    ready_button = inline_keyboard_creator(inline_buttons, row_width=2)

    await message.answer(
        text=mesg,
        reply_markup=ready_button
    )


# /READY
async def order_history_keyboard_handler(callback_query: types.CallbackQuery):
    """
    Запускается когда пользователь нажал на inline кнопку 'История заказов'
    :param callback_query:
    :return: Историю заказов или "У вас нет ни одного заказа!"
    """
    mesg = 'У вас нет ни одного заказа!'

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg
    )


# /READY
async def activate_coupon_keyboard_handler(callback_query: types.CallbackQuery):
    """
    Запустится если пользователь нажал на inline кнопку в "Активировать купон" в меню Профиль
    :param callback_query:
    :return: Введите код купона, потом state меняется на waiting_for_coupon
    """
    cancel_button = reply_keyboard_creator([['Отменить']])
    mesg = bot_mesg['input_coupon_code']

    # State пользователя меняем на waiting_for_coupon_code
    await ProfileMenuStates.waiting_for_coupon_code.set()

    # Отправляем сообшение "Введите код купона:":
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg,
        reply_markup=cancel_button
    )


# /READY
async def check_coupon_code(message: types.Message, state: FSMContext):
    mesg = bot_mesg['wrong_coupon_code']

    await message.answer(mesg)


def register_handlers_profile(db: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с кнопкой "Заработать"
    :param db:
    :return:
    """

    db.register_message_handler(
        profile_menu,
        lambda message: message.text == 'Профиль'
    )

    db.register_callback_query_handler(
        order_history_keyboard_handler,
        lambda c: c.data == 'order_history'
    )

    db.register_callback_query_handler(
        activate_coupon_keyboard_handler,
        lambda c: c.data == 'activate_coupon'
    )

    db.register_message_handler(
        check_coupon_code,
        state=ProfileMenuStates.waiting_for_coupon_code
    )
