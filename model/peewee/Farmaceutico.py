from peewee import * # type: ignore
from model.peewee.BaseModel import BaseModel

class Farmaceutico(BaseModel):
    farmaceutico_id = AutoField()
    dni = CharField(unique=True)
    nombre = CharField()
