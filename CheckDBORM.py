import os
import importlib
from typing import Union

import sqlalchemy as sq
from dotenv import load_dotenv
from psycopg2 import errors
from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from CheckBD.ABCCheckDb import ABCCheckDb
from table_structure import Genders, Cities, Users, Favorites, Exceptions, Criteries


class CheckDBSQL(ABCCheckDb):

    def get_engine(self, dbname:str, user:str, 
                    password:str, host:str='localhost', 
                    port:str='5432') -> sq.Engine:
        """
        Назначение:
        - создание движка sqlalchemy
        
        Выводной параметр:
        - движок sqlalchemy
        """

        # Построение DNS-ссылки и запуск движка
        dns_link = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        return create_engine(dns_link)


    def exists_db(self) -> bool:
        """
        Проверка, есть база данных или нет
        Returns:
            bool : True - есть база данных, False - нет базы данных
        """

        # Запуск движка
        engine = self.get_engine(
                            dbname=self.db_name, 
                            user = os.getenv(key='USER_NAME_DB'),
                            password=os.getenv(key='USER_PASSWORD_DB')
                            )
        
        # Учет отсутствия или наличия БД
        if not database_exists(engine.url):
            return False
        else:
            return True


    def create_db(self):
        """
        Создание базы данных
        """
        
        # Учет отсутствия БД
        if not self.exists_db():
            
            # Запуск движка
            engine = self.get_engine(
                                dbname=self.db_name, 
                                user = os.getenv(key='USER_NAME_DB'),
                                password=os.getenv(key='USER_PASSWORD_DB')
                                )
            
            # Создание БД
            create_database(engine.url)


    def exists_tables(self, name_table:str) -> bool:
        
        """
        Проверка, все ли нужные таблицы созданы
        Returns:
            bool : True - если созданы, False - нет
        """
        
        # Запуск движка
        engine = self.get_engine(
                            dbname=self.db_name, 
                            user=os.getenv(key='USER_NAME_DB'),
                            password=os.getenv(key='USER_PASSWORD_DB')
                            )
        
        # Учет наличия/отсутствия таблицы name_table
        if not sq.inspect(engine).has_table(name_table):            
            return False
        else:
            return True


    def form_classes(self) -> list:
        
        """
        Выводится список объектов класса
        """
        
        # Список объектов класса
        return [Genders, Cities, Users, 
                Favorites, Exceptions, Criteries]
    
    
    def form_module(self) -> str:

        """
        Выводится название модуля, котором
        содержатся объекты класса, отвечающие
        за таблицы в ORM
        """

        # Название модуля, откуда берутся ORM классы
        return "table_structure"


    def create_tables(self):
        
        """"
        name_table - имя таблицы
        
        Returns:
        None - отсутствие результата
        data_list - пустая/заполненная таблица
        """

        # Запуск движка
        engine = self.get_engine(
                            dbname=self.db_name, 
                            user=os.getenv(key='USER_NAME_DB'),
                            password=os.getenv(key='USER_PASSWORD_DB')
                            )
        
        # Выведение названия модуля
        name_module = self.form_module()
        
        # Учето таблиц и объектов классов
        for name_table, my_class in zip(self.tables, 
                                        self.form_classes()):
            
            # Учет наличия названия таблицы в объекте класса my_class
            if name_table == my_class.__tablename__:
                
                # Импортирование модуля
                table_models = importlib.import_module(name_module)
                
                # Формирование таблицы по данным объекта класса
                orm_table = getattr(
                                    table_models, 
                                    my_class.__name__
                                )
                orm_table.__table__.create(
                                            bind=engine, 
                                            checkfirst=True
                                        )

        # Учет некорректно введенных данных
        for table in self.tables:
            if not self.exists_tables(table):
                print(f'Таблица {table} не сформирована в ORM классах')


    def get_tables(self, name_table:str) -> Union[list, None]:
        
        """"
        Позволяет вывести таблицу
        
        name_table - имя таблицы
        
        Returns:
        None - отсутствие результата
        data_list - пустой/заполненный список словарей
        """

        # Запуск движка
        engine = self.get_engine(
                            dbname=self.db_name, 
                            user=os.getenv(key='USER_NAME_DB'),
                            password=os.getenv(key='USER_PASSWORD_DB')
                        )
        
        # Запуск сессии
        session_class = sessionmaker(bind=engine)
        session = session_class()
        
        # Учет имен таблиц внутри всех классов
        for my_class in self.form_classes():
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
    
    
    def fill_tables(self, name_table:str, data:list, autoincriment_bool:bool) -> None:
        
        """
        
        Позволяет заполнить таблицу
        
        name_table - название таблицы
        data - данные (заполняется в формате листа листов)
        
        autoincriment_bool = True (автоматическое заполнение ID). ЗАПОЛНЯЕТСЯ N-1 СТОЛБЦОВ (БЕЗ ID)
        data = [['Москва'], ['Питер'], ['Екатеринбург'], ['Сочи'], ['Адлер'], ['Мухосранск']]
        
        autoincriment_bool = False (ручное заполение ID). ЗАПОЛНЯЕТСЯ N СТОЛБЦОВ (ВМЕСТЕ С ID)
        data = [[2945, 'Москва'], [4424, 'Питер'], [4234, 'Екатеринбург']]
        """
        
        # Запуск функции получения таблицы
        data_table = self.get_tables(name_table)

        # Если таблица заведена в БД
        if data_table is not None:

            # Проверка наличия названия таблицы в разрезе классов 
            for my_class in self.form_classes():
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
                        engine = self.get_engine(
                                            dbname=self.db_name, 
                                            user=os.getenv(key='USER_NAME_DB'),
                                            password=os.getenv(key='USER_PASSWORD_DB')
                                        )
                        
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
    
    def delete_table_values(self, name_table:str, 
                            col_name:str, col_value:any) -> None:
        
        """
        Назначение:
        - удаление строк таблиц, находящихся в БД
        
        Вводные параметры:
        - name_table: название таблицы
        - col_name: название столбца в виде строки
        - col_value: значение столбца 
        """

        # Проверка наличия названия таблицы в разрезе классов 
        for my_class in self.form_classes():
            if name_table == my_class.__tablename__:
                
                # Запуск движка
                engine = self.get_engine(
                                        dbname='database_test', 
                                        user = 'postgres',
                                        password='postgres'
                                    )
                
                # Инициация сессии
                session_class = sessionmaker(bind=engine)
                session = session_class()

                try:
                    # Формирование запроса
                    delete_query = session.\
                                query(my_class).\
                                where(getattr(my_class, col_name)==col_value).\
                                one()
                    
                    # Удаление данных
                    session.delete(delete_query)
                    
                    # Завершение сессии
                    session.commit()
                    session.close()

                # Учет ошибок
                except exc.NoResultFound:
                    print('NoResultFound: результат по запросу не найден')
