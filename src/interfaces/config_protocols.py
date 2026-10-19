from typing import Protocol
from interfaces.enums import ConfigEnum


class ConfigServiceProtocol(Protocol):
    def get_config_value(self, service_name: ConfigEnum) -> str: ...


class FlagServiceProtocol(Protocol):
    def is_asignation_done(self) -> bool: ...

    pass
