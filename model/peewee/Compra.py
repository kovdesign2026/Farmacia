from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel
from model.peewee.Proveedor import Proveedor
from model.peewee.Medicamento import Medicamento

class Compra(BaseModel):
    compra_id = AutoField()
    proveedor_id = ForeignKeyField(Proveedor, backref='compras')
    medicamento_id = ForeignKeyField(Medicamento, backref='compras')
