from abc import ABC, abstractmethod
from models.User import User

class IAdminSecretDitoRepo(ABC):

    async def GetAllUsers(self) -> list[User]:
        pass

    def load_invalid_edges(self):
        pass