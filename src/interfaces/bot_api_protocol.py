from typing  import Protocol
from models.User import User

class IBotApiFacade(Protocol):
    def notify_user(self, user: User, message: str) -> None: ...