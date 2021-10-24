from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *


# City menu InlineKeyboardCreate handler
async def chosen_city(callback_query: types.CallbackQuery):
    # Если пользователь нажал на inline кнопку из welcome сообщении,
    # тогда запишем в базу выбранный город и отправим "Выбор сохранен"
    if callback_query.data.startswith('city_welcome'):
        # Записываем в базу выбранный город
        city_id = callback_query.data.replace('city_welcome', '')
        sql_handler.update_user_city(
            callback_query.from_user.id,
            city_id
        )

        ready_buttons = main_menu_buttons(callback_query.from_user.id)
        await callback_query.bot.send_message(
            callback_query.from_user.id,
            'Выбор сохранен. Спасибо!',
            reply_markup=ready_buttons
        )

    else:
        city_id = callback_query.data.replace('city_location', '')

    # Дальше мы покажем "Выберите товар:" и список товаров в этом районе
    mesg = 'Выберите товар:'


def register_handlers_products(dp: Dispatcher):
    dp.register_callback_query_handler(chosen_city, lambda c: c.data and c.data.startswith('city'))

