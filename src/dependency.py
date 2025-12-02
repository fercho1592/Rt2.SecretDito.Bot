
from integration.container import Container
from integration.SecretSantaRepo import SecretSantaRepo
from integration.YamlConfigService import YamlConfigService
from integration.TelegramApiFacade import TelegramApiFacade
from integration.flag_service import FlagService
from interfaces.config_protocols import ConfigServiceProtocol, FlagServiceProtocol
from interfaces.enums import ConfigEnum
from interfaces.repo_protocols import ISecretDitoRepo, IAdminSecretDitoRepo
from interfaces.bot_api_protocol import IBotApiFacade

def build_container() -> Container:
    container = Container()

    container.register(SecretSantaRepo, lambda: SecretSantaRepo(
        assignation_file=f"{container.resolve(ConfigServiceProtocol).get_config_value(ConfigEnum.ASSIGNATION_FILE)}",
        data_dir="data",
        invalid_edges_file=container.resolve(ConfigServiceProtocol).get_config_value(ConfigEnum.GRAPH_SETTINGS_FILE)
    ), True)
    container.register(ConfigServiceProtocol, YamlConfigService, True)
    container.register(FlagServiceProtocol, lambda: 
                       FlagService(f"data/{container.resolve(ConfigServiceProtocol).get_config_value(ConfigEnum.ASSIGNATION_FILE)}"), True)

    container.register(ISecretDitoRepo, lambda: container.resolve(SecretSantaRepo))
    container.register(IAdminSecretDitoRepo, lambda: container.resolve(SecretSantaRepo))

    container.register(IBotApiFacade, lambda: \
                       TelegramApiFacade(container.resolve(ConfigServiceProtocol)))

    return container
