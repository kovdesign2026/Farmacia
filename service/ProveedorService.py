from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.ProveedorVO import ProveedorVO
from model.dao.ProveedorDAO import ProveedorDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.ProveedorCommand import InsertProveedorCommand, DeleteProveedorCommand

class ProveedorService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_proveedores(self) -> List[ProveedorVO]:
        return ProveedorDAO.get_all_proveedores()
    
    def get_proveedor(self, id: int) -> ProveedorVO | None:
        return ProveedorDAO.get_proveedor(id)

    def insert_proveedor(self, vo: ProveedorVO):
        with self.connection_factory() as connection:
            result = ProveedorDAO.insert_proveedor(connection, vo)
            if result:
                vo.proveedor_id = result
                if self.undo_manager:
                    self.undo_manager.register(InsertProveedorCommand(vo))
            return result

    def delete_proveedor(self, id: int) -> None:
        vo = self.get_proveedor(id)
        if vo:
            ProveedorDAO.delete_proveedor(id)
            if self.undo_manager:
                self.undo_manager.register(DeleteProveedorCommand(vo))
