from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.FarmaceuticoVO import FarmaceuticoVO
from model.dao.FarmaceuticoDAO import FarmaceuticoDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.FarmaceuticoCommand import InsertFarmaceuticoCommand, DeleteFarmaceuticoCommand

class FarmaceuticoService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_farmaceuticos(self) -> List[FarmaceuticoVO]:
        return FarmaceuticoDAO.get_all_farmaceuticos()
    
    def get_farmaceutico(self, id: int) -> FarmaceuticoVO | None:
        return FarmaceuticoDAO.get_farmaceutico(id)

    def insert_farmaceutico(self, vo: FarmaceuticoVO):
        with self.connection_factory() as connection:
            result = FarmaceuticoDAO.insert_farmaceutico(connection, vo)
            if result:
                vo.farmaceutico_id = result
                if self.undo_manager:
                    self.undo_manager.register(InsertFarmaceuticoCommand(vo))
            return result

    def delete_farmaceutico(self, id: int) -> None:
        vo = self.get_farmaceutico(id)
        if vo:
            FarmaceuticoDAO.delete_farmaceutico(id)
            if self.undo_manager:
                self.undo_manager.register(DeleteFarmaceuticoCommand(vo))
