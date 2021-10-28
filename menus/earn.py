from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *


# /READY
async def earn_menu(message_or_callback_query):
    """
    Запускается если пользователь нажал на reply кнопку "Заработать" в главное меню или
    если нажал на inline кнопку заработать в profile_menu
    :param message_or_callback_query:
    :return: Сперва отправит сообщение "Ваш код реферала: SSYLP8T",
    потом "Вы можете заработать приглашая покупателей." c inline кнопкой "Подробнее"
    """
    if not sql_handler.check_user_exists(message_or_callback_query.from_user.id):
        return

    # Если пользователь за последный час открыл заявку на попол или покупку, тогда отправим "Необходимо отменить тек..."
    check_member_order_exist = sql_handler.check_member_order_exist(message_or_callback_query.from_user.id)
    if check_member_order_exist:
        await message_or_callback_query.bot.send_message(
            message_or_callback_query.from_user.id, bot_mesg['you_should_cancel_order_of_refill']
        )
        return

    chat_id = message_or_callback_query.from_user.id
    referal_code = sql_handler.get_referal_code(chat_id)['referal']
    your_referal_code_mesg = bot_mesg['your_referal_code'].replace('xxx', referal_code)
    # Отправляем 1-сообщение: Ваш код реферала: ....
    await message_or_callback_query.bot.send_message(chat_id, your_referal_code_mesg)

    # Создадим кнопку Подробнее и отправим с сообщением "Вы можете заработать приглашая покупателей...."
    more_details_button = inline_keyboard_creator([['Подробнее', 'about_referal']])
    await message_or_callback_query.bot.send_message(
        chat_id,
        bot_mesg['about_referal_system'],
        reply_markup=more_details_button
    )


# /READY
async def more_details_button_handler(callback_query: types.CallbackQuery):
    mesg = bot_mesg['more_details_button_answer']
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        mesg
    )


def register_handlers_earn(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с кнопкой "Заработать"
    :param dp:
    :return:
    """

    dp.register_message_handler(
        earn_menu,
        lambda message: message.text == 'Заработать'
    )

    dp.register_callback_query_handler(
        earn_menu,
        lambda c: c.data == 'earn_button_in_profile_menu'
    )

    dp.register_callback_query_handler(
        more_details_button_handler,
        lambda c: c.data == 'about_referal'
    )
