from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import sql_handler
from button_creators import *


async def start_command_handler(message_or_callback_query, state: FSMContext):
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
    sql_handler.del_member_orders(callback_query.from_user.id)


def register_cancel_system_handlers(dp: Dispatcher):
    # Если пользователь отправил /cancel тогда отправит "Отмена пополнение..." или "Отмена заказа ..."
    dp.register_message_handler(
        start_command_handler,
        commands=['cancel'],
        state='*'
    )

    # Запустится если пользователь нажал на inline кнопку "Да отменить пополнение" или "Да отменить заказ"
    dp.register_callback_query_handler(

    )