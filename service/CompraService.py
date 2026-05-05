from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.CompraVO import CompraVO
from model.dao.CompraDAO import CompraDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.CompraCommand import InsertCompraCommand, DeleteCompraCommand

class CompraService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_compras(self) -> List[CompraVO]:
        return CompraDAO.get_all_compras()
    
    def get_compra(self, id: int) -> CompraVO | None:
        return CompraDAO.get_compra(id)

    def insert_compra(self, vo: CompraVO):
        with self.connection_factory() as connection:
            result = CompraDAO.insert_compra(connection, vo)
            if result:
                vo.compra_id = result
                if self.undo_manager:
                    self.undo_manager.register(InsertCompraCommand(vo))
            return result

    def delete_compra(self, id: int) -> None:
        vo = self.get_compra(id)
        if vo:
            CompraDAO.delete_compra(id)
            if self.undo_manager:
                self.undo_manager.register(DeleteCompraCommand(vo))
