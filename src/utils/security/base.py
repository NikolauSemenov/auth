from abc import ABC, abstractmethod


class SecurityToken(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def create_access_token(self, user_id: int) -> str: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> bool: ...

    @abstractmethod
    def get_token_ttl(self, token: str) -> int: ...
