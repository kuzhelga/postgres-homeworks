"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2
from config import user, password


def read_csv(path):
    """Функция читает данные из scv файла и возвращает список"""
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        data = []
        for line in reader:
            data.append(line)

    return data


def main():

    try:
        # connection to existed database
        conn = psycopg2.connect(host='localhost', database='north', user=user, password=password)
        conn.autocommit = True

        # cursor for operating with database
        with conn.cursor() as cur:

            # добавление данных в таблицы
            customers_reader = read_csv('north_data/customers_data.csv')
            for row in customers_reader[1:]:
                cur.execute('INSERT INTO customers VALUES (%s, %s, %s)', (row[0], row[1], row[2]))
                cur.execute('SELECT * FROM customers')

            employees_reader = read_csv('north_data/employees_data.csv')
            for row in employees_reader[1:]:
                cur.execute(
                    'INSERT INTO employees (first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s)',
                    (row[0], row[1], row[2], row[3], row[4])
                )

            orders_reader = read_csv('north_data/orders_data.csv')
            for row in orders_reader[1:]:
                cur.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)', (row[0], row[1], row[2], row[3], row[4]))
                cur.execute('SELECT * FROM employees')

            print("Data was successfully added to table")

    except Exception as _ex:
        print("Ошибка подключения к PostgreSQL", _ex)
    else:
        if conn:
            conn.close()
            print('PostgreSQL connection closed')


if __name__ == "__main__":
    main()
