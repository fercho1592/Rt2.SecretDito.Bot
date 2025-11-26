from abc import ABC
from abc import abstractmethod

class ISecretDitoRepo(ABC):
    @abstractmethod
    async def getUserById(self, user_id: int):
        pass

    @abstractmethod
    async def createUser(self, user):
        pass

    @abstractmethod
    async def updateUser(self, user):
        pass