from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QSpinBox, 
                           QMessageBox, QLineEdit, QHeaderView)
from PyQt5.QtCore import Qt
from controller.FacturaController import FacturaController


class FacturaWidget(QWidget):
    def __init__(self, controller: FacturaController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de facturas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Cliente", "Farmacéutico", "Medicamentos"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Crear Nueva Factura")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_factura)
        btn_actualizar.clicked.connect(self.cargar_facturas)
        btn_eliminar.clicked.connect(self.eliminar_factura)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_facturas()

    def cargar_facturas(self):
        self.tabla.setRowCount(0)
        facturas = self.controller.get_all_facturas()
        for factura in facturas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(factura.factura_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(factura.cliente.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(factura.farmaceutico.nombre))
            
            medicamentos = ", ".join([v.medicamento.nombre for v in factura.ventas])
            self.tabla.setItem(row, 3, QTableWidgetItem(medicamentos))

    def agregar_factura(self):
        from PyQt5.QtWidgets import QComboBox, QListWidget, QAbstractItemView
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Nueva Factura")
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Seleccionar Cliente:"))
        cli_combo = QComboBox()
        clientes = list(self.controller.get_all_clientes())
        for c in clientes:
            cli_combo.addItem(c.nombre, c.cliente_id)
        layout.addWidget(cli_combo)
        
        layout.addWidget(QLabel("Seleccionar Farmacéutico:"))
        far_combo = QComboBox()
        farmaceuticos = list(self.controller.get_all_farmaceuticos())
        for f in farmaceuticos:
            far_combo.addItem(f.nombre, f.farmaceutico_id)
        layout.addWidget(far_combo)
        
        layout.addWidget(QLabel("Seleccionar Medicamentos (Ctrl+Click para varios):"))
        med_list = QListWidget()
        med_list.setSelectionMode(QAbstractItemView.MultiSelection)
        medicamentos = list(self.controller.get_all_medicamentos())
        for m in medicamentos:
            from PyQt5.QtWidgets import QListWidgetItem
            item = QListWidgetItem(m.nombre)
            item.setData(Qt.UserRole, m.medicamento_id)
            med_list.addItem(item)
        layout.addWidget(med_list)
        
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("✓ Guardar")
        btn_cancelar = QPushButton("✕ Cancelar")
        btn_guardar.setMinimumHeight(35)
        btn_cancelar.setMinimumHeight(35)
        
        def guardar():
            if cli_combo.currentData() is None or far_combo.currentData() is None:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un cliente y un farmacéutico")
                return
                
            cli_id = cli_combo.currentData()
            far_id = far_combo.currentData()
            selected_items = med_list.selectedItems()
            
            med_ids = [item.data(Qt.UserRole) for item in selected_items]
            
            if not med_ids:
                QMessageBox.warning(self, "Validación", "Debe seleccionar al menos un medicamento")
                return
            
            try:
                if self.controller.insert_factura(cli_id, far_id, med_ids):
                    QMessageBox.information(self, "Éxito", "Factura creada correctamente")
                    dialog.accept()
                    self.cargar_facturas()
                else:
                    QMessageBox.critical(self, "Error", "Cliente, Farmacéutico o Medicamento no encontrado")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear: {str(e)}")
        
        btn_guardar.clicked.connect(guardar)
        btn_cancelar.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def eliminar_factura(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            factura_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar esta factura?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_factura(factura_id)
                    self.cargar_facturas()
                    QMessageBox.information(self, "Éxito", "Factura eliminada")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione una factura para eliminar")
