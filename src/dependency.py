
from integration.container import Container
from integration.SecretSantaRepo import SecretSantaRepo
from integration.YamlConfigService import YamlConfigService
from integration.TelegramApiFacade import TelegramApiFacade
from interfaces.config_protocols import ConfigServiceProtocol
from interfaces.repo_protocols import ISecretDitoRepo, IAdminSecretDitoRepo
from interfaces.bot_api_protocol import IBotApiFacade

def build_container() -> Container:
    container = Container()

    container.register(SecretSantaRepo, SecretSantaRepo, True)
    container.register(YamlConfigService, YamlConfigService, True)

    container.register(ISecretDitoRepo, lambda: container.resolve(SecretSantaRepo))
    container.register(IAdminSecretDitoRepo, lambda: container.resolve(SecretSantaRepo))
    container.register(ConfigServiceProtocol, lambda: container.resolve(YamlConfigService))

    container.register(IBotApiFacade, lambda: \
                       TelegramApiFacade(container.resolve(ConfigServiceProtocol)))

    return container
