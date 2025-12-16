from enum import Enum
from typing import Self


class ConfigEnum(Enum):
    TELEGRAM_TOKEN = "telegram_token"
    ASSIGNATION_FILE = "assignation_file"
    GRAPH_SETTINGS_FILE = "graph_settings_file"
    # Agrega aquí más claves según se necesiten

    @staticmethod
    def get_default(service_name: Self) -> str:
        default = {
            ConfigEnum.ASSIGNATION_FILE: "assignation.json",
            ConfigEnum.GRAPH_SETTINGS_FILE: "graph_settings.json",
        }
        return default.get(service_name)

    def __str__(self):
        return self.value
