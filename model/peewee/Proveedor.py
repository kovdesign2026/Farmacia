from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel

class Proveedor(BaseModel):
    proveedor_id = AutoField()
    razon_social = CharField()
    nit = CharField(unique=True)
