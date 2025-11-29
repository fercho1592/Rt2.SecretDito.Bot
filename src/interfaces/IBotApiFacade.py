from abc import ABC, abstractmethod
from models.User import User

class IBotApiFacade(ABC):

    @abstractmethod
    def notify_user(self, user: User, message: str) -> None:
        pass