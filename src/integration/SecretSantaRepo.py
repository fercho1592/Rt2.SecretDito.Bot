import json
from interfaces.ISecretDitoRepo import ISecretDitoRepo
from pathlib import Path
from models.User import User
from typing import Optional


USER_DATA_DIR = Path("data")


class SecretSantaRepo(ISecretDitoRepo):
    """
    Implementación del repositorio ISecretDitoRepo usando archivos JSON
    para cada usuario.
    """

    def __init__(self, data_dir=USER_DATA_DIR):

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_filepath(self, user_id: int) -> Path:
        """Obtiene la ruta completa del archivo JSON para un usuario específico."""
        return self.data_dir / f"{user_id}.json"

    # --- Implementación de los métodos de la interfaz ISecretDitoRepo ---
    
    async def getUserById(self, user_id: int) -> Optional[User]:
        """
        Busca y retorna un usuario por su user_id.
        """
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
            print(f"Error al cargar el usuario {user_id}: {e}")
            return None

    async def createUser(self, user: User) -> bool:
        """
        Crea un nuevo archivo JSON para el usuario.
        """
        filepath = self._get_filepath(user.user_id)
        
        if filepath.exists():
            print(f"Error: El usuario {user.user_id} ya existe.")
            return False
            
        return await self._save_user_to_file(user)

    async def updateUser(self, user: User) -> bool:
        """
        Actualiza (sobrescribe) el archivo JSON para el usuario.
        """
        return await self._save_user_to_file(user)
    
    # --- Método auxiliar privado ---
    
    async def _save_user_to_file(self, user: User) -> bool:
        """
        Serializa el objeto User y lo guarda en su archivo JSON.
        """
        filepath = self._get_filepath(user.user_id)
        
        try:
            # Operación síncrona dentro de una función async
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(user.to_dict(), f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar el usuario {user.user_id}: {e}")
            return False