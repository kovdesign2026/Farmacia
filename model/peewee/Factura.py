from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel
from model.peewee.Farmaceutico import Farmaceutico
from model.peewee.Cliente import Cliente

class Factura(BaseModel):
    factura_id = AutoField()
    farmaceutico_id = ForeignKeyField(Farmaceutico, backref='facturas')
    cliente_id = ForeignKeyField(Cliente, backref='facturas')
