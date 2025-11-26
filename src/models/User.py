class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.wish_list = []

    def add_to_wish_list(self, item: str, message_id: int):
        self.wish_list.append({"item": item, "message_id": message_id})