import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import sql_handler
from button_creators import *


class MyStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_feedback_count = State()

    waiting_for_new_password = State()
    waiting_for_confirm_password = State()

    waiting_for_mailing_message = State()
    waiting_for_mailing_confirm = State()


async def admin_panel(message: types.Message, state: FSMContext):
    mesg = 'Введите пароль:'
    cancel_button = reply_keyboard_creator([['Отменить']])

    await MyStates.waiting_for_password.set()
    await message.answer(mesg, reply_markup=cancel_button)


async def check_password(message: types.Message, state: FSMContext):
    password = sql_handler.get_password()

    if message.text != password:
        await message.answer('❌ Неверный пароль!')
        return

    await state.finish()
    mesg = 'Добро пожаловать :)'
    buttons_list = [
        ['Отправить рассылку', 'send_mailing'],
        ['Изменить количество отзывов', 'change_feedbacks_count'],
        ['Изменить пароль', 'change_password']
    ]
    ready_buttons = inline_keyboard_creator(buttons_list, row_width=1)

    await message.answer(mesg, reply_markup=ready_buttons)


# Send mailing
async def send_mailing_handler(callback_query: types.CallbackQuery, state: FSMContext):
    mesg = 'Отправьте сообщение для рассылки'

    await MyStates.waiting_for_mailing_message.set()
    button = reply_keyboard_creator([['Назад']])
    await callback_query.bot.send_message(callback_query.from_user.id, mesg, reply_markup=button)


async def mailing_message(message: types.Message, state: FSMContext):
    await state.finish()
    await state.update_data(mailing_message=message.text)

    mesg = 'Подтверждаете рассылку'
    inline_buttons = [
        ['Да, подтверждаю', 'yes_confirm_mailing'],
        ['Нет, хочу отправить другое сообщение', 'no_send_another_mailing']
    ]
    ready_buttons = inline_keyboard_creator(inline_buttons)

    await message.answer(
        mesg,
        reply_markup=ready_buttons
    )


async def mailing_confirmed(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    mailing_message = state_data['mailing_message']
    await state.finish()

    users_chat_id = sql_handler.get_users_chat_id()

    mesg = '✅ Рассылка началась'
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg
    )

    for chat_id in users_chat_id:
        await callback_query.bot.send_message(chat_id, mailing_message)


# Change feedbacks count
# /READY
async def changer_feedback_count(callback_query: types.CallbackQuery, state: FSMContext):
    mesg = 'Напишите количество отзывов:'

    await MyStates.waiting_for_feedback_count.set()
    await callback_query.bot.send_message(callback_query.from_user.id, mesg)


# /READY
async def feedback_count_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Только целое число!')
        return

    sql_handler.update_feedback_count(message.text)
    mesg = '✅ Количество отзывов успешно обнавлен'
    button = reply_keyboard_creator([['Назад']])

    await state.finish()
    await message.answer(
        mesg,
        reply_markup=button
    )


# Change password
# /READY
async def password_change_handler(callback_query: types.CallbackQuery, state: FSMContext):
    mesg = 'Новый пароль:'

    await MyStates.waiting_for_new_password.set()
    await callback_query.bot.send_message(callback_query.from_user.id, mesg)


# /READY
async def password_first_time(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    mesg = 'Отправьте повторно:'

    await MyStates.waiting_for_confirm_password.set()
    await message.answer(mesg)


# /READY
async def password_confirm_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    first_password = state_data['password']

    if first_password == message.text:
        sql_handler.update_password(first_password)
        await state.finish()

        mesg = '✅ Пароль успешно обнавлен'
        button = reply_keyboard_creator([['Назад']])
        await message.answer(mesg, reply_markup=button)

    else:
        mesg = '❌ Пароли не совподают, попробуйте еще раз:'
        await message.answer(mesg)


def register_handlers_admin_panel(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано c админ панелью
    :param dp:
    :return:
    """

    # Регистрируем обработчик который запускается если пользователь отправил /admin
    dp.register_message_handler(
        admin_panel,
        commands=['admin']
    )

    dp.register_message_handler(
        check_password,
        state=MyStates.waiting_for_password
    )

    # Mailing system
    dp.register_callback_query_handler(
        send_mailing_handler,
        lambda c: c.data == 'send_mailing' or c.data == 'no_send_another_mailing'
    )

    dp.register_message_handler(
        mailing_message,
        state=MyStates.waiting_for_mailing_message
    )

    dp.register_callback_query_handler(
        mailing_confirmed,
        lambda c: c.data == 'yes_confirm_mailing'
    )

    # Feedback count updater system
    dp.register_callback_query_handler(
        changer_feedback_count,
        lambda c: c.data == 'change_feedbacks_count'
    )

    dp.register_message_handler(
        feedback_count_handler,
        state=MyStates.waiting_for_feedback_count
    )

    # Change password
    dp.register_callback_query_handler(
        password_change_handler,
        lambda c: c.data == 'change_password'
    )

    dp.register_message_handler(
        password_first_time,
        state=MyStates.waiting_for_new_password
    )

    dp.register_message_handler(
        password_confirm_handler,
        state=MyStates.waiting_for_confirm_password
    )
