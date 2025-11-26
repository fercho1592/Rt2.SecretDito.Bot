from typing import  Dict, Any
class WishListItem():
    def __init__(self, item: str, message_ids: list[int]):
        self.item = item
        self.message_ids = message_ids

    def to_dict(self):
        """Convierte el objeto a un diccionario para serializar."""
        return {
            "item": self.item,
            "message_ids": self.message_ids
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """Crea un objeto User desde un diccionario."""
        return WishListItem(
            item=data.get('item'),
            message_ids=data.get('message_ids', [])
        )