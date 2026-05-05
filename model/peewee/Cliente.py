from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel

class Cliente(BaseModel):
    cliente_id = AutoField()
    nombre = CharField()
    dni = CharField(unique=True)
