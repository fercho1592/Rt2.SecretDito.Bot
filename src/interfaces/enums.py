from enum import Enum

class ConfigEnum(Enum):
    TELEGRAM_TOKEN = "telegram_token"
    ASSIGNATION_FILE = "assignation_file"
    GRAPH_SETTINGS_FILE = "graph_settings_file"
    # Agrega aquí más claves según se necesiten

    def __str__(self):
        return self.value
    