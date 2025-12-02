
from itertools import permutations
from models import User
from models.graph.GraphEdges import GraphEdge


class Graph:
    def __init__(self):
        self.edges = []  # List of GraphEdge objects
    
    def build_graph(self, users: list[User], invalid_edges: list[GraphEdge]) -> dict[int, dict[int, int]]:
        graph = {}
        user_ids = [u.user_id for u in users]
        for uid in user_ids:
            graph[uid] = {}
            for to_uid in user_ids:
                if uid != to_uid:
                    special_edge = next((edge for edge in invalid_edges if edge.from_user_id == uid and edge.to_user_id == to_uid), None)
                    graph[uid][to_uid] = special_edge.value if special_edge else 1
        return graph

    def remove_invalid_relations(self, graph: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:
        for uid in graph:
            graph[uid] = {k: v for k, v in graph[uid].items() if v != -1}
        return graph

    def get_hamiltonian_paths(self, graph):
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

    def path_value(self, path, graph):
        value = 0
        n = len(path)
        for i in range(n):
            frm = path[i]
            to = path[(i + 1) % n]
            value += graph[frm][to]
        return value