from model.command.Command import Command
from model.vo.FacturaVO import FacturaVO
from model.dao.FacturaDAO import FacturaDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertFacturaCommand(Command):
    def __init__(self, factura: FacturaVO):
        self.factura = factura

    def undo(self, connection: Sqlite3Connection):
        if self.factura.factura_id:
            FacturaDAO.delete_factura(self.factura.factura_id)

    def redo(self, connection: Sqlite3Connection):
        if self.factura.factura_id:
            FacturaDAO.reinsert_factura(connection, self.factura)
        else:
            result = FacturaDAO.insert_factura(connection, self.factura)
            if result:
                self.factura.factura_id = result


class DeleteFacturaCommand(Command):
    def __init__(self, factura: FacturaVO):
        self.factura = factura

    def undo(self, connection: Sqlite3Connection):
        FacturaDAO.reinsert_factura(connection, self.factura)

    def redo(self, connection: Sqlite3Connection):
        FacturaDAO.delete_factura(self.factura.factura_id)
