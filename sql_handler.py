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

    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()

    connection.close()
    return cities


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


def get_balance(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = %s",
                   (chat_id,)
                   )
    balance = cursor.fetchone()

    connection.close()
    return balance['balance']


####
def get_feedback_count():
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("")


# После этой записи кнопка Товары изменится на "Товары (Имя города)"
# Если нажимаешь на кнопку "Товары (Имя города)" тогда бот сразу предложит выбрать товар
# Если столбец users.city пустой тогда бот предложит выбрать сперва город
def update_user_city(chat_id, city_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET city = %s WHERE id = %s;",
                   (city_id, chat_id)
                   )
    connection.commit()

    connection.close()


def get_user_city(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT cities.city FROM users JOIN cities ON users.city = cities.id WHERE users.id = %s",
                   (chat_id,)
                   )
    user_city = cursor.fetchone()

    connection.close()
    return user_city


def update_chosen_city(chat_id, city_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET chosen_city = %s WHERE id = %s;",
                   (city_id, chat_id)
                   )
    connection.commit()

    connection.close()


def get_chosen_city_id(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT chosen_city FROM users WHERE id = %s;",
                   (chat_id,)
                   )
    user_city = cursor.fetchone()

    connection.close()
    return user_city


def get_products_from_city(city_id):
    """
    :param city_id:
    :return: [{'id': 10, 'type': 'АЛЬФА (ПВП) КРИСТАЛЛ'}, {'id': 50, 'type': 'Мефедрон Мука'}]
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
                    SELECT products.product id, products_types.type FROM products
                    JOIN products_types ON products.product = products_types.id
                    WHERE city = %s;""",
                   (city_id, )
                   )

    products_in_city = cursor.fetchall()

    connection.close()
    return products_in_city


get_products_from_city(30)
