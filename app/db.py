import psycopg2
import psycopg2.extras
import config
import datetime


class Database:
    """
    Класс для взаимодействия с базой данных PostgreSQL.
    """
    def __init__(self):
        """
        Инициализация объекта класса Database.
        """
        self.connection = None


    def connect(self):
        """
        Установка соединения с базой данных.
        """
        try:
            "Конфиг должен выглядеть так CONFIG = {'host': 'localhost', 'user': 'обычно постгрс', 'password': 'пароль от пг', 'dbname': 'int_ssh', 'port': 5432}"
            self.connection = psycopg2.connect(**config.CONFIG)
        except psycopg2.DatabaseError as ex:
            print(ex)


    def close(self):
        """
        Закрытие соединения с базой данных.
        """
        if self.connection:
            self.connection.close()


    def get_data(self, query, values=None):
        """
        Выполнение SQL-запроса SELECT и возврат результата.
        """
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query, values)
            return cursor.fetchall()
        except psycopg2.DatabaseError as ex:
            print(ex)
        finally:
            self.close()


    def set_data(self, query, values=None):
        """
        Выполнение SQL-запроса INSERT/UPDATE и фиксация изменений в базе данных.
        """
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query, values)
            self.connection.commit()
            if "RETURNING id;" in query:
                return cursor.fetchone()[0]
        except psycopg2.DatabaseError as ex:
            print(ex)
        finally:
            self.close()
            
            
    def add_history(self, ip, os, version, build, architecture):
        """
        Добавление записи в таблицу истории сканирования.
        """
        time = datetime.datetime.now()
        return self.set_data('INSERT INTO history (ip, os, version, build, architecture, "time") VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;', (ip, os, version, build, architecture, time))


    def get_history(self):
        """
        Получение всех записей из таблицы истории сканирования.
        """
        return self.get_data('SELECT * FROM history;')

    
# def get_data(query, values=None):
#     """_summary_
#     ФУНКЦИЯ ДЛЯ  ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
#     Args:
#         query (_type_): _description_
#         values (_type_, optional): _description_. Defaults to None.

#     Returns:
#         _type_: _description_
#     """
#     try:
#         connection = psycopg2.connect(**config.CONFIG)
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute(query, values)
#         return cursor.fetchall()
#     except psycopg2.DatabaseError as ex:
#         print(ex)
#     finally:
#         connection.close()


# def set_data(query, values=None):
#     """_summary_
#     ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ И ОБНОВЛЕНИЯ ЗАПИСЕЙ В БД
#     Args:
#         query (_type_): _description_
#         values (_type_, optional): _description_. Defaults to None.

#     Returns:
#         _type_: _description_
#     """
#     try:
#         connection = psycopg2.connect(**config.CONFIG)
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute(query, values)
#         connection.commit()
#         if "RETURNING id;" in query:
#             return cursor.fetchone()[0]
#     except psycopg2.DatabaseError as ex:
#         print(ex)
#     finally:
#         connection.close()

