from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import sql_handler
from button_creators import *
import crypto_price

# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# States
class MyStates(StatesGroup):
    waiting_for_payment_summa = State()
    waiting_for_payment_method = State()


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


async def balance_menu(callback_query_or_message):
    """
    Эту функцию могут запустить 2 обработчика. Смотри внизу на register_handlers_products
    :param callback_query_or_message:
    :return: message like: "Пополнение баланса \n\n Ваш баланс: 0 руб ..." with reply button "Отменить"
    """
    if not sql_handler.check_user_exists(callback_query_or_message.from_user.id):
        return

    # Если пользователь за последный час открыл заявку на попол или покупку, тогда отправим "Необходимо отменить тек..."
    check_member_order_exist = sql_handler.check_member_order_exist(callback_query_or_message.from_user.id)
    if check_member_order_exist:
        await callback_query_or_message.bot.send_message(
            callback_query_or_message.from_user.id, bot_mesg['you_should_cancel_order_of_refill']
        )
        return


    balance = str(sql_handler.get_balance(callback_query_or_message.from_user.id))
    mesg = bot_mesg['balance_replenishment'].replace('xxx', balance)

    cancel_reply_button = reply_keyboard_creator([['Отменить']])

    # Статус меняем на waiting_for_payment_summa чтобы дальше все запросы обратал функция payment_summa_chosen
    await MyStates.waiting_for_payment_summa.set()

    await callback_query_or_message.bot.send_message(
        chat_id=callback_query_or_message.from_user.id,
        text=mesg,
        reply_markup=cancel_reply_button
    )


async def payment_summa_chosen(message: types.Message, state: FSMContext):
    """
    Запустится после того как пользователь ответил на "Введите на сколько хотите пополнить баланс (в руб)"
    :param message:
    :param state:
    :return: сообщение "Выберите способ пополнения:" с inline кнопками: Лайткоин, Биткоин, Банквской картой
    """
    # Если он ввел целое число, тогда перейдет на следуюшое окно: "Выберите способ пополнения:"
    if message.text.isdigit() and message.text != '0':
        mesg = 'Выберите способ пополнения:'

        aviable_payment_method = sql_handler.get_aviable_payments_methods()
        del (aviable_payment_method[0])

        buttons_list = []
        for i in aviable_payment_method:
            method_name = i['method_name']
            if method_name.strip() == 'Банковской картой':
                method_name = 'Банковской картой (Комиссия +13%)'
            callback_date = str(i['id'])

            buttons_list.append([method_name, callback_date])
        buttons_callback_data = [i[1] for i in buttons_list]

        ready_buttons = inline_keyboard_creator(buttons_list, row_width=1)

        # Добавим в FSMContext сумму пополнения который отправил пользователь
        await state.update_data(refill_summa=message.text)

        # В buttons_callback_data хранится callback_datas методов пополнение
        await state.update_data(payment_methods_buttons_callback_datas=buttons_callback_data)

        # Меняем статус на "waiting_for_payment_method"
        await MyStates.next()

        await message.answer(mesg, reply_markup=ready_buttons)

    else:
        await message.answer("<b>Ошибка</b>\n\nНеобходимо ввести сумму в руб!")
        return


async def payment_method_chosen(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Запустится после того как пользователь нажал на одну из этих кнопок: Лайткоин, Биткоин, Банквской картой
    :param callback_query:
    :param state:
    :return: сообщения "Номер заявки на попол...", "Переведите указанное...", "Если вы передумали..."
    Отправим сразу 2 вида кнопок: inline("Отменить пополнение баланса"), reply("Отменить пополнение", "Поддержка")
    """
    datas = await state.get_data()
    # Останавливаем state чтобы дальне он нам не мешал
    await state.finish()

    # Получаем рандомно адрес кашелько по выбранному типу
    wallet_address = sql_handler.randomly_get_wallet_address(callback_query.data)
    # Генирируем номер заявки
    order_number = gen_order_id()
    # Сумма который он хочет пополнить
    chosen_summa = datas['refill_summa']
    #Создаем reply кнопки
    reply_buttons = ['Отменить пополнение', 'Поддержка']
    cancel_support_buttons = reply_keyboard_creator([reply_buttons])

    # Если выбрал Лайткоин
    if callback_query.data == '2':
        # [ 'Курс_криптовалюты', 'сумма в выбранном методе оплаты' ]
        course_summa_in_chosen_currency = crypto_price.get_cource('ltc', chosen_summa)

        mesg1 = bot_mesg['number_applicatoin_to_refill_balance_ltc'] \
            .replace('***order_number***', order_number) \
            .replace('***chosen_summa***', chosen_summa) \
            .replace('***summa_in_chosen_currency***', str(course_summa_in_chosen_currency[1])) \
            .replace('***chosen_currency***', 'ltc')

        mesg2 = 'Переведите указанное количество ltc на этот кошелек:'
        mesg3 = wallet_address

        for mesg in mesg1, mesg2, mesg3:
            await callback_query.bot.send_message(
                callback_query.from_user.id,
                mesg,
                reply_markup=cancel_support_buttons
            )
    # Если выбрал Биткоин
    elif callback_query.data == '3':
        # [ 'Курс_криптовалюты', 'сумма в выбранном методе оплаты' ]
        course_summa_in_chosen_currency = crypto_price.get_cource('btc', chosen_summa)

        mesg1 = bot_mesg['number_applicatoin_to_refill_balance_btc'] \
            .replace('***order_number***', order_number) \
            .replace('***chosen_summa***', chosen_summa) \
            .replace('***summa_in_chosen_currency***', str(course_summa_in_chosen_currency[1])) \
            .replace('***chosen_currency***', 'btc')

        mesg2 = 'Переведите указанное количество btc на этот кошелек:'
        mesg3 = wallet_address

        for mesg in mesg1, mesg2, mesg3:
            await callback_query.bot.send_message(
                callback_query.from_user.id,
                mesg,
                reply_markup=cancel_support_buttons
            )
    # Если выбрал Банквскую карту
    else:
        summa_with_commission = str(int(chosen_summa)*1.13)
        mesg1 = bot_mesg['number_applicatoin_to_refill_balance_back_card'] \
            .replace('***order_number***', order_number) \
            .replace('***chosen_summa***', chosen_summa) \
            .replace('***summa_with_comission***', summa_with_commission)\
            .replace('***wallet***', wallet_address)

        await callback_query.bot.send_message(
            callback_query.from_user.id,
            mesg1,
            reply_markup=cancel_support_buttons
        )

    # Добавим пользователся в базу в течении часа если пользователь попытается открыть товары или баланс
    # он получит сообщение типа: "Необходимо отменить текущий заказ или пополнение баланса!
    #  Если вы хотите отменить текущий заказ или пополнение, введите /cancel"
    sql_handler.order_adder(callback_query.from_user.id, order_number, 'refill')

    wanna_cancel_text = 'Если вы передумали, и не хотите платить нажмите кнопку ниже.'
    button_text_data = ['Отменить пополнение баланса', 'cancel_refill_button']
    wanna_cancel_button = inline_keyboard_creator([button_text_data])

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        wanna_cancel_text,
        reply_markup=wanna_cancel_button
    )


def register_handlers_balance(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано Баланс
    :param dp:
    :return:
    """
    # Если пользователь отправил команду /addbalance
    dp.register_message_handler(
        balance_menu,
        commands=['addbalance']
    )

    # Если пользователь нажал на inline кнопку "Баланс (50)" из wecome, callback_query_handler запустит balance_menu
    dp.register_callback_query_handler(
        balance_menu,
        lambda c: c.data == 'balance'
    )

    # Если пользователь нажал на reply кнопку "Баланс" из главного меню, message_handler запустит balance_menu
    dp.register_message_handler(
        balance_menu,
        lambda message: message.text == 'Баланс'
    )

    # Если пользователь нажал на inline кнопку "Пополнить баланс" в меню Профиль
    dp.register_callback_query_handler(
        balance_menu,
        lambda c: c.data == 'balance_button_in_profile_menu'
    )

    # Если state пользователя равно waiting_for_payment_summa, тогда запускаем функцию payment_summa_chosen
    # Пользователь поподает в этот статус после нажатия на кнопку "Баланс"
    dp.register_message_handler(
        payment_summa_chosen,
        state=MyStates.waiting_for_payment_summa
    )

    # Если state пользователя равно waiting_for_payment_method, тогда зупускаем функцию payment_method_chosen
    # Пользователь попадает в этот статус ввода нажатия на кнопку: Лайткоин, Биткоин, Банквской картой
    dp.register_callback_query_handler(
        payment_method_chosen,
        state=MyStates.waiting_for_payment_method
    )
