import yaml
from interfaces.enums import ConfigEnum
from interfaces.config_protocols import ConfigServiceProtocol


class YamlConfigService(ConfigServiceProtocol):
    def __init__(self, config_path: str = ".env"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get_config_value(self, service_name: ConfigEnum) -> str:
        default_value = ConfigEnum.DEFAULTS.get(service_name)
        return self.config.get("services", {}).get(str(service_name), default_value)
