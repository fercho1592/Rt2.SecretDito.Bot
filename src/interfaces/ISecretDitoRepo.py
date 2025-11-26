from abc import ABC
from abc import abstractmethod

from models.User import User

class ISecretDitoRepo(ABC):
    @abstractmethod
    async def getUserById(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def createUser(self, user: User):
        pass

    @abstractmethod
    async def updateUser(self, user: User):
        pass