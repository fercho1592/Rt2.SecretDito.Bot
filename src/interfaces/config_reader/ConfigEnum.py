from enum import Enum

class ConfigEnum(Enum):
    TELEGRAM_TOKEN = "telegram_token"
    # Agrega aquí más claves según se necesiten

    def __str__(self):
        return self.value