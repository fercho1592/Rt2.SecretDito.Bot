
import random
import asyncio
from dependency import build_container
from interfaces.repo_protocols import ISecretDitoRepo, IAdminSecretDitoRepo
from interfaces.bot_api_protocol import IBotApiFacade
from models.User import User
from models.graph.Graph import Graph

async def save_assignations(repo: ISecretDitoRepo, admin_repo: IAdminSecretDitoRepo, chosen_path: dict[int, int]):
    n = len(chosen_path)
    asignations = []
    for i in range(n):
        user = [u for u in users if u.user_id == chosen_path[i]][0]
        assigned_user = [u for u in users if u.user_id == chosen_path[(i + 1) % n]][0]
        user.set_amigo_secreto(assigned_user)

        asignations.append((user, assigned_user))
        await repo.UpdateUser(user)
    await admin_repo.SaveAssignationsToTxt(asignations)

def select_path(paths: list[tuple[dict[int, int], int]]) -> dict[int, int]:
    if not paths:
        raise ValueError("No valid assignation found.")

    max_value = max(paths, key=lambda x: x[1])[1]
    best_paths = [path for path, value in paths if value == max_value]
    return random.choice(best_paths)

async def notify_all_users(botFacade: IBotApiFacade, repo: IAdminSecretDitoRepo):
    users:list[User] = await repo.GetAllUsers()
    for user in users:
        
        message = f'Hola {user.name}, ya se te ha asignado un amigo secreto!\n'+\
            'Usa /secret_friend para ver quien es \n'+\
            'Y /secret_wish_list para ver su wish list'
        await botFacade.notify_user(user, message)
        
        message = 'Y recuerda mantener tu wish list actualizada compartiendos por este chat'
        await botFacade.notify_user(user, message)
    pass

if __name__ == '__main__':
    container = build_container()
    repo: ISecretDitoRepo = container.resolve(ISecretDitoRepo)
    admin_repo: IAdminSecretDitoRepo = container.resolve(IAdminSecretDitoRepo)
    users = asyncio.run(admin_repo.GetAllUsers())
    invalid_edges = asyncio.run(admin_repo.GetInvalidEdges())

    graph_obj = Graph()
    graph_obj.build_graph(users)
    graph_obj.set_graph_settings(invalid_edges)
    paths = graph_obj.get_hamiltonian_paths()
    chosen_path = select_path(paths)

    asyncio.run(save_assignations(repo, admin_repo, chosen_path))

    print("Asignaciones realizadas y guardadas en assignations.txt")
    bot_api = container.resolve(IBotApiFacade)
    asyncio.run(notify_all_users(bot_api, admin_repo))
    pass