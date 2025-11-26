from abc import ABC, abstractmethod
from . import ConfigEnum

class IConfigService(ABC):
    @abstractmethod
    def get_service_api_key(self, service_name: ConfigEnum) -> str:
        """Devuelve la API key del servicio especificado."""
        pass

    @abstractmethod
    def get_all_services(self) -> dict:
        """Devuelve todas las configuraciones de servicios."""