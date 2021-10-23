import pymysql
from pymysql.cursors import DictCursor


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


def feedback_count():
    con = connection_creator()
    cursor = con.cursor()

    cursor.execute("")