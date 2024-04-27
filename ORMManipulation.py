import os
import inspect
from typing import Union

from psycopg2 import errors
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

import ORMTableStructure

def get_tables(engine, name_table: str) -> Union[list, None]:

    """"
    Позволяет вывести таблицу

    name_table - имя таблицы

    Returns:
    None - отсутствие результата
    data_list - пустой/заполненный список словарей
    """

    class_list = []
    for name, obj in inspect.getmembers(ORMTableStructure):
        if inspect.isclass(obj):
            if name != 'Base':
                class_list.append(obj)


    # Запуск сессии
    session_class = sessionmaker(bind=engine)
    session = session_class()

    # Учет имен таблиц внутри всех классов
    for my_class in class_list:
        if name_table == my_class.__tablename__:

            try:
                # Фиксация запроса
                query = session.query(my_class).all()

                # Заполнение столбцов
                table_columns = []
                for col_attr in my_class.__table__.columns:
                    table_columns.append(col_attr.key)

                # Заполнение данных таблиц в разрезе всех столбцов
                data_list = []
                for class_object in query:
                    data_dict = {}
                    for column in table_columns:
                        column_value = getattr(class_object, column)
                        data_dict[column] = column_value
                    data_list.append(data_dict)
                return data_list

            # Учет наличия ошибок
            except (errors.UndefinedTable,
                    exc.ProgrammingError):
                return None

    return None

# Добавить запись в genders
# dev chechorm
# универсальный метод (заполняет одну таблицу)

def fill_tables(engine, name_table, data, autoincriment_bool) -> None:

    """
    Позволяет заполнить таблицу

    name_table - название таблицы
    data - данные (заполняется в формате листа листов)

    autoincriment_bool = True (автоматическое заполнение ID). ЗАПОЛНЯЕТСЯ N-1 СТОЛБЦОВ (БЕЗ ID)
    data = [['Москва'], ['Питер'], ['Екатеринбург'], ['Сочи'], ['Адлер'], ['Мухосранск']]

    autoincriment_bool = False (ручное заполение ID). ЗАПОЛНЯЕТСЯ N СТОЛБЦОВ (ВМЕСТЕ С ID)
    data = [[2945, 'Москва'], [4424, 'Питер'], [4234, 'Екатеринбург']]
    """

    class_list = []
    for name, obj in inspect.getmembers(ORMTableStructure):
        if inspect.isclass(obj):
            if name != 'Base':
                class_list.append(obj)

    # Запуск функции получения таблицы
    data_table = get_tables(engine, name_table)

    # Если таблица заведена в БД
    if data_table is not None:

        # Проверка наличия названия таблицы в разрезе классов
        for my_class in class_list:
            if name_table == my_class.__tablename__:

                # Заполнение всех названий таблицы в рамках класса my_class
                table_columns = []
                for col_attr in my_class.__table__.columns:
                    table_columns.append(col_attr.key)

                # Вывод обработанных данных
                processed_data = []
                for row in data:

                    # Подстановка числа в зависимости от наличия autoincriment
                    # (переменная begin_int отражает стоит ли учитывать id вручную)
                    if autoincriment_bool:
                        begin_int = 1
                    else:
                        begin_int = 0

                    # Проверка на ввод нужного количества значаний столбцов
                    if len(row) == len(table_columns) - begin_int:

                        # Заполнение данных таблицы в формате словаря
                        data_dict = {}
                        for col_value, col_name in zip(row, table_columns[begin_int:]):
                            data_dict[col_name] = col_value

                        # Заполнения списка processed_data
                        processed_data.append(data_dict)

                # Запуска движка в случае наличия обработанных данных
                if processed_data:

                    # Учет id в зависимости от наличия autoincriment
                    if autoincriment_bool:
                        if len(data_table) == 0:
                            new_id = 1
                        else:
                            new_id = data_table[-1].get('id') + 1

                    # Работа со словарями из обработанных данных
                    for data_dict in processed_data:

                        # Обновление id в зависимости от наличия autoincriment
                        if autoincriment_bool:
                            data_dict.update({'id': new_id})

                        try:
                            # Инициация сессии
                            session_class = sessionmaker(bind=engine)
                            session = session_class()

                            # Заполнение таблицы
                            model = my_class(**data_dict)
                            session.add(model)

                            # Завершение сессии
                            session.commit()
                            session.close()

                            # Обновление id в зависимости от наличия autoincriment
                            if autoincriment_bool:
                                new_id += 1

                        # Учет ошибок
                        except (exc.IntegrityError,
                                errors.UniqueViolation,
                                exc.DataError,
                                errors.InvalidTextRepresentation,
                                errors.UndefinedTable,
                                exc.ProgrammingError,
                                exc.PendingRollbackError) as e:
                            print(e)
                            continue

    return get_tables(engine, name_table)

def delete_table_values(engine, name_table, col_name, col_value):

    """
    Назначение:
    - удаление строк таблиц, находящихся в БД

    Вводные параметры:
    - name_table: название таблицы
    - col_name: название столбца в виде строки
    - col_value: значение столбца
    """

    class_list = []
    for name, obj in inspect.getmembers(ORMTableStructure):
        if inspect.isclass(obj):
            if name != 'Base':
                class_list.append(obj)

    # Проверка наличия названия таблицы в разрезе классов
    for my_class in class_list:
        if name_table == my_class.__tablename__:

            # Инициация сессии
            session_class = sessionmaker(bind=engine)
            session = session_class()

            try:
                # Формирование запроса
                delete_query = session. \
                    query(my_class). \
                    where(getattr(my_class, col_name) == col_value). \
                    one()

                # Удаление данных
                session.delete(delete_query)

                # Завершение сессии
                session.commit()
                session.close()

            # Учет ошибок
            except exc.NoResultFound:
                print('NoResultFound: результат по запросу не найден')

def fill_genders():
    fill_tables(engine, name_table='genders',
                data=[['Женщина'], ['Мужчина']],
                autoincriment_bool=True)

def fill_city():
    fill_tables(engine, name_table='cities',
                data=[['Москва']],
                autoincriment_bool=True)


    # data = [[394923, 'Иван', 'Иванов', 28, 2, 1, 'Привет это я']]
    #
    # fill_tables(engine, name_table='users',
    #             data=data,
    #             autoincriment_bool=False)




if __name__ == '__main__':

    from sqlalchemy import create_engine

    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    dbname = 'new_database2'

    dns_link = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(dns_link)

    fill_genders()
    fill_city()

    data = [['Татьяна', 'Малахова', 394333, 30, 1, 'sexyTanya',
             'photo1', 'photo2', 'photo3', 1]]

    fill_tables(engine, name_table='favorites',
                data=data,
                autoincriment_bool=True)

# psycopg2.errors.ForeignKeyViolation