from pyrogram import Client, filters
import pymysql
from pymysql.cursors import DictCursor
import random

app = Client("my_account")

# SQL handlers
def connection_creator():
    connect = pymysql.connect(
        host='localhost',
        user='futurist',
        password='futurist',
        db='the_first',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    return connect
def get_bot_username():
    connection = connection_creator()

    cursor = connection.cursor()

    cursor.execute("SELECT data FROM additional_data WHERE data_name = 'bot_user_name'")
    api_bot = cursor.fetchone()

    connection.close()
    return api_bot['data']
def check_user_exists(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (chat_id,))
    responce = cursor.fetchone()

    connection.close()
    return responce
def add_user(chat_id, first_name):
    upper_letters_numbers_list = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    upper_letters_numbers_list.extend([str(i) for i in range(10)])
    referal = ''
    for i in range(7):
        referal += random.choice(upper_letters_numbers_list)

    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users(id, first_name, referal, balance) VALUES(%s, %s, %s, %s)",
                   (chat_id, first_name, referal, 0)
                   )
    connection.commit()
    connection.close()


@app.on_message()
async def hello(client, message):
    if not check_user_exists(message.chat.id):
        add_user(message.from_user.id, message.from_user.first_name)

    bot_username = get_bot_username()
    mesg = f'Приветcтвуем! Ваш индивидуальный бот для покупок {bot_username} <== ЖМИТЕ СЮДА.\nЕсли вашего бота заблокируют, просто снова напишите сюда для получения нового!'

    await message.reply_text(mesg)

app.run()
