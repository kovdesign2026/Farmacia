from typing import List
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.MedicamentoVO import MedicamentoVO
from model.peewee.Medicamento import Medicamento

class MedicamentoDAO:

    @staticmethod
    def get_all_medicamentos():
        """Retorna un generador que carga los medicamentos de forma perezosa (lazy loading)"""
        for p_i in Medicamento.select().iterator():
            yield MedicamentoVO(
                medicamento_id=p_i.medicamento_id,
                nombre=p_i.nombre,
                dosis=p_i.dosis
            )
    
    @staticmethod
    def get_medicamento(id: int) -> MedicamentoVO | None:
        p_i = Medicamento.get_or_none(id)
        if p_i is None:
            return None
        return MedicamentoVO(
            medicamento_id=p_i.medicamento_id,
            nombre=p_i.nombre,
            dosis=p_i.dosis
        )

    @staticmethod
    def delete_medicamento(id: int | None) -> None:
        Medicamento.delete_by_id(id)

    @staticmethod
    def insert_medicamento(connection: Sqlite3Connection,
                           medicamento: MedicamentoVO) -> int | None:
        query_string = 'INSERT INTO medicamento (nombre, dosis) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (medicamento.nombre, medicamento.dosis))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_medicamento(connection: Sqlite3Connection,
                             medicamento: MedicamentoVO) -> int | None:
        query_string = 'INSERT INTO medicamento (medicamento_id, nombre, dosis) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (medicamento.medicamento_id, medicamento.nombre, medicamento.dosis))
        return cursor.lastrowid
