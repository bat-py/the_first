import pymysql
from pymysql.cursors import DictCursor
import random


def connection_creator():
    connect = pymysql.connect(
        host='archlinux.uz',
        user='crow',
        password='ifuckyou',
        db='the_first',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    return connect


def get_cities_list():
    """
    :return: List with dicts like:  [ {'id': 10, 'city': 'Уфа'}, {'id': 20, 'city': 'Челябинск'}, ... ]
    """

    con = connection_creator()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()

    return cities


def check_user_exists(chat_id):
    con = connection_creator()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (chat_id, ))
    responce = cursor.fetchone()

    return responce


def add_user(chat_id, first_name):
    upper_letters_numbers_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
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


def get_balance(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = %s",
                   (chat_id, )
                   )
    balance = cursor.fetchone()

    return balance['balance']


####
def get_feedback_count():
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("")


def get_user_city(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT cities.city FROM users JOIN cities ON users.city = cities.id WHERE users.id = %s",
                   (chat_id, )
                   )
    user_city = cursor.fetchone()

    return user_city


def change_user_city(chat_id):
    pass


