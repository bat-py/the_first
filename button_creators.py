from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sql_handler
import json

with open('bot_messages.json', 'r', encoding='utf-8') as json_mesg:
    bot_mesg = json.load(json_mesg)


# Creates InlineKeyboardMarkup
def inline_keyboard_creator(buttons_list, row_width=2):
    """
    :param row_width: Columns count
    :param buttons_list: You should give lists. Every list is one button. List's structure: [button_text, callback_data]
    :return: Ready InlineKeyboardMarkup
    """

    ready_buttons = InlineKeyboardMarkup(row_width=row_width)

    for i in buttons_list:
        if i[1].startswith('https://'):
            button = InlineKeyboardButton(i[0], url=i[1])
            ready_buttons.add(button)
        else:
            button = InlineKeyboardButton(i[0], callback_data=i[1])
            ready_buttons.add(button)

    return ready_buttons


# Creates ReplyKeyboardCreator
def reply_keyboard_creator(buttons_list):
    """
    :param buttons_list: Передаешь массивы, каждый массив это одна строка, в внутри массива будет еще массавы которые каждый
    :return:
    """

    ready_buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in buttons_list:
        row = [KeyboardButton(j) for j in i]
        ready_buttons.row(*row)

    return ready_buttons


def main_menu_buttons(chat_id):
    feedback_count = sql_handler.get_feedback_count()

    user_city = sql_handler.get_user_city(chat_id)
    # Если он еще не выбрал город из welcome сообщении
    if not user_city:
        product = 'Товары'
    else:
        product = f'Товары ({user_city["city"]})'

    buttons = [
        ['Локации', product, 'Профиль'],
        ['Баланс', f'Отзывы ({feedback_count})', 'Поддержка'],
        ['Заработать']
    ]
    ready_buttons = reply_keyboard_creator(buttons)

    return ready_buttons
