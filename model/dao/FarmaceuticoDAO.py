from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.FarmaceuticoVO import FarmaceuticoVO
from model.peewee.Farmaceutico import Farmaceutico

class FarmaceuticoDAO:

    @staticmethod
    def get_all_farmaceuticos():
        """Retorna un generador que carga los farmacéuticos de forma perezosa (lazy loading)"""
        for p_i in Farmaceutico.select().iterator():
            yield FarmaceuticoVO(
                farmaceutico_id=p_i.farmaceutico_id,
                dni=p_i.dni,
                nombre=p_i.nombre
            )
    
    @staticmethod
    def get_farmaceutico(id: int) -> FarmaceuticoVO | None:
        p_i = Farmaceutico.get_or_none(id)
        if p_i is None:
            return None
        return FarmaceuticoVO(
            farmaceutico_id=p_i.farmaceutico_id,
            dni=p_i.dni,
            nombre=p_i.nombre
        )

    @staticmethod
    def delete_farmaceutico(id: int | None) -> None:
        Farmaceutico.delete_by_id(id)

    @staticmethod
    def insert_farmaceutico(connection: Sqlite3Connection,
                            farmaceutico: FarmaceuticoVO) -> int | None:
        query_string = 'INSERT INTO farmaceutico (dni, nombre) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (farmaceutico.dni, farmaceutico.nombre))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_farmaceutico(connection: Sqlite3Connection,
                              farmaceutico: FarmaceuticoVO) -> int | None:
        query_string = 'INSERT INTO farmaceutico (farmaceutico_id, dni, nombre) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (farmaceutico.farmaceutico_id, farmaceutico.dni, farmaceutico.nombre))
        return cursor.lastrowid
