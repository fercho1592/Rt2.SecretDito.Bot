import yaml
from interfaces.enums import ConfigEnum
from interfaces.config_protocols import ConfigServiceProtocol

class YamlConfigService(ConfigServiceProtocol):
    def __init__(self, config_path: str = ".env"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get_service_api_key(self, service_name: ConfigEnum) -> str:
        return self.config.get("services", {}).get(str(service_name), "")

    def get_all_services(self) -> dict:
        return self.config.get("services", {})
