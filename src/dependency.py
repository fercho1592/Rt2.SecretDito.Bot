
from integration.SecretSantaRepo import SecretSantaRepo
from integration.YamlConfigService import YamlConfigService
from integration.TelegramApiFacade import TelegramApiFacade
from interfaces.ISecretDitoRepo import ISecretDitoRepo
from interfaces.IAdminSecretDitoRepo import IAdminSecretDitoRepo
from interfaces.config_reader.IConfigService import IConfigService

def getRepoInstance() -> ISecretDitoRepo:
    return SecretSantaRepo()

def getAdminRepoInstance() -> IAdminSecretDitoRepo:
    return SecretSantaRepo()

def getConfigService() -> IConfigService:
    return YamlConfigService()

def getBotApiFacade() -> TelegramApiFacade:
    config_service = getConfigService()
    return TelegramApiFacade(config_service)