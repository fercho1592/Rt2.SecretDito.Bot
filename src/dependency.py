
from integration.SecretSantaRepo import SecretSantaRepo
from interfaces.ISecretDitoRepo import ISecretDitoRepo

def getRepoInstance() -> ISecretDitoRepo:
    return SecretSantaRepo()
