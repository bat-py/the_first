from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import crypto_price
import sql_handler
from button_creators import *
import random


def feedback_count_button_handler(message: types.Message):
    """
    Если пользователь нажал на "Отзывы (4680)"
    :param message:
    :return:
    """
    feedbacks_count = sql_handler.get_feedback_count()
    mesg = f'Всего отзывов: {feedbacks_count}'

    # Получает [{'id': 10, 'rate': 10, 'order_date': datetime.date(2021, 10, 21)}, {'id'...}, ...]
    feedbacks = sql_handler.get_feedbacks(1)

    feedbacks_buttons = []
    for feedback in feedbacks:
        button_text = f'{str(feedback["rate"])}/10 | Бот | {feedback["order_date"].replace("-", ".")}'
        button_callback_date = f'feedback_id{str(feedback["id"])}'
        feedbacks_buttons.append([button_text, button_callback_date])



def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с отзывами
    :param dp:
    :return:
    """

