
from integration.container import Container
from integration.SecretSantaRepo import SecretSantaRepo
from integration.YamlConfigService import YamlConfigService
from integration.TelegramApiFacade import TelegramApiFacade
from interfaces.config_reader.protocols import ConfigServiceProtocol
from interfaces.ISecretDitoRepo import ISecretDitoRepo
from interfaces.IAdminSecretDitoRepo import IAdminSecretDitoRepo
from interfaces.config_reader.IConfigService import IConfigService
from interfaces.IBotApiFacade import IBotApiFacade

@DeprecationWarning
def getRepoInstance() -> ISecretDitoRepo:
    return SecretSantaRepo()

@DeprecationWarning
def getAdminRepoInstance() -> IAdminSecretDitoRepo:
    return SecretSantaRepo()

@DeprecationWarning
def getConfigService() -> IConfigService:
    return YamlConfigService()

@DeprecationWarning
def getBotApiFacade() -> IBotApiFacade:
    config_service = getConfigService()
    return TelegramApiFacade(config_service)

def build_container() -> Container:
    container = Container()

    container.register(SecretSantaRepo, SecretSantaRepo, True)
    container.register(SecretSantaRepo, YamlConfigService, True)

    container.register(ISecretDitoRepo, lambda: container.resolve(SecretSantaRepo))
    container.register(IAdminSecretDitoRepo, lambda: container.resolve(SecretSantaRepo))
    container.register(IConfigService, lambda: container.resolve(YamlConfigService))
    container.register(ConfigServiceProtocol, lambda: container.resolve(YamlConfigService))

    container.register(IBotApiFacade, lambda: \
                       TelegramApiFacade(container.resolve(IConfigService)))

    return container
