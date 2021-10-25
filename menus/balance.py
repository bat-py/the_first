from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *

# Getting all bot messages
with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# States
class MyStates(StatesGroup):
    waiting_for_payment_summa = State()
    waiting_for_payment_method = State()


async def payment_summa_chosen(message: types.Message, state: FSMContext):
    if message.text.isdigit() and message.text != '0':
        await message.answer('fuck you')
    else:
        await message.answer("<b>Ошибка</b>\n\nНеобходимо ввести сумму в руб!")
        return


async def balance_menu(callback_query_or_message):
    """
    Эту функцию могут запустить 2 обработчика. Смотри внизу на register_handlers_products
    :param callback_query_or_message:
    :return:
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


def register_handlers_products(dp: Dispatcher):
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

    # Если state пользователя равно waiting_for_payment_summa, тогда запускаем функцию payment_summa_chosen
    # Пользователь поподает в этот статус после нажатия на кнопку "Баланс"
    dp.register_message_handler(
        payment_summa_chosen,
        state=MyStates.waiting_for_payment_summa
    )