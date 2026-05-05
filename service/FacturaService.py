from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.FacturaVO import FacturaVO
from model.dao.FacturaDAO import FacturaDAO
from model.dao.VentaDAO import VentaDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.FacturaCommand import InsertFacturaCommand, DeleteFacturaCommand

class FacturaService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_facturas(self) -> List[FacturaVO]:
        return FacturaDAO.get_all_facturas()
    
    def get_factura(self, id: int) -> FacturaVO | None:
        return FacturaDAO.get_factura(id)

    def insert_factura(self, factura: FacturaVO):
        with self.connection_factory() as connection:
            factura_id = FacturaDAO.insert_factura(connection, factura)
            # Insert associated ventas
            for venta in factura.ventas:
                VentaDAO.insert_venta(connection, venta, factura_id)
            
            if factura_id:
                factura.factura_id = factura_id
                if self.undo_manager:
                    self.undo_manager.register(InsertFacturaCommand(factura))
            
            return factura_id

    def delete_factura(self, id: int) -> None:
        vo = self.get_factura(id)
        if vo:
            FacturaDAO.delete_factura(id)
            if self.undo_manager:
                self.undo_manager.register(DeleteFacturaCommand(vo))
