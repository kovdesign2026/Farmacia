from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel

class Medicamento(BaseModel):
    medicamento_id = AutoField()
    nombre = CharField()
    dosis = FloatField()
