from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from controller.ProveedorController import ProveedorController


class ProveedorWidget(QWidget):
    def __init__(self, controller: ProveedorController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de proveedores
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Razón Social", "NIT"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Proveedor")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_proveedor)
        btn_actualizar.clicked.connect(self.cargar_proveedores)
        btn_eliminar.clicked.connect(self.eliminar_proveedor)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_proveedores()

    def cargar_proveedores(self):
        self.tabla.setRowCount(0)
        proveedores = self.controller.get_all_proveedores()
        for prov in proveedores:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(prov.proveedor_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(prov.razon_social))
            self.tabla.setItem(row, 2, QTableWidgetItem(prov.nit))

    def agregar_proveedor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Proveedor")
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Razón Social:"))
        razon_input = QLineEdit()
        layout.addWidget(razon_input)
        
        layout.addWidget(QLabel("NIT:"))
        nit_input = QLineEdit()
        layout.addWidget(nit_input)
        
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("✓ Guardar")
        btn_cancelar = QPushButton("✕ Cancelar")
        btn_guardar.setMinimumHeight(35)
        btn_cancelar.setMinimumHeight(35)
        
        def guardar():
            razon = razon_input.text().strip()
            nit = nit_input.text().strip()
            if razon and nit:
                try:
                    self.controller.insert_proveedor(razon, nit)
                    QMessageBox.information(self, "Éxito", "Proveedor agregado correctamente")
                    dialog.accept()
                    self.cargar_proveedores()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al agregar: {str(e)}")
            else:
                QMessageBox.warning(self, "Validación", "Todos los campos son requeridos")
        
        btn_guardar.clicked.connect(guardar)
        btn_cancelar.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def eliminar_proveedor(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            prov_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar este proveedor?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_proveedor(prov_id)
                    self.cargar_proveedores()
                    QMessageBox.information(self, "Éxito", "Proveedor eliminado")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un proveedor para eliminar")
