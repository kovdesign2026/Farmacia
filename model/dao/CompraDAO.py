from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.CompraVO import CompraVO
from model.vo.ProveedorVO import ProveedorVO
from model.vo.MedicamentoVO import MedicamentoVO
from model.peewee.Compra import Compra
from model.peewee.Proveedor import Proveedor
from model.peewee.Medicamento import Medicamento

class CompraDAO:

    @staticmethod
    def get_all_compras():
        """Retorna un generador que carga las compras de forma perezosa (lazy loading)"""
        # Usamos join para cargar las relaciones de forma eficiente en una sola consulta
        query = Compra.select(Compra, Proveedor, Medicamento).join(Proveedor).switch(Compra).join(Medicamento)
        for p_i in query.iterator():
            proveedor_vo = ProveedorVO(
                proveedor_id=p_i.proveedor_id.proveedor_id,
                razon_social=p_i.proveedor_id.razon_social,
                nit=p_i.proveedor_id.nit
            )
            medicamento_vo = MedicamentoVO(
                medicamento_id=p_i.medicamento_id.medicamento_id,
                nombre=p_i.medicamento_id.nombre,
                dosis=p_i.medicamento_id.dosis
            )
            yield CompraVO(
                compra_id=p_i.compra_id,
                proveedor=proveedor_vo,
                medicamento=medicamento_vo
            )
    
    @staticmethod
    def get_compra(id: int) -> CompraVO | None:
        p_i = Compra.get_or_none(id)
        if p_i is None:
            return None
        
        proveedor_vo = ProveedorVO(
            proveedor_id=p_i.proveedor_id.proveedor_id,
            razon_social=p_i.proveedor_id.razon_social,
            nit=p_i.proveedor_id.nit
        )
        medicamento_vo = MedicamentoVO(
            medicamento_id=p_i.medicamento_id.medicamento_id,
            nombre=p_i.medicamento_id.nombre,
            dosis=p_i.medicamento_id.dosis
        )
        return CompraVO(
            compra_id=p_i.compra_id,
            proveedor=proveedor_vo,
            medicamento=medicamento_vo
        )

    @staticmethod
    def delete_compra(id: int | None) -> None:
        Compra.delete_by_id(id)

    @staticmethod
    def insert_compra(connection: Sqlite3Connection,
                      compra: CompraVO) -> int | None:
        query_string = 'INSERT INTO compra (proveedor_id, medicamento_id) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (compra.proveedor.proveedor_id, compra.medicamento.medicamento_id))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_compra(connection: Sqlite3Connection,
                        compra: CompraVO) -> int | None:
        query_string = 'INSERT INTO compra (compra_id, proveedor_id, medicamento_id) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (compra.compra_id, compra.proveedor.proveedor_id, compra.medicamento.medicamento_id))
        return cursor.lastrowid
