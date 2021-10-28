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

    feedback_list =

def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с отзывами
    :param dp:
    :return:
    """

