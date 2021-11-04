import pymysql
from pymysql.cursors import DictCursor
import random


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


def get_bot_api():
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT data FROM additional_data WHERE data_name = 'bot_api_token'")
    api_bot = cursor.fetchone()

    connection.close()
    return api_bot['data']


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


def get_feedback_count():
    """
    :return: feedback count in str: '5246'
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT data FROM additional_data WHERE data_name = 'feedbacks_count'")

    feedbacks_count = cursor.fetchone()
    connection.close()

    if feedbacks_count:
        return feedbacks_count['data']
    else:
        return '4691'


def update_feedback_count(feedback_count):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("UPDATE additional_data SET data = %s WHERE data_name = 'feedbacks_count';", (feedback_count,))
    connection.commit()
    connection.close()


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
    WHERE city = %s AND product = %s AND rayon = %s AND massa = %s AND status = 1;
    """,
                   (city_id, product_id, rayon_id, masssa_id)
                   )

    aviable_klads = cursor.fetchall()

    connection.close()
    return aviable_klads


def get_referal_code(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT referal FROM users WHERE id = %s;", (chat_id,))
    referal = cursor.fetchone()

    connection.close()
    return referal


def get_aviable_payments_methods():
    """
    :return:  [{id, status, method_name, my_wallet}, {}, ...]
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM payment_methods WHERE status = 1;")
    methods_list = cursor.fetchall()

    connection.close()
    return methods_list


def randomly_get_wallet_address(payment_method_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT my_wallet FROM payment_methods WHERE id = %s AND status = 1;", (payment_method_id,))
    # Получаем {'my_wallet': '998984561875,7741369875'}
    my_wallet = cursor.fetchone()

    my_wallets = my_wallet['my_wallet'].split(',')
    random_chosen_wallet = random.choice(my_wallets)

    connection.close()
    return random_chosen_wallet


def order_adder(chat_id, order_number, type):
    """
    В type можно указать либо "refill" либо "product_order".
    Если refill тогда при /cancel пользователю отправим "Отмена пополнения..."
    Если product_order тогда при /cancel пользователю отправим "Отмена заказа..."
    :param chat_id:
    :param order_number:
    :param type:
    :return:
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO active_orders(chat_id, order_number, date_time, type)
                   VALUES(%s, %s, NOW(), %s);
                   """,
                   (chat_id, order_number, type)
                   )

    connection.commit()
    connection.close()


def check_member_order_exist(chat_id):
    """
    :param chat_id:
    :return: Либо вернет {'order_number'} если за последный час пользователь создал заявку на пололнение или на покупку
    либо вернет None если за последный час не создал
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM active_orders WHERE date_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR) AND
    chat_id = %s ORDER BY id DESC;
    """,
                   (chat_id,)
                   )
    order_number = cursor.fetchone()

    connection.close()
    return order_number


def del_member_orders(chat_id):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM active_orders WHERE chat_id = %s", (chat_id,))
    connection.commit()

    connection.close()


def product_price(city_id, product_id, rayon_id, massa_id, klad_type_id):
    """
    :param city_id:
    :param product_id:
    :param rayon_id:
    :param massa_id:
    :param klad_type_id:
    :return: Вернет {'price'}
    """

    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT price FROM products
    WHERE city = %s AND product = %s AND rayon = %s AND massa = %s AND klad_type = %s AND status = 1;
    """,
                   (city_id, product_id, rayon_id, massa_id, klad_type_id))
    price = cursor.fetchone()

    connection.close()
    return price


def get_columns_name_by_id(city_id, product_id, rayon_id, massa_id, klad_type_id):
    """
    :param city_id:
    :param rayon_id:
    :param product_id:
    :param massa_id:
    :param klad_type_id:
    :return: Получает id, возврашает имя этих столбцов:
    {'city': 'Уфа', 'product': 'Шишки', 'rayon': 'Юматово', 'massa': '2.00gr', 'klad_type': 'Тайник'}
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT cities.city, products_types.type product, products_rayons.region rayon, products_massa.massa_gr massa, klad_types.type klad_type
    FROM products
    JOIN cities ON cities.id = products.city
    JOIN products_types ON products_types.id = products.product
    JOIN products_rayons ON products_rayons.id = products.rayon
    JOIN products_massa ON products_massa.id = products.massa
    JOIN klad_types ON klad_types.id = products.klad_type
    WHERE products.city = %s AND products.product = %s AND products.rayon = %s 
    AND products.massa = %s AND products.klad_type = %s
    """,
                   (city_id, product_id, rayon_id, massa_id, klad_type_id)
                   )

    columns_names = cursor.fetchone()

    connection.close()
    return columns_names


def get_column_name_payment_method(payment_method_id):
    """
    :param payment_method_id:
    :return: Возврашает имя метода оплаты (Лайткоин, Биткоин ...)
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT method_name FROM payment_methods WHERE id = %s", (payment_method_id,))
    method_name = cursor.fetchone()

    connection.close()
    return method_name


def get_password():
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT data FROM additional_data WHERE data_name = 'password'")
    password = cursor.fetchone()

    if password:
        return password['data']
    else:
        return 'batpy123'


def update_password(new_password):
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("UPDATE additional_data SET data = %s WHERE data_name = 'password';", (new_password,))
    connection.commit()
    connection.close()


def get_users_chat_id():
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users;")
    users_chat_id_dict = cursor.fetchall()
    users_chat_id = [i['id'] for i in users_chat_id_dict]

    connection.close()
    return users_chat_id


def get_feedbacks(list_number: int):
    """
    :param list_number:
    :return: 10 отзывов: [{'id': 10, 'rate': 10, 'order_date': datetime.date(2021, 10, 21)}, {'id'...}, ...]
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(id) FROM feedbacks")
    count = cursor.fetchone()['COUNT(id)']

    start = (list_number-1)*10
    finish = list_number*10

    if finish > count:
        cursor.execute("SELECT id, rate, order_date FROM feedbacks ORDER BY id DESC")
        feedbacks_list = cursor.fetchall()[-10:]
    else:
        cursor.execute("SELECT id, rate, order_date FROM feedbacks  ORDER BY id DESC")
        feedbacks_list = cursor.fetchall()[start:finish]

    connection.close()
    return feedbacks_list


def get_feedback_by_id(feedback_id):
    """
    :param feedback_id:
    :return: {'id': 1, 'order_date': datetime.date(2021, 10, 21), 'customer_name': '@hjikogfg', 'rate': 9, 'feedback_text': 'Отличный товар'}
    """
    connection = connection_creator()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (feedback_id, ))
    feedback_data = cursor.fetchone()

    connection.close()
    return feedback_data
