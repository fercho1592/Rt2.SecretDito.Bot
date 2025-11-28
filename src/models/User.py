from typing import  Dict, Any
from models.WishListItem import WishListItem

class User:
    def __init__(self, user_id: int, username: str, name: str = None, chat_id: int = None,wish_list: list = None):
        self.user_id = user_id
        self.username = username
        self.chat_id = chat_id
        self.name = name
        self.wish_list: list[WishListItem] = wish_list if wish_list is not None else []

    def to_dict(self):
        """Convierte el objeto a un diccionario para serializar."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "chat_id": self.chat_id,
            "name": self.name,
            #"amigo_secreto_id": self.amigo_secreto_id,
            "wish_list": [item.to_dict() for item in self.wish_list]
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """Crea un objeto User desde un diccionario."""
        user = User(
            user_id=data.get('user_id'),
            chat_id=data.get('chat_id'),
            username=data.get('username'),
            name=data.get('name'),
            #amigo_secreto_id=data.get('amigo_secreto_id'),
        )

        user.wish_list = [WishListItem.from_dict(item_data) for item_data in data.get('wish_list', [])]
        return user

    def set_name(self, name: str) -> None:
        self.name = name

    def add_to_wish_list(self, wish_list_item: WishListItem) -> None:
        self.wish_list.append(wish_list_item)

    async def show_wish_list(self, reply_function: callable, get_message_id: callable) -> None:
        if not self.wish_list:
            reply_function("Tu wish list está vacía.")
            return

        reply_function("Tu wish list:")
        for item in self.wish_list:
            reply_message = await reply_function(str(item))
            item.message_ids.append(get_message_id(reply_message))

    def remove_wish_list_item_by_message_id(self, message_id: int) -> WishListItem | None:
        for item in self.wish_list:
            if message_id in item.message_ids:
                self.wish_list.remove(item)
                return item
        return None