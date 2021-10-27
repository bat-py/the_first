from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import sql_handler
from button_creators import *





@dp.message_handler(commands=['admin'], state='*')
async def admin_panel(message: types.Message, state: FSMContext):
    await state.finish()




def register_handlers_admin_panel(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано c админ панелью
    :param dp:
    :return:
    """
    # Регистрируем обработчик который запускается после выбора какого-то города
    dp.register_callback_query_handler(
        chosen_city,
        lambda c: c.data.startswith('city_location') or c.data.startswith('city_welcome')
    )