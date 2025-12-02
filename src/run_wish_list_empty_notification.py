import asyncio
from dependency import build_container
from models.User import User
from interfaces.bot_api_protocol import IBotApiFacade
from interfaces.repo_protocols import IAdminSecretDitoRepo

async def notify_all_users(botFacade: IBotApiFacade, repo: IAdminSecretDitoRepo):
    users:list[User] = await repo.GetAllUsers()
    for user in users:
        if len(user.wish_list) > 0:
            continue
        await notify_user(botFacade, user)
    pass

async def notify_user(botFacade: IBotApiFacade, user: User):
    message = f'Hey {user.name}!!, Recuerda actualizar tu lista de regalos\n'+\
        'Comparte los items que te interesan para que tu amigo secreto sepa que regalarte!'
    await botFacade.notify_user(user, message)

if __name__ == '__main__':
    container = build_container()
    adminRepo = container.resolve(IAdminSecretDitoRepo)
    repo = container.resolve(IAdminSecretDitoRepo)
    bot_api = container.resolve(IBotApiFacade)

    asyncio.run(notify_all_users(bot_api, adminRepo))
    pass
