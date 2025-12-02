from typing  import Protocol
from interfaces.enums import ConfigEnum

class ConfigServiceProtocol(Protocol):
    def get_config_value(self, service_name: ConfigEnum) -> str: ...
    def get_all_services(self) -> dict: ...
    
class FlagServiceProtocol(Protocol):
    def is_asignation_done(self) -> bool: ...
    pass
