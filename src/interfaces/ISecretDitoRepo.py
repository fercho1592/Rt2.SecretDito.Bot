from abc import ABC, abstractmethod

from models.User import User

class ISecretDitoRepo(ABC):
    @abstractmethod
    async def GetUserById(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def CreateUser(self, user: User):
        pass

    @abstractmethod
    async def UpdateUser(self, user: User):
        pass