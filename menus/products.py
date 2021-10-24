from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *


async def waiting_for_product_type(callback_query_or_message, city_id):
    """
    Эту функцию может запускать либо chosen_city/(callback_query, city_id) либо products_menu/(message, city_id)
    либо кнопка 'Товары (Уфа)'
    Функция создает inline кнопки из списка товаров который есть в городе
    callback_data кнопок выглядит так: "city20;product30"
    :param callback_query_or_message: Здень он может получить либо callback_query либо message
    :param city_id:
    :return:
    """

    # Получает list с dict элементами: [ {id, type}, ... ]
    products_dict_list_in_city = sql_handler.get_products_from_city(city_id)

    products_list_list_in_city = []

    for product in products_dict_list_in_city:
        inline_button_text = product['type']
        callback_data = f'city{city_id};product{product["id"]}'
        products_list_list_in_city.append([inline_button_text, callback_data])

    inline_keyboards = inline_keyboard_creator(products_list_list_in_city, row_width=1)

    mesg = 'Выберите товар:'
    # Отправляем список товаров который есть в выбранном городе
    await callback_query_or_message.bot.send_message(chat_id=callback_query_or_message.from_user.id,
                                                     text=mesg,
                                                     reply_markup=inline_keyboards
                                                     )


async def chosen_city(callback_query: types.CallbackQuery):
    """
    Функция запустится если пользователь выбрал какой-нибудь город
    :param callback_query:
    :return: Возврашает сообщение "Выберите товар:"
    """
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

    # Запустим функцию который отправит сообщение "Выберите товар:"
    await waiting_for_product_type(callback_query, city_id)


async def chosen_product(callback_query: types.CallbackQuery):
    """
    Запускается если пользователь выбрал товар (например альфа или мефедрон).
    Получает callback_data как: "city10;product30"
    :param callback_query:
    :return:
    """
    callback_data = callback_query.data.split(';')
    city_id = callback_data[0].replace('city', '')
    product_id = callback_data[1].replace('product', '')
    chat_id = callback_query.from_user.id

    #сообщение "Наличие по {название города}",
    # сообщение "Выберите район:" с inline кнопками
    product_info = sql_handler.get_product_info(product_id)

    # Теперь отправим фотографию выбранного товара
    await callback_query.bot.send_photo(
        chat_id=chat_id,
        photo=open(f'images/{product_info["photo_name"]}', 'rb')
    )

    # Теперь отправим описание выбранного товара
    await callback_query.bot.send_message(
        chat_id=chat_id,
        text=product_info["about"]
    )

    # Теперь отправим сообщение "Наличие по {название города}"



def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано Локации и Товары
    :param dp:
    :return:
    """
    # Регистрируем обработчик который запускается после выбора какого-то города
    dp.register_callback_query_handler(
        chosen_city,
        lambda c: c.data.startswith('city_location') or c.data.startswith('city_welcome')
    )

    # Регистрируем обработчик который запускается после выбора товар (например мефедрон или альфа)
    dp.register_callback_query_handler(
        chosen_product,
        # Если получит callback_data как: "city10;product30"
        lambda c: c.data.startswith('city') and c.data.count(';') == 1
    )



