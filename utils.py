"""
Замечательный модуль для разгрузки основного файла приложения app.py
Сюда вынесены вспомогательные функции такие как:
Открытие конфига
Соединение с базой данных
Соединение с сервисом dadata.ru
и многое, многое другое
Your code has been rated at 10.00/10 (previous run: 9.68/10, +0.32)
"""
import configparser

import psycopg2
from dadata import Dadata

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini", encoding="utf-8")  # читаем конфиг


def get_address(address):
    """
    Взаимодействие с сервисом dadate.ru
    :param address: передаётся строка адреса введёного пользователем
    :return: Возвращается словарь с информацией о координатах точки,
    либо None, если не найдена таковая
    """
    with Dadata(config["dadata"]["api-token"], config["dadata"]["api-secret"]) as dadata:
        result = dadata.clean(name="address", source=address)
    if result['geo_lat'] is None:
        return None
    return {'geo_lat': result['geo_lat'],
            'geo_lon': result['geo_lon']}


def get_db_connection():
    """
    Подключение к базе данных
    :return: коннектор к базе
    """
    conn = psycopg2.connect(host=config["database"]["qhost"],
                            port=config["database"]["qport"],
                            user=config["database"]["quser"],
                            password=config["database"]["qpass"],
                            database=config["database"]["qbase"]
                            )
    return conn


def get_closes_points(lat, lon, radius):
    """
    Поиск точек в переданном радиусе к переданной координате
    """
    db_con = get_db_connection()
    cur = db_con.cursor()
    # Запрос на поиск близжайших точек
    sql = f"""SELECT geo_lat, geo_lon FROM addresses WHERE acos(
       sin(radians({lat}))
         * sin(radians(geo_lat))
       + cos(radians({lat}))
         * cos(radians(geo_lat))
         * cos( radians({lon})
           - radians(geo_lon))
       ) * 6371 <= {radius};"""
    cur.execute(sql)
    dots = cur.fetchall()
    result = list({"geo_lat": _[0], "geo_lon": _[1]} for _ in dots)
    return result


def get_zoom_level(radius, pixels=800):
    """
    Для удобства отображения поиск оптимального зум-левела для карты
    """
    # Зум мельче вряд ли пригодится, начнём с него
    start_zoom = {"zoom_level": 12, "m/pixel": 38.187}
    # если радиус не передан - возвращаем 11
    if radius:
        param = (int(radius) * 2 * 1000) / pixels
    else:
        return 11
    # если передан - ищем оптимальный
    while param > start_zoom["m/pixel"]:
        start_zoom["m/pixel"] *= 2
        start_zoom["zoom_level"] -= 1
    return start_zoom["zoom_level"]
