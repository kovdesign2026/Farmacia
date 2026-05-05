import random
from DependencyContainer import DependencyContainer

def seed_db():
    print("Iniciando inyección de dependencias para poblar la base de datos...")
    container = DependencyContainer()
    
    # Controllers
    ctrl_cliente = container.controllers["cliente"]
    ctrl_medicamento = container.controllers["medicamento"]
    ctrl_farmaceutico = container.controllers["farmaceutico"]
    ctrl_proveedor = container.controllers["proveedor"]
    ctrl_compra = container.controllers["compra"]
    ctrl_factura = container.controllers["factura"]
    
    # Datos coherentes aleatorios
    nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofia", "Diego", "Marta"]
    apellidos = ["Perez", "Gomez", "Rodriguez", "Lopez", "Martinez", "Garcia", "Fernandez", "Ruiz", "Diaz", "Alvarez"]
    medicamentos_nombres = ["Paracetamol", "Ibuprofeno", "Amoxicilina", "Omeprazol", "Loratadina", "Diclofenaco", "Losartan", "Metformina"]
    razones_sociales = ["FarmaCorp", "MediSalud S.A.", "Laboratorios XYZ", "Distribuidora San Juan", "BioPharma"]
    
    print("Inyectando Clientes...")
    for _ in range(10):
        nombre_completo = f"{random.choice(nombres)} {random.choice(apellidos)}"
        dni = f"{random.randint(10000000, 99999999)}"
        ctrl_cliente.insert_cliente(nombre_completo, dni)
        
    print("Inyectando Medicamentos...")
    for med in medicamentos_nombres:
        dosis = round(random.uniform(50.0, 1000.0), 2)
        ctrl_medicamento.insert_medicamento(med, dosis)
        
    print("Inyectando Farmacéuticos...")
    for _ in range(5):
        nombre_completo = f"{random.choice(nombres)} {random.choice(apellidos)}"
        dni = f"{random.randint(10000000, 99999999)}"
        ctrl_farmaceutico.insert_farmaceutico(dni, nombre_completo)
        
    print("Inyectando Proveedores...")
    for prov in razones_sociales:
        nit = f"NIT-{random.randint(100000, 999999)}"
        ctrl_proveedor.insert_proveedor(prov, nit)
        
    # Refresh to get IDs
    clientes = list(ctrl_cliente.get_all_clientes())
    medicamentos = list(ctrl_medicamento.get_all_medicamentos())
    farmaceuticos = list(ctrl_farmaceutico.get_all_farmaceuticos())
    proveedores = list(ctrl_proveedor.get_all_proveedores())
    
    if proveedores and medicamentos:
        print("Inyectando Compras...")
        for _ in range(15):
            prov = random.choice(proveedores)
            med = random.choice(medicamentos)
            ctrl_compra.insert_compra(prov.proveedor_id, med.medicamento_id)
            
    if clientes and farmaceuticos and medicamentos:
        print("Inyectando Facturas...")
        for _ in range(10):
            cli = random.choice(clientes)
            farm = random.choice(farmaceuticos)
            num_meds = random.randint(1, 4)
            meds_seleccionados = [random.choice(medicamentos).medicamento_id for _ in range(num_meds)]
            ctrl_factura.insert_factura(cli.cliente_id, farm.farmaceutico_id, meds_seleccionados)
            
    print("¡Base de datos inyectada con éxito!")

if __name__ == "__main__":
    seed_db()
