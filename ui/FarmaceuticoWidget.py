from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from controller.FarmaceuticoController import FarmaceuticoController


class FarmaceuticoWidget(QWidget):
    def __init__(self, controller: FarmaceuticoController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de farmacéuticos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "DNI"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Farmacéutico")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_farmaceutico)
        btn_actualizar.clicked.connect(self.cargar_farmaceuticos)
        btn_eliminar.clicked.connect(self.eliminar_farmaceutico)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_farmaceuticos()

    def cargar_farmaceuticos(self):
        self.tabla.setRowCount(0)
        farmaceuticos = self.controller.get_all_farmaceuticos()
        for far in farmaceuticos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(far.farmaceutico_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(far.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(far.dni))

    def agregar_farmaceutico(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Farmacéutico")
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
                    self.controller.insert_farmaceutico(dni, nombre)
                    QMessageBox.information(self, "Éxito", "Farmacéutico agregado correctamente")
                    dialog.accept()
                    self.cargar_farmaceuticos()
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

    def eliminar_farmaceutico(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            far_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar este farmacéutico?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_farmaceutico(far_id)
                    self.cargar_farmaceuticos()
                    QMessageBox.information(self, "Éxito", "Farmacéutico eliminado")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un farmacéutico para eliminar")
