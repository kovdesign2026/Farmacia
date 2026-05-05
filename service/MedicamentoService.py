from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.MedicamentoVO import MedicamentoVO
from model.dao.MedicamentoDAO import MedicamentoDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.MedicamentoCommand import InsertMedicamentoCommand, DeleteMedicamentoCommand

class MedicamentoService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_medicamentos(self) -> List[MedicamentoVO]:
        return MedicamentoDAO.get_all_medicamentos()
    
    def get_medicamento(self, id: int) -> MedicamentoVO | None:
        return MedicamentoDAO.get_medicamento(id)

    def insert_medicamento(self, vo: MedicamentoVO):
        with self.connection_factory() as connection:
            result = MedicamentoDAO.insert_medicamento(connection, vo)
            if result:
                vo.medicamento_id = result
                if self.undo_manager:
                    self.undo_manager.register(InsertMedicamentoCommand(vo))
            return result

    def delete_medicamento(self, id: int) -> None:
        vo = self.get_medicamento(id)
        if vo:
            MedicamentoDAO.delete_medicamento(id)
            if self.undo_manager:
                self.undo_manager.register(DeleteMedicamentoCommand(vo))
