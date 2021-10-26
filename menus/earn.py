from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button_creators import *


async def earn_menu(message: types.Message):
    """
    Запускается если пользователь нажал на кнопку "Заработать"
    :param message:
    :return: Сперва отправит сообщение "Ваш код реферала: SSYLP8T",
    потом "Вы можете заработать приглашая покупателей." c inline кнопкой "Подробнее"
    """
    referal_code = sql_handler.get_referal_code(message.chat.id)['referal']
    your_referal_code_mesg = bot_mesg['your_referal_code'].replace('xxx', referal_code)
    # Отправляем 1-сообщение: Ваш код реферала: ....
    await message.answer(your_referal_code_mesg)

    # Создадим кнопку Подробнее и отправим с сообщением "Вы можете заработать приглашая покупателей...."
    more_details_button = inline_keyboard_creator([['Подробнее', 'about_referal']])
    await message.answer(
        bot_mesg['about_referal_system'],
        reply_markup=more_details_button
    )


def register_handlers_products(dp: Dispatcher):
    """
    Регистрируем все наши обработчики(handlers) который связано с кнопкой "Заработать"
    :param dp:
    :return:
    """

    dp.register_message_handler(
        earn_menu,
        lambda message: message.text == 'Заработать'
    )
