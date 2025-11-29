import asyncio
from dependency import getAdminRepoInstance, getRepoInstance, getBotApiFacade
from models.User import User
from interfaces.IBotApiFacade import IBotApiFacade
from interfaces.IAdminSecretDitoRepo import IAdminSecretDitoRepo

async def notify_all_users(botFacade: IBotApiFacade, repo: IAdminSecretDitoRepo):
    users:list[User] = await repo.GetAllUsers()
    for user in users:
        await notify_user(botFacade, user)
    pass


async def notify_user(botFacade: IBotApiFacade, user: User):
    message = f'Hola {user.name}, ya se te ha asignado un amigo secreto!\n'+\
            'Usa /secret_friend para ver quien es \n'+\
            'Y /secret_wish_list para ver su wish list'
    await botFacade.notify_user(user, message)
    message = 'Y recuerda mantener tu wish list actualizada compartiendos por este chat'
    await botFacade.notify_user(user, message)

if __name__ == '__main__':
    adminRepo = getAdminRepoInstance()
    repo = getRepoInstance()
    bot_api = getBotApiFacade()

    user = asyncio.run(repo.GetUserById(1345956985))
    asyncio.run(notify_user(bot_api, user))