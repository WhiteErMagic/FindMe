import pytest
from sqlalchemy.orm import sessionmaker

from User import User
from CheckBD.ORMTableStructure import Users
from Repository.ORMRepository import ORMRepository


class TestRepositoryORM:

    TEST_USER_ID = 10101010
    TEST_FIRST_NAME = 'Тестовый'
    TEST_LAST_NAME = 'Пользователь'
    TEST_AGE = 28
    TEST_GENDER = 2
    TEST_CITY_ID = 1
    TEST_CITY_NAME = 'Москва'
    TEST_ABOUT_ME = 'Я тестовый пользователь'

    def setup_method(self):
        self.checkorm = ORMRepository()
        self.user = User(self.TEST_USER_ID)

    def teardown_method(self):
        del self.checkorm
        del self.user

    def set_user_params(self):
        self.user.set_first_name(self.TEST_FIRST_NAME)
        self.user.set_last_name(self.TEST_LAST_NAME)
        self.user.set_age(self.TEST_AGE)
        self.user.set_gender(self.TEST_GENDER)
        self.user.set_city({'id': self.TEST_CITY_ID,
                            'title': self.TEST_CITY_NAME})
        self.user.set_about_me(self.TEST_ABOUT_ME)

    def delete_test_user_row(self):
        engine = self.checkorm.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        user_to_delete = session.query(Users).\
            filter_by(id=self.TEST_USER_ID).\
            all()
        for exception in user_to_delete:
            session.delete(exception)
            session.commit()

    @pytest.mark.parametrize('expected_user_id', ([TEST_USER_ID]))
    def test_add_user(self, expected_user_id):
        self.set_user_params()
        self.checkorm.add_user(self.user)
        dict_result = self.checkorm.get_user(self.TEST_USER_ID)
        actual_user_id = dict_result.get('_User__id')
        assert actual_user_id == expected_user_id
        self.delete_test_user_row()