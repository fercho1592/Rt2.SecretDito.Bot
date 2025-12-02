from itertools import permutations
from models.User import User
from models.graph.GraphEdgesSettings import GraphEdgeSettings

class Graph:
    def __init__(self):
        self.edges_map: dict[int, list[tuple[int, int]]] = {}  # Tuple of (to_user_id, value)

    def build_graph(self, users: list[User]) -> dict[int, dict[int, int]]:
        graph = {}
        for usr in users:
            graph[usr.user_id] = [(u.user_id, 1) for u in users]

        self.edges_map = graph
        return self

    def set_graph_settings(self, edges_settings: list[GraphEdgeSettings]):
        for (from_user_id, to_user_id, value) in edges_settings:
            if from_user_id not in self.edges_map:
                continue

            # find the edge and update its value
            self.edges_map[from_user_id] = [
                (to_id, value) if to_id == to_user_id else (to_id, val)
                for to_id, val in self.edges_map[from_user_id]
            ]

            self.edges_map[from_user_id] = [
                (to_id, val) for to_id, val in self.edges_map[from_user_id] if val != -1
            ]

    def get_hamiltonian_paths(self) -> list[tuple[tuple[int, ...], int]]:
        user_ids = list(self.edges_map.keys())
        paths: list[tuple[tuple[int, ...], int]] = []
        for perm in permutations(user_ids):
            valid = True
            value = 0
            for i in range(len(perm)):
                frm = perm[i]
                to = perm[(i + 1) % len(perm)]

                to_edge = [edge for edge in self.edges_map[frm] if edge[0] == to]

                if not to_edge:
                    valid = False
                    break
                
                value += to_edge[0][1]

            if valid:
                paths.append((perm, value))
        return paths