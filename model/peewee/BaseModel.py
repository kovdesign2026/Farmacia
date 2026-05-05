from peewee import * # type: ignore
from datetime import datetime

db = SqliteDatabase("db/farmacia.db")

class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = db