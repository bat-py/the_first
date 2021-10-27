from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import crypto_price
import sql_handler
from button_creators import *
import random

# Возврашает str типа: "BCCC-1087387"
def gen_order_id(access_code=None):
    if access_code:
        gen_access_code = str(random.randint(10000000, 99999999))
        return str(gen_access_code)

    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]

    order_id = ''
    for i in range(4):
        order_id += random.choice(letters).upper()

    order_number = str(random.randint(1000000, 9999999))

    return order_id+'-'+order_number


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

    ready_products_dict_list_in_city = []
    added_products = []
    for product in products_dict_list_in_city:
        if product['id'] not in added_products:
            added_products.append(product['id'])
            ready_products_dict_list_in_city.append(product)

    products_list_list_in_city = []
    for product in ready_products_dict_list_in_city:
        inline_button_text = product['type']
        callback_data = f'city{city_id};product{product["id"]}'
        products_list_list_in_city.append([inline_button_text, callback_data])

    inline_keyboards = inline_keyboard_creator(products_list_list_in_city, row_width=1)

    # Если в выбранном городе есть товары
    if products_list_list_in_city:
        mesg = 'Выберите товар:'
        # Отправляем список товаров который есть в выбранном городе
        await callback_query_or_message.bot.send_message(chat_id=callback_query_or_message.from_user.id,
                                                         text=mesg,
                                                         reply_markup=inline_keyboards
                                                         )
    else:
        mesg = 'Товаров пока нет'
        await callback_query_or_message.bot.send_message(chat_id=callback_query_or_message.from_user.id,
                                                         text=mesg
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
    :return: Фотографию товара, информацию о товаре, наличие по городу, "выберете город:" c inline кнопками
    """
    # Если пользователь за последный час открыл заявку на попол или покупку, тогда отправим "Необходимо отменить тек..."
    check_member_order_exist = sql_handler.check_member_order_exist(callback_query.from_user.id)
    if check_member_order_exist:
        # Отправим всплываюшое сообшение с кнопкой ОК
        await callback_query.bot.answer_callback_query(
            callback_query.id,
            bot_mesg['you_should_cancel_order_of_refill'],
            show_alert=True
        )
        return

    callback_data = callback_query.data.split(';')
    city_id = callback_data[0].replace('city', '')
    product_id = callback_data[1].replace('product', '')
    chat_id = callback_query.from_user.id

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

    # Получаем список доступных товаров выбраннотого типа в выбранном городе
    products = sql_handler.get_one_product_type_in_city(city_id, product_id)
    city_name = products[0]['city']
    product_name = products[0]['product']

    # Теперь отправим сообщение "Наличие по {название города}"
    msg1 = f'Наличие по г. {city_name}'

    products_massa = []
    for product in products:
        if product['massa'] not in products_massa:
            products_massa.append(product['massa'])

    # Теперь создаем msg2 который хранить строки как: АЛЬФА (ПВП) КРИСТАЛЛ - 0.50 г, районы: северо-восточный, свесткий
    msg2 = ''
    for massa in products_massa:
        rayons = []
        # Будет хранить массив как: [rayon_text, callback_data_to_rayon]
        for product in products:
            if product['massa'] == massa:
                rayons.append(product['rayon'].lower())

        part_msg2 = f'<b>{product_name} - {massa.replace("gr", " г")}</b>, районы: {", ".join(rayons)}\n'
        msg2 += part_msg2

    await callback_query.bot.send_message(
        chat_id=chat_id,
        text=f'{msg1}\n\n{msg2}'
    )

    # Отправим сообщение "Выберите район:" c inline кнопками
    # Хранит в себе [ [rayon_name, callback_data], ...] В callback_data будет "city10;product30;rayon20"
    rayon_name_callback_data = []

    added_rayons_id = []
    for product in products:
        if product['rayon_id'] not in added_rayons_id:
            inline_rayon_button = [product['rayon'], f"{callback_query.data};rayon{product['rayon_id']}"]
            rayon_name_callback_data.append(inline_rayon_button)

            added_rayons_id.append(product['rayon_id'])

    inline_rayon_buttons = inline_keyboard_creator(rayon_name_callback_data, row_width=1)
    # Теперь отправим сообщение "Выберите район:" с inline кнопками
    await callback_query.bot.send_message(
        chat_id=chat_id,
        text='Выберите район:',
        reply_markup=inline_rayon_buttons
    )


async def chosen_rayon(callback_query: types.CallbackQuery):
    """
    Запускается если пользователь выбрал район товора
    :param callback_query: callback_query.data is like: 'city20;product40;rayon60'
    :return: сообщения "Выберите фасовку для товара АЛЬФА (ПВП) КРИСТАЛЛ:" с inline кнопками где показано "масса - цена"
    """
    chat_id = callback_query.from_user.id

    callback_data = callback_query.data.split(';')
    city_id = callback_data[0].replace('city', '')
    product_id = callback_data[1].replace('product', '')
    rayon_id = callback_data[2].replace('rayon', '')

    product_name = sql_handler.get_product_name_by_id(product_id)['product_name']
    rayon_name = sql_handler.get_rayon_name_by_id(rayon_id)['rayon_name']

    # Отправляем сообщение как: "Вы выбрали район Северо-Восточный"
    await callback_query.bot.send_message(
        chat_id=chat_id,
        text=f'Вы выбрали район {rayon_name}'
    )

    # Отправим сообщение "Выберите фасовку для товара {product_name}" c inline кнопками типа "0.5 г - 1500р"
    # Сперва определим какие есть фасовки выбранного товара в выбранном районе
    massa_price_list = sql_handler.get_product_massas_price_in_chosen_rayon(city_id, product_id, rayon_id)
    mesg = f'Выберите фасовку для товара {product_name}'

    inline_buttons_list = []
    for i in massa_price_list:
        price = str(i["price"])
        ready_price = price[:-3] + ' ' + price[-3:]
        button_text = f'{i["massa"].replace("gr", "")} г - {ready_price} руб'
        callback_data = f'{callback_query.data};massa{i["massa_id"]}'
        inline_buttons_list.append([button_text, callback_data])

    # Создаем кнопки
    ready_buttons = inline_keyboard_creator(inline_buttons_list, row_width=1)

    await callback_query.bot.send_message(
        chat_id=chat_id,
        text=mesg,
        reply_markup=ready_buttons
    )


async def chosen_massa(callback_query: types.CallbackQuery):
    """
    Запускается если пользователь выбрал фасовку. Получает callback.data типа: "city20;product40;rayon60;massa30"
    :param callback_query:
    :return: Отправит сообщение "Выберите тип клада:" с inline кнопками.
    """
    chat_id = callback_query.from_user.id

    callback_data_list = callback_query.data.split(';')
    city_id = callback_data_list[0].replace('city', '')
    product_id = callback_data_list[1].replace('product', '')
    rayon_id = callback_data_list[2].replace('rayon', '')
    massa_id = callback_data_list[3].replace('massa', '')

    mesg = "Выберите тип клада:"

    aviable_klads = sql_handler.get_aviable_klads_type(city_id, product_id, rayon_id, massa_id)

    list_for_create_buttons = []
    for i in aviable_klads:
        button_text = i['klad_name']
        button_callback_data = f'{callback_query.data};klad_type{i["klad_id"]}'
        button = [button_text, button_callback_data]
        list_for_create_buttons.append(button)
    ready_inline_buttons = inline_keyboard_creator(list_for_create_buttons, row_width=1)

    await callback_query.bot.send_message(
        chat_id=chat_id,
        text=mesg,
        reply_markup=ready_inline_buttons
    )


async def chosen_klad_type(callback_query: types.CallbackQuery):
    """
    Запускается если пользователь выбрал тип клада. Получает callback.data типа: "city20;product40;rayon60;massa30;klad_type20"
    :param callback_query:
    :return: Отправит сообщение "Выберите способ оплаты:"  c inline кнопками: Оплата с баланса, Лайткоин ...
    """
    chat_id = callback_query.from_user.id
    user_balance = str(sql_handler.get_balance(chat_id))

    callback_data_list = callback_query.data.split(';')
    city_id = callback_data_list[0].replace('city', '')
    product_id = callback_data_list[1].replace('product', '')
    rayon_id = callback_data_list[2].replace('rayon', '')
    massa_id = callback_data_list[3].replace('massa', '')
    klad_type_id = callback_data_list[4].replace('klad_type', '')
    product_price = sql_handler.product_price(city_id, product_id, rayon_id, massa_id, klad_type_id)

    if not product_price:
        return
    else:
        product_price = product_price['price']

    # Из 1000 сделаем "1 000"
    price = str(product_price)
    ready_price = price[:-3] + ' ' + price[-3:]

    # Получит [{id, status, method_name, my_wallet}, {}, ...]
    aviable_payment_methods = sql_handler.get_aviable_payments_methods()

    buttons = []
    # Создаем кнопки из доступных методов оплаты
    for method in aviable_payment_methods:
        # Оплата с баланса
        if method['id'] == 1:
            mesg = f'Оплата с баланса - {ready_price} руб (у вас {user_balance} руб)'
        # Лайткоин
        elif method['id'] == 2:
            price_in_ltc = crypto_price.get_cource('ltc', product_price)
            mesg = f'Лайткоин - {ready_price} ({price_in_ltc[1]} ltc)'
        # Биткоин
        elif method['id'] == 3:
            price_in_btc = crypto_price.get_cource('btc', product_price)
            mesg = f'Биткоин - {ready_price} ({price_in_btc[1]} btc)'
        # Банквская карта
        elif method['id'] == 4:
            mesg = f'Банковской картой - {str(int(product_price * 1.13))} руб'
        else:
            return

        callback_date = callback_query.data + f';p{str(method["id"])}'
        buttons.append([mesg, callback_date])

    mesg = 'Выберите способ оплаты:'
    ready_buttons = inline_keyboard_creator(buttons, row_width=1)

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg,
        reply_markup=ready_buttons
    )


async def chosen_payment_method(callback_query: types.CallbackQuery):
    """
    Запускается если пользователь выбрал метод оплаты
    :param callback_query:
    :return: Сообшение "Информация о заказе" с inline кнопкой "Подтвердить"
    """
    callback_data_list = callback_query.data.split(';')
    city_id = callback_data_list[0].replace('city', '')
    product_id = callback_data_list[1].replace('product', '')
    rayon_id = callback_data_list[2].replace('rayon', '')
    massa_id = callback_data_list[3].replace('massa', '')
    klad_type_id = callback_data_list[4].replace('klad_type', '')
    payment_method_id = callback_data_list[5].replace('p', '')
    product_price = sql_handler.product_price(city_id, product_id, rayon_id, massa_id, klad_type_id)['price']

    price = str(product_price)
    ready_price = price[:-3] + ' ' + price[-3:]

    # Если выбрал "Оплата с баланса"
    if payment_method_id == '1':
        mesg = bot_mesg['insufficient_balance']
        await callback_query.bot.send_message(callback_query.from_user.id, mesg)
        return

    # Если выбрал другие методы:
    # Получает: {'city': 'Уфа', 'product': 'Шишки', 'rayon': 'Юматово', 'massa': '2.00gr', 'klad_type': 'Тайник'}
    column_names = sql_handler.get_columns_name_by_id(city_id,
                                                      product_id,
                                                      rayon_id,
                                                      massa_id,
                                                      klad_type_id)
    # Получает {'method_name'}
    column_name_payment_method = sql_handler.get_column_name_payment_method(payment_method_id)


    # Создаем сообшение "Информация о заказе..."
    mesg = bot_mesg['about_order'].replace('***city***', column_names['city'])\
                                               .replace('***rayon***', column_names['rayon'])\
                                               .replace('***product***', column_names['product'])\
                                               .replace('***massa***', column_names['massa'].replace('gr', ''))\
                                               .replace('***price***', ready_price)\
                                               .replace('***klad_type***', column_names['klad_type'])\
                                               .replace('***paymnet_method***', column_name_payment_method['method_name'])

    button = inline_keyboard_creator([['Подтвердить', callback_query.data+';confirmed']])

    # Отправляем "Информация о заказе" и просим подтверждение
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg,
        reply_markup=button
    )


async def order_confirmed(callback_query: types.CallbackQuery):
    """
    Запустится после того как пользователь нажал на inline кнопку "Подтвердить"
    :param callback_query:
    :return: сообщения "Номер заказа: OPWP-1294096 ...", "Если вы передумали..."
    Отправим сразу 2 вида кнопок: inline("Отменить пополнение баланса"), reply("Отменить пополнение", "Поддержка")
    """
    chat_id = callback_query.from_user.id
    callback_data_list = callback_query.data.split(';')
    city_id = callback_data_list[0].replace('city', '')
    product_id = callback_data_list[1].replace('product', '')
    rayon_id = callback_data_list[2].replace('rayon', '')
    massa_id = callback_data_list[3].replace('massa', '')
    klad_type_id = callback_data_list[4].replace('klad_type', '')
    payment_method_id = callback_data_list[5].replace('p', '')
    product_price = sql_handler.product_price(city_id, product_id, rayon_id, massa_id, klad_type_id)['price']
    wallet_addess = sql_handler.randomly_get_wallet_address(payment_method_id)
    order_number = gen_order_id()
    access_code = gen_order_id(access_code=True)

    #Создаем reply кнопки
    reply_buttons = ['Отменить заказ', 'Поддержка']
    cancel_support_buttons = reply_keyboard_creator([reply_buttons])

    if payment_method_id == '2':
        price_in_ltc = crypto_price.get_cource('ltc', product_price)
        mesg1 = bot_mesg['number_applicatoin_to_buy_product_ltc'].replace('***order_number***', order_number)\
                                                                 .replace('***access_code***', access_code)
        mesg2 = price_in_ltc[1]
        mesg3 = 'На Лайткоин адрес:'
        mesg4 = wallet_addess
        mesg5 = bot_mesg['warning_dont_cancel']

        for mesg in mesg1, mesg2, mesg3, mesg4:
            await callback_query.bot.send_message(chat_id, mesg)
        await callback_query.bot.send_message(chat_id, mesg5, reply_markup=cancel_support_buttons)

    elif payment_method_id == '3':
        price_in_btc = crypto_price.get_cource('btc', product_price)
        mesg1 = bot_mesg['number_applicatoin_to_buy_product_btc'].replace('***order_number***', order_number) \
                                                                 .replace('***access_code***', access_code)
        mesg2 = price_in_btc[1]
        mesg3 = 'На Биткоин адрес:'
        mesg4 = wallet_addess
        mesg5 = bot_mesg['warning_dont_cancel']

        for mesg in mesg1, mesg2, mesg3, mesg4:
            await callback_query.bot.send_message(chat_id, mesg)
        await callback_query.bot.send_message(chat_id, mesg5, reply_markup=cancel_support_buttons)

    else:
        mesg = bot_mesg['number_applicatoin_to_buy_product_card'].replace('***order_number***', order_number) \
                                                                  .replace('***access_code***', access_code)\
                                                                  .replace('***price***', str(product_price))\
                                                                  .replace('***wallet***', wallet_addess)
        await callback_query.bot.send_message(chat_id, mesg, reply_markup=cancel_support_buttons)


    # Добавим пользователся в базу в течении часа если пользователь попытается открыть товары или баланс
    # он получит сообщение типа: "Необходимо отменить текущий заказ или пополнение баланса!
    #  Если вы хотите отменить текущий заказ или пополнение, введите /cancel"
    sql_handler.order_adder(callback_query.from_user.id, order_number, 'product_order')

    wanna_cancel_text = 'Если вы передумали, и не хотите платить нажмите кнопку ниже.'
    button_text_data = ['Отменить заказ', 'cancel_order_button']
    wanna_cancel_button = inline_keyboard_creator([button_text_data])

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        wanna_cancel_text,
        reply_markup=wanna_cancel_button
    )


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

    # Регистрируем обработчик который запускается послле выбора района
    dp.register_callback_query_handler(
        chosen_rayon,
        # Если получит callback_data как: "city20;product40;rayon60"
        lambda c: c.data.startswith('city') and c.data.count(';') == 2
    )

    # Регистрируем обработчик который запускается после выбора массы
    dp.register_callback_query_handler(
        chosen_massa,
        # Если получит callback_data как: "city20;product40;rayon60;massa20"
        lambda c: c.data.startswith('city') and c.data.count(';') == 3
    )

    # Регистрируем обработчик который запускается после выбора типа клада
    dp.register_callback_query_handler(
        chosen_klad_type,
        # Если получит callback_data как: "city20;product40;rayon60;massa20;klad_type20"
        lambda c: c.data.startswith('city') and c.data.count(';') == 4
    )

    # Регистрируем обработчик который запускается после выбора метода оплаты
    dp.register_callback_query_handler(
        chosen_payment_method,
        # Если получит callback_data как: "city20;product40;rayon60;massa20;klad_type20;p10"
        lambda c: c.data.startswith('city') and c.data.count(';') == 5
    )

    # Регистрируем обработчик который запускается после нажатия на кнопку Подтвердить
    dp.register_callback_query_handler(
        order_confirmed,
        # Если получит callback_data как: "city20;product40;rayon60;massa20;klad_type20;p10;confirmed"
        lambda c: c.data.startswith('city') and c.data.count(';') == 6
    )