from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel
from model.peewee.Factura import Factura
from model.peewee.Medicamento import Medicamento

class Venta(BaseModel):
    venta_id = AutoField()
    factura_id = ForeignKeyField(Factura, backref='ventas')
    medicamento_id = ForeignKeyField(Medicamento, backref='ventas')
