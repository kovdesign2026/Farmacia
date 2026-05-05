from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from controller.ClienteController import ClienteController
from model.vo.ClienteVO import ClienteVO


class ClienteWidget(QWidget):
    def __init__(self, controller: ClienteController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de clientes
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "DNI"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Cliente")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_cliente)
        btn_actualizar.clicked.connect(self.cargar_clientes)
        btn_eliminar.clicked.connect(self.eliminar_cliente)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_clientes()

    def cargar_clientes(self):
        self.tabla.setRowCount(0)
        clientes = self.controller.get_all_clientes()
        for cliente in clientes:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(cliente.cliente_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(cliente.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(cliente.dni))

    def agregar_cliente(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Cliente")
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Nombre:"))
        nombre_input = QLineEdit()
        layout.addWidget(nombre_input)
        
        layout.addWidget(QLabel("DNI:"))
        dni_input = QLineEdit()
        layout.addWidget(dni_input)
        
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("✓ Guardar")
        btn_cancelar = QPushButton("✕ Cancelar")
        btn_guardar.setMinimumHeight(35)
        btn_cancelar.setMinimumHeight(35)
        
        def guardar():
            nombre = nombre_input.text().strip()
            dni = dni_input.text().strip()
            if nombre and dni:
                try:
                    self.controller.insert_cliente(nombre, dni)
                    QMessageBox.information(self, "Éxito", "Cliente agregado correctamente")
                    dialog.accept()
                    self.cargar_clientes()
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

    def eliminar_cliente(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            cliente_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar este cliente?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_cliente(cliente_id)
                    self.cargar_clientes()
                    QMessageBox.information(self, "Éxito", "Cliente eliminado")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar")
