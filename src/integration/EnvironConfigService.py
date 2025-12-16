from os import environ
from interfaces.enums import ConfigEnum
from interfaces.config_protocols import ConfigServiceProtocol


class EnvironConfig(ConfigServiceProtocol):
    def __init__(self):
        pass

    def get_config_value(self, service_name: ConfigEnum) -> str:
        service_name_str = str(service_name).upper()
        value = environ.get(service_name_str)
        return value if value is not None else ConfigEnum.get_default(service_name)
