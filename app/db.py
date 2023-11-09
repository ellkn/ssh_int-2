import psycopg2
import psycopg2.extras
import config
import datetime


class Database:
    
    def __init__(self):
        self.connection = None


    def connect(self):
        try:
            self.connection = psycopg2.connect(**config.CONFIG)
        except psycopg2.DatabaseError as ex:
            print(ex)


    def close(self):
        if self.connection:
            self.connection.close()


    def get_data(self, query, values=None):
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
        time = datetime.datetime.now()
        return self.set_data('INSERT INTO history (ip, os, version, build, architecture, "time") VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;', (ip, os, version, build, architecture, time))


    def get_history(self):
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

