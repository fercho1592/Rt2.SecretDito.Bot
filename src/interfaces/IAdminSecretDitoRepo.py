from abc import ABC, abstractmethod
from models.User import User
from models.GraphEdges import GraphEdge

class IAdminSecretDitoRepo(ABC):
    @abstractmethod
    async def GetAllUsers(self) -> list[User]:
        pass
    @abstractmethod
    async def GetInvalidEdges(self) -> list[GraphEdge]:
        pass
    @abstractmethod
    async def SaveAssignationsToTxt(self, assignations: list[tuple[User, User]], filename: str = "assignations.txt") -> None:
        pass
