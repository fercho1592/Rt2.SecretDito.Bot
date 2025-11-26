from typing import  Dict, Any
from models.WishListItem import WishListItem

class User:
    def __init__(self, user_id: int, username: str, name: str = None, wish_list: list = None):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.wish_list: list[WishListItem] = wish_list if wish_list is not None else []

    def add_to_wish_list(self, item: str, message_id: int):
        self.wish_list.append({"item": item, "message_id": message_id})

    def to_dict(self):
        """Convierte el objeto a un diccionario para serializar."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            #"amigo_secreto_id": self.amigo_secreto_id,
            "wish_list": [item.to_dict() for item in self.wish_list]
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """Crea un objeto User desde un diccionario."""
        user = User(
            user_id=data.get('user_id'),
            username=data.get('username'),
            name=data.get('name'),
            #amigo_secreto_id=data.get('amigo_secreto_id'),
        )

        user.wish_list = [WishListItem.from_dict(item_data) for item_data in data.get('wish_list', [])]
        return user