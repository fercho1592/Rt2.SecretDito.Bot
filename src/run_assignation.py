import os
import json
import random
from pathlib import Path
from itertools import permutations

DATA_DIR = Path("data")
INVALID_EDGES_FILE = DATA_DIR / "invalidEdges.json"

def load_users(data_dir):
    users = []
    for file in os.listdir(data_dir):
        if file.endswith(".json") and file != "invalidEdges.json":
            with open(data_dir / file, "r", encoding="utf-8") as f:
                users.append(json.load(f))
    return users

def load_invalid_edges(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        edges = json.load(f)
    invalid = set()
    for edge in edges:
        invalid.add((edge["user_id"], edge["to_user_id"]))
    return invalid

def build_graph(users, invalid_edges):
    graph = {}
    user_ids = [u["user_id"] for u in users]
    for uid in user_ids:
        graph[uid] = {}
        for to_uid in user_ids:
            if uid != to_uid:
                graph[uid][to_uid] = 1 if (uid, to_uid) not in invalid_edges else -1
    return graph

def remove_invalid_relations(graph):
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
    # read from data files all users and set nodes for gaph
    users = load_users(DATA_DIR)
    invalid_edges = load_invalid_edges(INVALID_EDGES_FILE)

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
    for i in range(n):
        user_id = [u for u in users if u["user_id"] == chosen_path[i]][0]["name"]
        assigned_id = [u for u in users if u["user_id"] == chosen_path[(i + 1) % n]][0]["name"]
        notify_user(user_id, assigned_id)
