from model.command.Command import Command
from model.vo.MedicamentoVO import MedicamentoVO
from model.dao.MedicamentoDAO import MedicamentoDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertMedicamentoCommand(Command):
    def __init__(self, medicamento: MedicamentoVO):
        self.medicamento = medicamento

    def undo(self, connection: Sqlite3Connection):
        if self.medicamento.medicamento_id:
            MedicamentoDAO.delete_medicamento(self.medicamento.medicamento_id)

    def redo(self, connection: Sqlite3Connection):
        if self.medicamento.medicamento_id:
            MedicamentoDAO.reinsert_medicamento(connection, self.medicamento)
        else:
            result = MedicamentoDAO.insert_medicamento(connection, self.medicamento)
            if result:
                self.medicamento.medicamento_id = result


class DeleteMedicamentoCommand(Command):
    def __init__(self, medicamento: MedicamentoVO):
        self.medicamento = medicamento

    def undo(self, connection: Sqlite3Connection):
        MedicamentoDAO.reinsert_medicamento(connection, self.medicamento)

    def redo(self, connection: Sqlite3Connection):
        MedicamentoDAO.delete_medicamento(self.medicamento.medicamento_id)
