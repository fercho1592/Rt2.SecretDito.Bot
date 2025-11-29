
import random
import asyncio
from itertools import permutations
from dependency import getAdminRepoInstance
from models.User import User
from models.GraphEdges import GraphEdge

def build_graph(users: list[User], invalid_edges: list[GraphEdge]) -> dict[int, dict[int, int]]:
    graph = {}
    user_ids = [u.user_id for u in users]
    for uid in user_ids:
        graph[uid] = {}
        for to_uid in user_ids:
            if uid != to_uid:
                special_edge = next((edge for edge in invalid_edges if edge.from_user_id == uid and edge.to_user_id == to_uid), None)
                graph[uid][to_uid] = special_edge.value if special_edge else 1
    return graph

def remove_invalid_relations(graph: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:
    for uid in graph:
        graph[uid] = {k: v for k, v in graph[uid].items() if v != -1}
    return graph

def get_hamiltonian_paths(graph):
    user_ids = list(graph.keys())
    paths = []
    for perm in permutations(user_ids):
        valid = True
        for i in range(len(perm)):
            frm = perm[i]
            to = perm[(i + 1) % len(perm)]
            if to not in graph[frm]:
                valid = False
                break
        if valid:
            paths.append(perm)
    return paths

def path_value(path, graph):
    value = 0
    n = len(path)
    for i in range(n):
        frm = path[i]
        to = path[(i + 1) % n]
        value += graph[frm][to]
    return value

def notify_user(user_id, assigned_id):
    # Stub: implement notification logic here
    print(f"* {user_id} -> {assigned_id}")

if __name__ == '__main__':
    admin_repo = getAdminRepoInstance()
    # read from data files all users and set nodes for gaph
    users: list[User] = asyncio.run(admin_repo.GetAllUsers())
    invalid_edges = asyncio.run(admin_repo.GetInvalidEdges())

    # create relation among users
    graph = build_graph(users, invalid_edges)

    # remove invalid relations
    graph = remove_invalid_relations(graph)

    # get a list of all hamiltonian paths
    paths = get_hamiltonian_paths(graph)

    # set a value for each path based on relation weights
    if not paths:
        print("No valid assignation found.")
        exit(1)

    scored = [(path, path_value(path, graph)) for path in paths]

    # get the best paths
    # in case of multiple best paths, select one randomly
    max_value = max(scored, key=lambda x: x[1])[1]
    best_paths = [p for p, v in scored if v == max_value]
    chosen_path = random.choice(best_paths)

    # call function to notify each user
    n = len(chosen_path)
    asignations = []
    for i in range(n):
        user: User = [u for u in users if u.user_id == chosen_path[i]][0]
        assigned_user: User = [u for u in users if u.user_id == chosen_path[(i + 1) % n]][0]
        user.set_amigo_secreto(assigned_user)

        asignations.append((user, assigned_user))
        notify_user(user.name, assigned_user.name)
