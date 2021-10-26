from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_handler
from button_creators import *

# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# States
class MyStates(StatesGroup):
    waiting_for_payment_summa = State()
    waiting_for_payment_method = State()


async def balance_menu(callback_query_or_message):
    """
    Эту функцию могут запустить 2 обработчика. Смотри внизу на register_handlers_products
    :param callback_query_or_message:
    :return: message like: "Пополнение баланса \n\n Ваш баланс: 0 руб ..." with reply button "Отменить"
    """

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

            callback_date = 'balance_menu_method_id' + str(i['id'])
            buttons_list.append([method_name, callback_date])

        ready_buttons = inline_keyboard_creator(buttons_list, row_width=1)

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

    mesg1 =




def register_handlers_balance(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано Баланс
    :param dp:
    :return:
    """
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
