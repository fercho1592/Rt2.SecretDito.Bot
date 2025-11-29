import asyncio
from dependency import getAdminRepoInstance, getRepoInstance, getBotApiFacade
from models.User import User
from interfaces.IBotApiFacade import IBotApiFacade
from interfaces.IAdminSecretDitoRepo import IAdminSecretDitoRepo
from interfaces.ISecretDitoRepo import ISecretDitoRepo

async def notify_all_users(botFacade: IBotApiFacade, repo: IAdminSecretDitoRepo):
    users:list[User] = await repo.GetAllUsers()
    for user in users:
        message = f"Hello {user.name}, this is a notification!"
        await botFacade.notify_user(user, message)

async def notify_user(botFacade: IBotApiFacade, repo: ISecretDitoRepo):
    user:User = await repo.GetUserById(1345956985)
    message = f"Hello {user.name}, this is a notification!"
    await botFacade.notify_user(user, message)

if __name__ == '__main__':
    adminRepo = getAdminRepoInstance()
    repo = getRepoInstance()
    bot_api = getBotApiFacade()

    asyncio.run(notify_user(bot_api, repo))