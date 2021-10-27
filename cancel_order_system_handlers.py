from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import sql_handler
from button_creators import *
import main


async def cancel_command_handler(message_or_callback_query, state: FSMContext):
    """
    Запускается если пользователь отправил команду /cancel
    :param message_or_callback_query:
    :param state:
    :return: Если у ползователя есть открытая заявка тогда вернет сообщение: "Отмена пополнения.." или "Отмена заказа.."
    Если у пользователя нету открытых заявок, тогда вернет сообщение "Нечего отменять"
    """
    await state.finish()

    check_order = sql_handler.check_member_order_exist(message_or_callback_query.from_user.id)
    if check_order:
        # Если пользователь в течении часа отправил заявку на пополнение счета (refill)
        if check_order['type'] == 'refill':
            mesg = f'<b>Отмена пополнения {check_order["order_number"]}</b>\nВы действительно хотите отменить заказ?'
            what_to_cancel = 'пополнение'

        # Если пользователь в течении часа отправил заявку на покупку товара (product_order)
        else:
            mesg = f'<b>Отмена заказа {check_order["order_number"]}</b>\nВы действительно хотите отменить заказ?'
            what_to_cancel = 'заказ'

        inline_buttons_text_data = [
            [f'Да, отменить {what_to_cancel}', 'yes_cancel_order'],
            ['Нет, я передумал', 'no_i_changed_my_mind']
        ]
        ready_buttons = inline_keyboard_creator(inline_buttons_text_data)

        await message_or_callback_query.bot.send_message(
            message_or_callback_query.from_user.id,
            mesg,
            reply_markup=ready_buttons
        )
    else:
        mesg = 'Нечего отменять'
        await message_or_callback_query.bot.send_message(
            message_or_callback_query.from_user.id,
            mesg)


async def cancel_order(callback_query: types.CallbackQuery):
    """
    Запустится если пользователь нажал на "Да отменить пополнение..." или "Да отменить заказ..." (yes_cancel_order)
    :param callback_query:
    :return: main.send_welcome
    """
    # Удаляем все заказы пользователя из базы
    sql_handler.del_member_orders(callback_query.from_user.id)

    await main.send_welcome(callback_query)


async def no_dont_cancel_order(callback_query: types.CallbackQuery):
    """
    Запустится если пользователь нажал на "Нет я передумал" (no_i_changed_my_mind)
    :param callback_query:
    :return: Всплываюшое окно "Ок. Ждем перевод"
    """
    await callback_query.answer('Ок. Ждем перевод')


def register_cancel_system_handlers(dp: Dispatcher):
    # Если пользователь отправил /cancel тогда отправит "Отмена пополнение..." или "Отмена заказа ..."
    dp.register_message_handler(
        cancel_command_handler,
        commands=['cancel'],
        state='*'
    )

    # Запустится если пользователь нажал на inline кнопку "Да отменить пополнение" или "Да отменить заказ"
    dp.register_callback_query_handler(
        cancel_order,
        lambda c: c.data == 'yes_cancel_order'
    )

    # Запустится если пользователь нажал на inline кнопку "Нет, я передумал"
    dp.register_callback_query_handler(
        no_dont_cancel_order,
        lambda c: c.data == 'no_i_changed_my_mind'
    )

    # Запустится если пользователь нажал на inline кнопку "Отменить пополнение баланса" (cancel_refill)
    # Вернем сообшение "Отмена пополнения XOGC-2185246..." с двумя inline кнопками  "Да" и "Нет"
    dp.register_callback_query_handler(
        cancel_command_handler,
        lambda c: c.data == 'cancel_refill_button',
        state='*'
    )

    # Запустится если пользователь нажал на inline кнопку "Отменить заказ" (cancel_order_button)
    # Вернем сообшение "Отмена заказа XOGC-2185246..." с двумя inline кнопками  "Да" и "Нет"
    dp.register_callback_query_handler(
        cancel_command_handler,
        lambda c: c.data == 'cancel_order_button',
        state='*'
    )


    # Запустится если пользователь нажал на reply кнопку "Отменить пополнение" или "Отменить заказ"
    dp.register_message_handler(
        cancel_command_handler,
        lambda message: message.text == "Отменить пополнение" or message.text == "Отменить заказ"
    )