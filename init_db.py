import pandas as pd
import psycopg2
from psycopg2 import extras

import utils

# Соединяемся с базой данных
con = utils.get_db_connection()

# Открываем курсор
cur = con.cursor()

# Создаём новую таблицу (перед этим удляя, если была создана)
cur.execute('DROP TABLE IF EXISTS addresses;')
# Создаём поля в ней (по-сути, кроме lat и lon остальные поля не нужны, поэтому делаем их varchar)
cur.execute('CREATE TABLE addresses (id serial PRIMARY KEY,'
            'address varchar (100),'
            'postal_code varchar (50),'
            'country varchar (50),'
            'federal_district varchar (50),'
            'region_type varchar (50),'
            'region varchar (50),'
            'area_type varchar (50),'
            'area varchar (50),'
            'city_type varchar (50),'
            'city varchar (50),'
            'settlement_type varchar (50),'
            'settlement varchar (50),'
            'kladr_id varchar (50),'
            'fias_id varchar (50),'
            'fias_level varchar (50),'
            'capital_marker varchar (50),'
            'okato varchar (50),'
            'oktmo varchar (50),'
            'tax_office varchar (50),'  # geo_lat,geo_lon,population,foundation_year
            'timezone varchar (50),'
            'geo_lat decimal(9,6),'
            'geo_lon decimal(9,6),'
            'population varchar (50),'
            'foundation_year varchar (50));'
            )

con.commit()

cur.close()


def execute_values(conn, df, table):
    """
    Заполнение таблицы базы данных данными с датафрейма pandas
    """
    # Создаём список кортежей-значений для заполнения данных
    tuples = [tuple(x) for x in df.to_numpy()]
    # разделяем колонки
    cols = ','.join(list(df.columns))
    # SQL-запрос на заполнение таблицы
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"ошибка при заполнении таблицы: {error}")
        conn.rollback()
        cursor.close()
        return 1
    print("Вставка значений завершена!")
    cursor.close()


# Открываем csv-файл как датафрейм
dataframe = pd.read_csv('city.csv', delimiter=',')

# Исправляем неточности при переводе значений
dataframe['postal_code'] = dataframe['postal_code'].astype(str).str.replace('.0', '', regex=False)
dataframe['okato'] = dataframe['okato'].astype(str).str.replace('.0', '', regex=False)
dataframe['oktmo'] = dataframe['oktmo'].astype(str).str.replace('.0', '', regex=False)
dataframe['tax_office'] = dataframe['tax_office'].astype(str).str.replace('.0', '', regex=False)

# Заполняем таблицу
execute_values(con, dataframe, 'addresses')

con.close()
