from typing import List
from peewee import prefetch
from sqlite3 import Cursor
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.FacturaVO import FacturaVO
from model.vo.ClienteVO import ClienteVO
from model.vo.FarmaceuticoVO import FarmaceuticoVO
from model.vo.VentaVO import VentaVO
from model.vo.MedicamentoVO import MedicamentoVO
from model.peewee.Factura import Factura
from model.peewee.Venta import Venta
from model.peewee.Cliente import Cliente
from model.peewee.Farmaceutico import Farmaceutico
from model.peewee.Medicamento import Medicamento

class FacturaDAO:

    @staticmethod
    def get_all_facturas():
        """Retorna un generador que carga las facturas de forma perezosa (lazy loading)"""
        # Usamos join para Cliente y Farmaceutico, y prefetch para Ventas (Eager Loading completo)
        query = Factura.select(Factura, Cliente, Farmaceutico).join(Cliente).switch(Factura).join(Farmaceutico).order_by(Factura.factura_id)
        facturas_with_ventas = prefetch(query, Venta.select(Venta, Medicamento).join(Medicamento))
        
        for p_i in facturas_with_ventas:
            cliente_vo = ClienteVO(
                cliente_id=p_i.cliente_id.cliente_id,
                nombre=p_i.cliente_id.nombre,
                dni=p_i.cliente_id.dni
            )
            farmaceutico_vo = FarmaceuticoVO(
                farmaceutico_id=p_i.farmaceutico_id.farmaceutico_id,
                dni=p_i.farmaceutico_id.dni,
                nombre=p_i.farmaceutico_id.nombre
            )
            
            ventas_vo = []
            # p_i.ventas ya está precargado por prefetch
            for pv in p_i.ventas:
                medicamento_vo = MedicamentoVO(
                    medicamento_id=pv.medicamento_id.medicamento_id,
                    nombre=pv.medicamento_id.nombre,
                    dosis=pv.medicamento_id.dosis
                )
                ventas_vo.append(VentaVO(
                    venta_id=pv.venta_id,
                    medicamento=medicamento_vo
                ))

            yield FacturaVO(
                factura_id=p_i.factura_id,
                farmaceutico=farmaceutico_vo,
                cliente=cliente_vo,
                ventas=ventas_vo
            )
    
    @staticmethod
    def get_factura(id: int) -> FacturaVO | None:
        p_i = Factura.get_or_none(id)
        if p_i is None:
            return None
        
        cliente_vo = ClienteVO(
            cliente_id=p_i.cliente_id.cliente_id,
            nombre=p_i.cliente_id.nombre,
            dni=p_i.cliente_id.dni
        )
        farmaceutico_vo = FarmaceuticoVO(
            farmaceutico_id=p_i.farmaceutico_id.farmaceutico_id,
            dni=p_i.farmaceutico_id.dni,
            nombre=p_i.farmaceutico_id.nombre
        )
        
        # Load associated ventas
        peewee_ventas = Venta.select().where(Venta.factura_id == id)
        ventas_vo = []
        for pv in peewee_ventas:
            medicamento_vo = MedicamentoVO(
                medicamento_id=pv.medicamento_id.medicamento_id,
                nombre=pv.medicamento_id.nombre,
                dosis=pv.medicamento_id.dosis
            )
            ventas_vo.append(VentaVO(
                venta_id=pv.venta_id,
                medicamento=medicamento_vo
            ))

        return FacturaVO(
            factura_id=p_i.factura_id,
            farmaceutico=farmaceutico_vo,
            cliente=cliente_vo,
            ventas=ventas_vo
        )

    @staticmethod
    def delete_factura(id: int | None) -> None:
        # Delete associated ventas first or rely on cascading (Peewee doesn't cascade by default on delete_by_id unless configured)
        Venta.delete().where(Venta.factura_id == id).execute()
        Factura.delete_by_id(id)

    @staticmethod
    def insert_factura(connection: Sqlite3Connection,
                       factura: FacturaVO) -> int | None:
        query_string = 'INSERT INTO factura (farmaceutico_id, cliente_id) VALUES (?, ?)'
        cursor: Cursor = connection.execute(query_string, (factura.farmaceutico.farmaceutico_id, factura.cliente.cliente_id))
        return cursor.lastrowid
    
    @staticmethod
    def reinsert_factura(connection: Sqlite3Connection,
                         factura: FacturaVO) -> int | None:
        query_string = 'INSERT INTO factura (factura_id, farmaceutico_id, cliente_id) VALUES (?, ?, ?)'
        cursor: Cursor = connection.execute(query_string, (factura.factura_id, factura.farmaceutico.farmaceutico_id, factura.cliente.cliente_id))
        return cursor.lastrowid


