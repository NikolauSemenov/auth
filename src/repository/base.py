from abc import ABC, abstractmethod

from src.repository.query.user import CreateUser, GetUserByName


class UserRepository(ABC):
    @property
    @abstractmethod
    def create_user(self) -> CreateUser: ...

    @property
    @abstractmethod
    def get_user_by_name(self) -> GetUserByName: ...
