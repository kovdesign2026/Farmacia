from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.ProveedorVO import ProveedorVO
from model.peewee.Proveedor import Proveedor

class ProveedorDAO:

    @staticmethod
    def get_all_proveedores():
        """Retorna un generador que carga los proveedores de forma perezosa (lazy loading)"""
        for p_i in Proveedor.select().iterator():
            yield ProveedorVO(
                proveedor_id=p_i.proveedor_id,
                razon_social=p_i.razon_social,
                nit=p_i.nit
            )
    
    @staticmethod
    def get_proveedor(id: int) -> ProveedorVO | None:
        p_i = Proveedor.get_or_none(id)
        if p_i is None:
            return None
        return ProveedorVO(
            proveedor_id=p_i.proveedor_id,
            razon_social=p_i.razon_social,
            nit=p_i.nit
        )

    @staticmethod
    def delete_proveedor(id: int | None) -> None:
        Proveedor.delete_by_id(id)

    @staticmethod
    def insert_proveedor(connection: Sqlite3Connection,
                         proveedor: ProveedorVO) -> int | None:
        query_string = 'INSERT INTO proveedor (razon_social, nit) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (proveedor.razon_social, proveedor.nit))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_proveedor(connection: Sqlite3Connection,
                           proveedor: ProveedorVO) -> int | None:
        query_string = 'INSERT INTO proveedor (proveedor_id, razon_social, nit) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (proveedor.proveedor_id, proveedor.razon_social, proveedor.nit))
        return cursor.lastrowid
