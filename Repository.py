from User import User
from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def add_favorites(self, user_vk):
        pass

    @abstractmethod
    def add_exceptions(self, user_vk):
        pass

    @abstractmethod
    def change_favorites(self, user_vk):
        pass

    @abstractmethod
    def change_exceptions(self, user_vk):
        pass

    @abstractmethod
    def delete_favorites(self, user_vk):
        pass

    @abstractmethod
    def delete_exceptions(self, user_vk):
        pass

    @abstractmethod
    def get_favorites(self, user_id):
        pass

    @abstractmethod
    def get_exceptions(self, user_id):
        pass