import pymysql
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '1752613191:AAGvWm7IbiHNy8VZWqyZsekxo-ebARgRErE'
API_TOKEN = '1559565040:AAG97C16gpMUk4cZgElzGspPb8uplSCX0Ss'
# Настроить ведение журнала
logging.basicConfig(level=logging.INFO)
# Инициализировать бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot)

# Создает mysql соединение и возврашает его
def connection_creator():
    connection = pymysql.connect(
        host='185.204.2.89',
        port=3306,
        user='hik',
        password='sherxan@123#',
        database='telegram',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# Запустится если пользователь отправил /start
@dp.message_handler(commands="start")
async def cities_menu(message: types.Message):
    main_menu_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_buttons.add(
        types.KeyboardButton('Datasheets'),
        types.KeyboardButton('Firmware')
    )

    mesg = "Добро пожаловать :)"
    await message.answer(mesg, reply_markup=main_menu_buttons)


# Запустится если пользователь нажал на Datasheet
@dp.message_handler(lambda message: message.text == 'Datasheets')
async def datasheets_menu(message: types.Message):
    # Получаем список всех datasheet в виде [{Model, file_id}, {}, ...]
    with connection_creator().cursor() as cursor:
        cursor.execute("SELECT Model FROM datasheet")
        datasheets_dict = cursor.fetchall()
        # Переобразуем datasheets_dict в list:
        datasheets_list = [i['Model'] for i in datasheets_dict]

    inline_buttons = types.InlineKeyboardMarkup(row_width=2)
    for datasheet in datasheets_list:
        inline_buttons.add(InlineKeyboardButton(datasheet, callback_data='x'+datasheet))
# callback_data='datasheet_dISDIASL'
    mesg = "Список даташитов:"

    await message.answer(mesg, reply_markup=inline_buttons)


@dp.callback_query_handler(lambda c: c.data.startswith('datasheet_name'))
async def datasheets_inline_buttons_handler(callback_query: types.CallbackQuery):
    with connection_creator().cursor() as cursor:
        model = callback_query.data.replace('datasheet_name', '')
        cursor.execute("SELECT file_id FROM datasheet WHERE Model = %s", (model, ))
        file_id = cursor.fetchone()['file_id']

    print(file_id)
    await callback_query.bot.send_document(
        chat_id=callback_query.from_user.id,
        document=file_id
    )


# Запустится если пользователь нажал на Firmware
@dp.message_handler(lambda message: message.text == 'Firmware')
async def firmware_menu(message: types.Message):
    # Получаем список всех firmware в виде [{Model, file_id}, {}, ...]
    with connection_creator().cursor() as cursor:
        cursor.execute("SELECT Model FROM firmware")
        firmware_dict = cursor.fetchall()
        # Переобразуем datasheets_dict в list:
        firmware_list = [i['Model'] for i in firmware_dict]

    inline_buttons = types.InlineKeyboardMarkup(row_width=2)
    for firmware in firmware_list:
        inline_buttons.add(InlineKeyboardButton(firmware, callback_data='firmware_name'+firmware))

    mesg = "Список фреймворков:"

    await message.answer(mesg, reply_markup=inline_buttons)


@dp.callback_query_handler(lambda c: c.data.startswith('firmware_name'))
async def firmware_inline_buttons_handler(callback_query: types.CallbackQuery):
    with connection_creator().cursor() as cursor:
        model = callback_query.data.replace('firmware_name', '')
        cursor.execute("SELECT file_id FROM firmware WHERE Model = %s", (model, ))
        file_id = cursor.fetchone()['file_id']

    print(file_id)
    await callback_query.bot.send_document(
        chat_id=callback_query.from_user.id,
        document='BQACAgIAAxkBAAIDGGF3FLnzQaxQp_1VtmwiR8gefsNfAAJAEwAC9_y4S1plkoLOaoO4IQQ'
    )


# Если бот получит документ от пользователя, тогда вернет мета-данные пользователю обратно
@dp.message_handler(content_types=['document'])
async def return_message(message: types.Message):
    await message.answer(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

