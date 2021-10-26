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
    """
    :param chat_id:
    :return: Returns None or {'city': 'Уфа', 'city_id': 30}
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT cities.city, users.city city_id FROM users JOIN cities ON users.city = cities.id WHERE users.id = %s",
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
                    WHERE city = %s and status = 1;""",
                   (city_id,)
                   )

    products_in_city = cursor.fetchall()

    connection.close()
    return products_in_city


def get_product_info(product_id):
    """
    :param product_id:
    :return: { 'id':'', 'type':'', 'photo_name':'', 'about':'' }
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products_types WHERE id = %s;", (product_id,))
    product_info = cursor.fetchone()

    connection.close()
    return product_info


def get_city_name(city_id):
    """
    :param city_id:
    :return: {'city': 'Уфа'}
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT city FROM cities WHERE id = %s;",
                   (city_id,)
                   )
    city_name = cursor.fetchone()

    connection.close()
    return city_name


def get_one_product_type_in_city(city_id, product_id):
    """
    Например пользователь выбрал город Уфа, товар альфа-пвп. Функция возврашает все альфа-пвп товары в городе Уфа
    :param city_id:
    :param product_id:
    :return: [{'city_id': 10, 'city': 'Уфа', 'product_id': 40, 'product': 'Шишки Amnesia Feminised',
               'rayon_id': 5, 'rayon': 'Юматово', 'massa_id': 40, 'massa': '2.00gr'}, ...]
    """

    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT products.city city_id, cities.city city, products.product product_id, products_types.type product,
    products.rayon rayon_id, products_rayons.region rayon, products.massa massa_id, products_massa.massa_gr massa
    FROM products
    JOIN cities ON products.city = cities.id
    JOIN products_types ON products.product = products_types.id
    JOIN products_rayons ON products.rayon = products_rayons.id
    JOIN products_massa ON products.massa = products_massa.id
    WHERE products.city = %s and products.product = %s and status = 1;
    """,
                   (city_id, product_id)
                   )

    products = cursor.fetchall()

    connection.close()
    return products


def get_product_name_by_id(product_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT type product_name FROM products_types WHERE id = %s", (product_id,))
    product_name = cursor.fetchone()

    connection.close()
    return product_name


def get_rayon_name_by_id(rayon_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT region rayon_name FROM products_rayons WHERE id = %s", (rayon_id,))
    rayon_name = cursor.fetchone()

    connection.close()
    return rayon_name


def get_product_massas_price_in_chosen_rayon(city_id, product_id, rayon_id):
    """
    :param city_id:
    :param product_id:
    :param rayon_id:
    :return: list with dicts elements: [{'massa_id', 'massa', 'price'}, {...}]
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT massa massa_id, massa_gr massa, price
    FROM products
    JOIN products_massa ON products.massa = products_massa.id
    WHERE city = %s and product = %s and rayon = %s;
    """,
                   (city_id, product_id, rayon_id)
                   )
    massa_price_list = cursor.fetchall()

    connection.close()
    return massa_price_list


def get_aviable_klads_type(city_id, product_id, rayon_id, masssa_id):
    """
    :param city_id:
    :param product_id:
    :param rayon_id:
    :param masssa_id:
    :return: dicts' list like: [{klad_id, klad_name}, {}, ...]
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT products.klad_type klad_id, klad_types.type klad_name 
    FROM products 
    JOIN klad_types ON klad_type = klad_types.id
    WHERE city = %s AND product = %s AND rayon = %s AND massa = %s;
    """,
                   (city_id, product_id, rayon_id, masssa_id)
                   )

    aviable_klads = cursor.fetchall()

    connection.close()
    return aviable_klads


def get_referal_code(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT referal FROM users WHERE id = %s;", (chat_id, ))
    referal = cursor.fetchone()

    connection.close()
    return referal