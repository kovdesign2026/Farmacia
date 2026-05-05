from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.VentaVO import VentaVO
from model.vo.MedicamentoVO import MedicamentoVO
from model.peewee.Venta import Venta

class VentaDAO:

    @staticmethod
    def get_all_ventas() -> List[VentaVO]:
        peewee_items = Venta.select()
        items = []
        for p_i in peewee_items:
            medicamento_vo = MedicamentoVO(
                medicamento_id=p_i.medicamento_id.medicamento_id,
                nombre=p_i.medicamento_id.nombre,
                dosis=p_i.medicamento_id.dosis
            )
            items.append(VentaVO(
                venta_id=p_i.venta_id,
                medicamento=medicamento_vo
            ))
        return items
    
    @staticmethod
    def get_venta(id: int) -> VentaVO | None:
        p_i = Venta.get_or_none(id)
        if p_i is None:
            return None
        
        medicamento_vo = MedicamentoVO(
            medicamento_id=p_i.medicamento_id.medicamento_id,
            nombre=p_i.medicamento_id.nombre,
            dosis=p_i.medicamento_id.dosis
        )
        return VentaVO(
            venta_id=p_i.venta_id,
            medicamento=medicamento_vo
        )

    @staticmethod
    def delete_venta(id: int | None) -> None:
        Venta.delete_by_id(id)

    @staticmethod
    def insert_venta(connection: Sqlite3Connection,
                     venta: VentaVO,
                     factura_id: int) -> int | None:
        query_string = 'INSERT INTO venta (factura_id, medicamento_id) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (factura_id, venta.medicamento.medicamento_id))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_venta(connection: Sqlite3Connection,
                       venta: VentaVO,
                       factura_id: int) -> int | None:
        query_string = 'INSERT INTO venta (venta_id, factura_id, medicamento_id) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (venta.venta_id, factura_id, venta.medicamento.medicamento_id))
        return cursor.lastrowid
