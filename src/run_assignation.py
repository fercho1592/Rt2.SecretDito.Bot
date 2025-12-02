
import random
import asyncio
from dependency import build_container
from interfaces.repo_protocols import ISecretDitoRepo, IAdminSecretDitoRepo
from models.graph.Graph import Graph

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

    if not paths:
        print("No valid assignation found.")
        exit(1)

    max_value = max(paths, key=lambda x: x[1])[1]
    best_paths = [path for path, value in paths if value == max_value]
    chosen_path = random.choice(best_paths)

    n = len(chosen_path)
    asignations = []
    for i in range(n):
        user = [u for u in users if u.user_id == chosen_path[i]][0]
        assigned_user = [u for u in users if u.user_id == chosen_path[(i + 1) % n]][0]
        user.set_amigo_secreto(assigned_user)

        asignations.append((user, assigned_user))
        asyncio.run(repo.UpdateUser(user))
    asyncio.run(admin_repo.SaveAssignationsToTxt(asignations))
    print("Asignaciones realizadas y guardadas en assignations.txt")