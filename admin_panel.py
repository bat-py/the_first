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


# Change feedbacks count
async def changer_feedback_count(callback_query: types.CallbackQuery, state: FSMContext):
    mesg = 'Напишите количество отзывов:'

    await MyStates.waiting_for_feedback_count.set()
    await callback_query.bot.send_message(callback_query.from_user.id, mesg)


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
async def password_change_handler(callback_query: types.CallbackQuery, state: FSMContext):
    mesg = 'Новый пароль:'

    await MyStates.waiting_for_new_password.set()
    await callback_query.bot.send_message(callback_query.from_user.id, mesg)


async def password_first_time(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    mesg = 'Отправьте повторно:'

    await MyStates.waiting_for_confirm_password.set()
    await message.answer(mesg)


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