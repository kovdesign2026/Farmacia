from model.peewee.BaseModel import db
from model.peewee.Cliente import Cliente
from model.peewee.Farmaceutico import Farmaceutico
from model.peewee.Medicamento import Medicamento
from model.peewee.Factura import Factura
from model.peewee.Venta import Venta
from model.peewee.Proveedor import Proveedor
from model.peewee.Compra import Compra

def init_db():
    print("Creando tablas en la base de datos...")
    db.connect()
    db.create_tables([
        Cliente, 
        Farmaceutico, 
        Medicamento, 
        Factura, 
        Venta, 
        Proveedor, 
        Compra
    ])
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    init_db()
