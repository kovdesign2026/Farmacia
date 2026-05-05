from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.ClienteVO import ClienteVO
from model.peewee.Cliente import Cliente

class ClienteDAO:

    @staticmethod
    def get_all_clientes():
        """Retorna un generador que carga los clientes de forma perezosa (lazy loading)"""
        for p_c in Cliente.select().iterator():
            yield ClienteVO(
                cliente_id=p_c.cliente_id,
                nombre=p_c.nombre,
                dni=p_c.dni
            )
    
    @staticmethod
    def get_cliente(id: int) -> ClienteVO | None:
        p_c = Cliente.get_or_none(id)
        if p_c is None:
            return None
        return ClienteVO(
            cliente_id=p_c.cliente_id,
            nombre=p_c.nombre,
            dni=p_c.dni
        )

    @staticmethod
    def delete_cliente(id: int | None) -> None:
        Cliente.delete_by_id(id)

    @staticmethod
    def insert_cliente(connection: Sqlite3Connection,
                       cliente: ClienteVO) -> int | None:
        query_string = 'INSERT INTO cliente (nombre, dni) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (cliente.nombre, cliente.dni))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_cliente(connection: Sqlite3Connection,
                         cliente: ClienteVO) -> int | None:
        query_string = 'INSERT INTO cliente (cliente_id, nombre, dni) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (cliente.cliente_id, cliente.nombre, cliente.dni))
        return cursor.lastrowid
