from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import crypto_price
import sql_handler
from button_creators import *
import random


async def feedback_count_button_handler(message: types.Message):
    """
    Если пользователь нажал на "Отзывы (4680)"
    :param message:
    :return: Последные 10 отзывов + пнопка вперед. Все это с помощью inline кнопок
    """
    if not sql_handler.check_user_exists(message.from_user.id):
        return

    feedbacks_count = sql_handler.get_feedback_count()
    mesg = f'Всего отзывов: {feedbacks_count}'

    # Получает [{'id': 10, 'rate': 10, 'order_date': datetime.date(2021, 10, 21)}, {'id'...}, ...]
    feedbacks = sql_handler.get_feedbacks(1)

    feedbacks_buttons = []
    for feedback in feedbacks:
        day = str(feedback["order_date"].day)
        month = str(feedback["order_date"].month)
        year = str(feedback["order_date"].year)[-2:]
        button_text = f'    {str(feedback["rate"])}/10 | Бот | {day}.{month}.{year}    '
        button_callback_data = f'feedback_id{str(feedback["id"])}'
        feedbacks_buttons.append([button_text, button_callback_data])

    button_text = '>>'
    button_callback_data = 'feedback_page2'
    feedbacks_buttons.append([button_text, button_callback_data])

    ready_buttons = inline_keyboard_creator(feedbacks_buttons, row_width=1)

    await message.answer(mesg, reply_markup=ready_buttons)


async def feedback_info_handler(callback_query: types.CallbackQuery):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']

    feedback_id = callback_query.data.replace('feedback_id', '')

    feedback_data = sql_handler.get_feedback_by_id(feedback_id)
    day = str(feedback_data["order_date"].day)
    month = months[feedback_data["order_date"].month - 1]
    year = str(feedback_data["order_date"].year)
    date = f'{day} {month} {year} г.'

    mesg = f'<b>Отзыв</b>\n\nДата: {date}\nПокупатель: {feedback_data["customer_name"]}\nОценка: {feedback_data["rate"]} из 10\nОтзыв: {feedback_data["feedback_text"]}'
    await callback_query.bot.send_message(callback_query.from_user.id, mesg)


async def feedback_by_page_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    page = int(callback_query.data.replace('feedback_page', ''))

    # Получает [{'id': 10, 'rate': 10, 'order_date': datetime.date(2021, 10, 21)}, {'id'...}, ...]
    feedbacks = sql_handler.get_feedbacks(page)

    ready_buttons = InlineKeyboardMarkup(row_width=2)

    # Добавляем 10 отзывов
    for feedback in feedbacks:
        day = str(feedback["order_date"].day)
        month = str(feedback["order_date"].month)
        year = str(feedback["order_date"].year)[-2:]
        button_text = f'    {str(feedback["rate"])}/10 | Бот | {day}.{month}.{year}    '
        button_callback_data = f'feedback_id{str(feedback["id"])}'

        button = InlineKeyboardButton(button_text, callback_data=button_callback_data)
        ready_buttons.add(button)

    # Если просит первую страницу, то он отправит 1 страницу с одно кнопкой ">>"
    if page == 1:
        paginate_button = InlineKeyboardButton('>>', callback_data='feedback_page2')
        ready_buttons.add(paginate_button)
    else:
        previous_page = page - 1
        next_page = page + 1

        previous_button = InlineKeyboardButton('<<', callback_data=f'feedback_page{previous_page}')
        next_button = InlineKeyboardButton('>>', callback_data=f'feedback_page{next_page}')
        ready_buttons.add(previous_button, next_button)

    await callback_query.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=ready_buttons
    )


def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с отзывами
    :param dp:
    :return:
    """

    dp.register_message_handler(
        feedback_count_button_handler,
        lambda message: message.text.startswith('Отзывы')
    )

    dp.register_callback_query_handler(
        feedback_info_handler,
        lambda c: c.data.startswith('feedback_id')
    )

    dp.register_callback_query_handler(
        feedback_by_page_handler,
        lambda c: c.data.startswith('feedback_page')
    )