from typing import Dict, Any

class GraphEdgeSettings:
    def __init__(self, from_user_id: int, to_user_id: int, value: int):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.value = value

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """Crea un objeto User desde un diccionario."""
        edge = GraphEdgeSettings(
            from_user_id=data.get('user_id'),
            to_user_id=data.get('to_user_id'),
            value=data.get('value')
        )

        return edge