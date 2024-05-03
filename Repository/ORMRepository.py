import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from User import User
from Criteria import Criteria
from Repository.ABCRepository import ABCRepository
from Repository.CardFavorites import CardFavorites
from Repository.CardExceptions import CardExceptions
from CheckBD.ORMTableStructure import Cities, Users, Favorites, Exceptions, Criteries


class ORMRepository(ABCRepository):

    def get_engine(self) -> sqlalchemy.Engine:

        """
        Формирует движок Sqlalchemy

        Выводной параметр:
        - движок sqlalchemy
        """

        load_dotenv()

        dbname = 'findme'
        user = os.getenv(key='USER_NAME_DB')
        password = os.getenv(key='USER_PASSWORD_DB')
        host = 'localhost'
        port = '5432'

        # Создание DNS-ссылки и запуск движка
        dns_link = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        return create_engine(dns_link)


    def add_user(self, user: User):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_user = session.query(Users).\
            filter_by(id=user.get_user_id()).\
            first()

        if existing_user:
            existing_user.first_name = user.get_first_name()
            existing_user.last_name = user.get_last_name()
            existing_user.age = user.get_age()
            existing_user.gender_id = user.get_gender()
            existing_user.city_id = user.get_city()['id']
            existing_user.about_me = user.get_about_me()

        else:
            city = session.query(Cities).\
                filter_by(name=user.get_city()['title']).\
                first()

            if not city:
                city = Cities(
                    id=user.get_city()['id'],
                    name=user.get_city()['title']
                )
                session.add(city)
                session.commit()

            new_user = Users(
                id=user.get_user_id(),
                first_name=user.get_first_name(),
                last_name=user.get_last_name(),
                age=user.get_age(),
                gender_id=user.get_gender(),
                city_id=user.get_city()['id'],
                about_me=user.get_about_me()
            )
            session.add(new_user)
            session.commit()

            new_criteria = Criteries(
                user_id=user.get_user_id(),
                gender_id=user.get_gender(),
                status=1,
                age_from=user.get_age() - 5,
                age_to=user.get_age() + 5,
                city_id=user.get_city()['id'],
                has_photo=1
            )
            session.add(new_criteria)
            session.commit()

        session.close()


    def add_favorites(self, user: User):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        card = user.get_card().__dict__
        print(card)

        photos = card.get('photos')
        photo1 = photos[0] if len(photos) >= 1 else ''
        photo2 = photos[1] if len(photos) >= 2 else ''
        photo3 = photos[2] if len(photos) == 3 else ''

        new_favorite = Favorites(
            user_id=user.get_user_id(),
            first_name=card['first_name'],
            last_name=card['last_name'],
            age=card['age'],
            gender_id=card['gender'],
            profile='https://vk.com/id' + str(card['id']),
            photo1=photo1,
            photo2=photo2,
            photo3=photo3,
            city_id=card['city_id']
        )
        session.add(new_favorite)

        session.commit()
        session.close()


    # ?
    def add_exceptions(self, user: User):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        card = user.get_card()
        photos = card.get('photos')
        photo1 = photos[0] if len(photos) >= 1 else ''
        photo2 = photos[1] if len(photos) >= 2 else ''
        photo3 = photos[2] if len(photos) == 3 else ''

        new_exception = Exceptions(
            user_id=user.get_user_id(),
            first_name=card['first_name'],
            last_name=card['last_name'],
            age=0,
            gender_id=card['sex'],
            profile='https://vk.com/id' + str(card['id']),
            photo1=photo1,
            photo2=photo2,
            photo3=photo3,
            city_id=card['city']['id']
        )
        session.add(new_exception)

        session.commit()
        session.close()

    # ?
    def change_favorites(self, user_vk):
        pass

    # ?
    def change_exceptions(self, user_vk):
        pass


    def delete_favorites(self, user_id, profile):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        favorites_to_delete = session.query(Favorites).\
            filter_by(user_id=user_id, profile=profile).\
            all()

        for favorite in favorites_to_delete:
            session.delete(favorite)
            session.commit()

        session.close()


    def delete_exceptions(self, user_id, profile):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        exceptions_to_delete = session.query(Exceptions).\
            filter_by(user_id=user_id, profile=profile).\
            all()

        for exception in exceptions_to_delete:
            session.delete(exception)
            session.commit()

        session.close()


    def get_favorites(self, user_id, token_api):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        favorites_list = session.query(Favorites, Cities).\
            join(Cities, Cities.id == Favorites.city_id).\
            filter(Favorites.user_id == user_id).\
            all()

        card_list = []
        for favorite, city in favorites_list:
            card = CardFavorites()
            card.id = favorite.user_id
            card.first_name = favorite.first_name
            card.last_name = favorite.last_name
            card.age = favorite.age
            card.gender_id = favorite.gender_id
            card.profile = favorite.profile
            card.photos = [favorite.photo1, favorite.photo2, favorite.photo3]
            card.city_id = city.id
            card.city_name = city.name
            card_list.append(card.__dict__)

        session.close()

        if len(card_list) > 0:
            return card_list
        else:
            return None


    # ?
    def get_exceptions(self, user_id):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        favorites_list = session.query(Exceptions, Cities).\
            join(Cities, Cities.id == Exceptions.city_id).\
            filter(Exceptions.user_id == user_id).\
            all()

        card_list = []
        for exception, city in favorites_list:
            card = CardExceptions()
            card.id = exception.user_id
            card.first_name = exception.first_name
            card.last_name = exception.last_name
            card.age = exception.age
            card.gender_id = exception.gender_id
            card.profile = exception.profile
            card.photos = [exception.photo1,
                           exception.photo2,
                           exception.photo3]
            card.city_id = city.id
            card.city_name = city.name
            card_list.append(card.__dict__)

        session.close()

        if len(card_list) > 0:
            return card_list
        else:
            return None


    def get_user(self, user_id):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        user_query, city_query = session.query(Users, Cities).\
            join(Cities, Cities.id == Users.city_id).\
            filter(Users.id == user_id).\
            first()

        if user_query:
            user = User(user_id)
            user.set_first_name(user_query.first_name)
            user.set_last_name(user_query.last_name)
            user.set_age(user_query.age)
            user.set_gender(user_query.gender_id)
            user.set_about_me(user_query.about_me)
            user.set_city({'id': city_query.id,
                           'title': city_query.name})
            criteria = self.open_criteria(user_id)
            user.set_criteria(criteria)
            return user.__dict__
        else:
            return None


    def open_criteria(self, user_id):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        criteria_query, city_query = session.query(Criteries, Cities).\
            join(Cities, Cities.id == Criteries.city_id).\
            filter(Criteries.user_id == user_id).\
            first()

        if criteria_query:
            print('da')
            criteria = Criteria()
            criteria.id = criteria_query.id
            criteria.gender_id =  1 if criteria_query.gender_id == 2 else 1
            criteria.status = criteria_query.status
            criteria.age_from = criteria_query.age_from
            criteria.age_to =criteria_query.age_to
            criteria.city = {'id': city_query.id, 'name': city_query.name}
            criteria.has_photo = criteria_query.has_photo
            return criteria.__dict__
        else:
            return Criteria().__dict__


    def save_criteria(self, user: User):

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        criteria = user.get_criteria()

        city = session.query(Cities).\
            filter(Cities.name == criteria.city['name']).\
            first()

        if not city:
            new_city = Cities(
                id=criteria.city['id'],
                name=criteria.city['name']
            )
            session.add(new_city)
            session.commit()

        criteria_query = session.query(Criteries).\
            filter_by(id=criteria.id, user_id=user.get_user_id()).\
            first()

        if criteria_query:
            criteria_query.gender_id = criteria.gender_id
            criteria_query.status = criteria.status
            criteria_query.age_from = criteria.age_from
            criteria_query.age_to = criteria.age_to
            criteria_query.city_id = criteria.city['id']
            criteria_query.has_photo = criteria.has_photo

        session.close()