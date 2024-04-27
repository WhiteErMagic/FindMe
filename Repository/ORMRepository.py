import os

from sqlalchemy import create_engine

from User import User
from CheckDB.CheckDBORM import
from Repository.ABCRepository import ABCRepository
from ORMManipulation import get_tables, fill_tables, delete_table_values

class ORMRepository(ABCRepository):

    def get_engine(self):

        """
        Формирует движок Sqlalchemy

        Вводные параметры:
        - dbname: наименование БД
        - user: имя пользователя Postgres
        - password: пароль пользователя Postgres
        - host: хост
        - port: порт

        Выводной параметр:
        - движок Sqlalchemy
        """

        dbname = 'findme'
        user = os.getenv(key='USER_NAME_DB')
        password = os.getenv(key='USER_PASSWORD_DB')
        host = 'localhost'
        port = '5432'

        dns_link = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        return create_engine(dns_link)

    # иначе psycopg2.errors.ForeignKeyViolation
    # def add_genders(self):
    #
    #     engine = self.get_engine()
    #
    #     fill_tables(engine, name_table='genders',
    #                 data=[['Женщина'], ['Мужчина']],
    #                 autoincriment_bool=True)
    #
    # # Иначе psycopg2.errors.ForeignKeyViolation11
    # def add_cities(self):
    #
    #     engine = self.get_engine()
    #
    #     fill_tables(engine, name_table='cities',
    #                 data=[[self.add_cities('My city')]],
    #                 autoincriment_bool=True)


    # Добавить пользователя в таблицу users
    # Вытащить данные из класса User (словарь) == таблица (не name_table='users')
    def add_user(self, dict_user):

        # self.add_genders()
        # self.add_cities()

        engine = self.get_engine()

        class_obj = user({''})

        vk_id = class_obj.set_vk_id()
        first_name = class_obj.first_name()
        last_name = class_obj.last_name()
        age = class_obj.age()
        gender = class_obj.gender()
        city = class_obj.city()
        about_name = class_obj.about_name()

        data = [[vk_id, first_name, last_name, age, gender, city, about_name]]
        fill_tables(engine, name_table='users',
                    data=data,
                    autoincriment_bool=False)

    # Cловарь [{''}]
    # Добавление избранной второй половинки
    # user_id == user_vk (int): VK-идентификатор пользователя
    # Favorites => словарь по руками
    def add_favorites(self, dict_user):

        self.fill_genders()
        self.fill_city()

        data = [['Татьяна', 'Малахова', user_vk, 30, 2, 'sexyTanya',
                 'photo1', 'photo2', 'photo3', 1]]

        engine = self.get_engine()

        fill_tables(engine, name_table='favorites',
                    data=data,
                    autoincriment_bool=True)

    # Добавление человека в черный список
    def add_exceptions(self, dict_user):

        self.fill_genders()
        self.fill_city()

        data = [['Марина', 'Захарова', user_vk, 50, 2, 'sexyTanya',
                 'photo1', 'photo2', 'photo3', 1]]

        engine = self.get_engine()

        fill_tables(engine, name_table='exceptions',
                    data=data,
                    autoincriment_bool=True)

    # Удаление человека из избранного
    # user_id == user_vk (int): идентификатор пользователя <=> VK-идентификатор пользователя
    # id, id фаворит
    def delete_favorites(self, dict_user):
        pass

    # Удаление человека из черного списка
    def delete_exceptions(self, dict_user):
        pass

    # Получение списка словарей по user_id
    # user_id == user_vk (int): идентификатор пользователя <=> VK-идентификатор пользователя
    def get_favorites(self, user_id):
        pass

    # Получение списка словарей для user_id
    def get_exceptions(self, user_id):
        pass