import json
import os
from interfaces.repo_protocols import ISecretDitoRepo, IAdminSecretDitoRepo
from pathlib import Path
from models.User import User
from models.graph.GraphEdgesSettings import GraphEdgeSettings
from typing import Optional

USER_DATA_DIR = Path('data')
INVALID_EDGES_FILE =  'graph_settings.json'

class SecretSantaRepo(ISecretDitoRepo, IAdminSecretDitoRepo):
    def __init__(self, data_dir=USER_DATA_DIR, invalid_edges_file=INVALID_EDGES_FILE):
        self.data_dir = Path(data_dir)
        self.invalid_edges_file = invalid_edges_file
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_filepath(self, user_id: int) -> Path:
        return self.data_dir / f'{user_id}.json'

    # --- Implementación de los métodos de la interfaz ISecretDitoRepo ---

    async def GetUserById(self, user_id: int) -> Optional[User]:
        filepath = self._get_filepath(user_id)

        if not filepath.exists():
            return None

        try:
            # Operación síncrona dentro de una función async.
            # En producción, usarías asyncio.to_thread para no bloquear el bucle.
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return User.from_dict(data)
        except Exception as e:
            print(f'Error al cargar el usuario {user_id}: {e}')
            return None

    async def CreateUser(self, user: User) -> bool:
        filepath = self._get_filepath(user.user_id)

        if filepath.exists():
            print(f'Error: El usuario {user.user_id} ya existe.')
            return False

        return await self._save_user_to_file(user)

    async def UpdateUser(self, user: User) -> bool:
        return await self._save_user_to_file(user)

    async def _save_user_to_file(self, user: User) -> bool:
        filepath = self._get_filepath(user.user_id)

        try:
            # Operación síncrona dentro de una función async
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(user.to_dict(), f, indent=4)
            return True
        except Exception as e:
            print(f'Error al guardar el usuario {user.user_id}: {e}')
            return False

    async def GetAllUsers(self) -> list[User]:
        users = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.json') and file != self.invalid_edges_file:
                with open(self.data_dir / file, 'r', encoding='utf-8') as f:
                    users.append(User.from_dict(json.load(f)))
        return users

    async def GetInvalidEdges(self) -> list[GraphEdgeSettings]:
        filepath = self.data_dir / self.invalid_edges_file
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            edges = json.load(f)
        invalid = []
        for edge in edges:
            invalid.append(GraphEdgeSettings(edge['user_id'], edge['to_user_id'], edge['value']))
        return invalid

    async def SaveAssignationsToTxt(self, assignations: list[tuple[User, User]], filename: str = "assignations.txt") -> None:
        filepath = self.data_dir / filename
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                for user1, user2 in assignations:
                    line = f"({user1.user_id}, {user1.name}) -> ({user2.user_id}, {user2.name})\n"
                    f.write(line)
        except Exception as e:
            print(f"Error al guardar las asignaciones: {e}")