from abc import ABC, abstractmethod

from src.repository.query.user import (
    CreateUser,
    GetUserByName,
    GetUserById,
    UpdateUserActive,
)


class UserRepository(ABC):
    @property
    @abstractmethod
    def create_user(self) -> CreateUser: ...

    @property
    @abstractmethod
    def get_user_by_name(self) -> GetUserByName: ...

    @property
    @abstractmethod
    def get_user_by_id(self) -> GetUserById: ...

    @property
    @abstractmethod
    def set_token_permission(self) -> UpdateUserActive: ...
