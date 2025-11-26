
from integration.SecretSantaRepo import SecretSantaRepo
from integration.YamlConfigService import YamlConfigService
from interfaces.ISecretDitoRepo import ISecretDitoRepo
from interfaces.config_reader.IConfigService import IConfigService

def getRepoInstance() -> ISecretDitoRepo:
    return SecretSantaRepo()

def getConfigService() -> IConfigService:
    return YamlConfigService()
