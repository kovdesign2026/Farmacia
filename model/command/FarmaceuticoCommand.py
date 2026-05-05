from model.command.Command import Command
from model.vo.FarmaceuticoVO import FarmaceuticoVO
from model.dao.FarmaceuticoDAO import FarmaceuticoDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertFarmaceuticoCommand(Command):
    def __init__(self, farmaceutico: FarmaceuticoVO):
        self.farmaceutico = farmaceutico

    def undo(self, connection: Sqlite3Connection):
        if self.farmaceutico.farmaceutico_id:
            FarmaceuticoDAO.delete_farmaceutico(self.farmaceutico.farmaceutico_id)

    def redo(self, connection: Sqlite3Connection):
        if self.farmaceutico.farmaceutico_id:
            FarmaceuticoDAO.reinsert_farmaceutico(connection, self.farmaceutico)
        else:
            result = FarmaceuticoDAO.insert_farmaceutico(connection, self.farmaceutico)
            if result:
                self.farmaceutico.farmaceutico_id = result


class DeleteFarmaceuticoCommand(Command):
    def __init__(self, farmaceutico: FarmaceuticoVO):
        self.farmaceutico = farmaceutico

    def undo(self, connection: Sqlite3Connection):
        FarmaceuticoDAO.reinsert_farmaceutico(connection, self.farmaceutico)

    def redo(self, connection: Sqlite3Connection):
        FarmaceuticoDAO.delete_farmaceutico(self.farmaceutico.farmaceutico_id)
