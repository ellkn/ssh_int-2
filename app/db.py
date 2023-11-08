import psycopg2
import psycopg2.extras
import config


def get_data(query, values=None):
    """_summary_
    ФУНКЦИЯ ДЛЯ  ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
    Args:
        query (_type_): _description_
        values (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    try:
        connection = psycopg2.connect(**config.CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, values)
        return cursor.fetchall()
    except psycopg2.DatabaseError as ex:
        print(ex)
    finally:
        connection.close()


def set_data(query, values=None):
    """_summary_
    ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ И ОБНОВЛЕНИЯ ЗАПИСЕЙ В БД
    Args:
        query (_type_): _description_
        values (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    try:
        connection = psycopg2.connect(**config.CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, values)
        connection.commit()
        if "RETURNING id;" in query:
            return cursor.fetchone()[0]
    except psycopg2.DatabaseError as ex:
        print(ex)
    finally:
        connection.close()
