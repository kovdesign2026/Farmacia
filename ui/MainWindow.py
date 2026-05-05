from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt

from ui.ClienteWidget import ClienteWidget
from ui.MedicamentoWidget import MedicamentoWidget
from ui.FarmaceuticoWidget import FarmaceuticoWidget
from ui.ProveedorWidget import ProveedorWidget
from ui.CompraWidget import CompraWidget
from ui.FacturaWidget import FacturaWidget


class MainWindow(QMainWindow):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.history_controller = self.controllers["history"]
        self.init_ui()
        self.apply_styles()



    def init_ui(self):
        self.setWindowTitle("Sistema Integral de Farmacia")
        self.setGeometry(100, 100, 1200, 700)

        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar con botones Undo/Redo
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 10, 10, 10)
        
        btn_undo = QPushButton("Deshacer")
        btn_redo = QPushButton("Rehacer")
        
        btn_undo.setMaximumWidth(120)
        btn_redo.setMaximumWidth(120)
        btn_undo.setCursor(Qt.PointingHandCursor)
        btn_redo.setCursor(Qt.PointingHandCursor)
        
        btn_undo.clicked.connect(self.undo_action)
        btn_redo.clicked.connect(self.redo_action)
        
        toolbar_layout.addWidget(btn_undo)
        toolbar_layout.addWidget(btn_redo)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.tabBar().setExpanding(True)

        # Crear widgets y guardar referencias
        self.cliente_widget = ClienteWidget(self.controllers["cliente"])
        self.medicamento_widget = MedicamentoWidget(self.controllers["medicamento"])
        self.farmaceutico_widget = FarmaceuticoWidget(self.controllers["farmaceutico"])
        self.proveedor_widget = ProveedorWidget(self.controllers["proveedor"])
        self.compra_widget = CompraWidget(self.controllers["compra"])
        self.factura_widget = FacturaWidget(self.controllers["factura"])

        # Agregar cada widget como una pestaña
        tabs.addTab(self.cliente_widget, "Clientes")
        tabs.addTab(self.medicamento_widget, "Medicamentos")
        tabs.addTab(self.farmaceutico_widget, "Farmacéuticos")
        tabs.addTab(self.proveedor_widget, "Proveedores")
        tabs.addTab(self.compra_widget, "Compras")
        tabs.addTab(self.factura_widget, "Facturas")

        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def undo_action(self):
        self.history_controller.undo()
        self.refresh_all_widgets()

    def redo_action(self):
        self.history_controller.redo()
        self.refresh_all_widgets()

    def refresh_all_widgets(self):
        """Actualiza todos los widgets después de un undo/redo"""
        self.cliente_widget.cargar_clientes()
        self.medicamento_widget.cargar_medicamentos()
        self.farmaceutico_widget.cargar_farmaceuticos()
        self.proveedor_widget.cargar_proveedores()
        self.compra_widget.cargar_compras()
        self.factura_widget.cargar_facturas()

    def apply_styles(self):
        stylesheet = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #d0d0d0;
        }
        
        QTabBar::tab {
            background-color: #e8e8e8;
            color: #333333;
            padding: 8px 10px;
            border: 1px solid #c0c0c0;
            border-bottom: none;
            margin-right: 2px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #0066cc;
            border-bottom: 3px solid #0066cc;
        }
        
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        
        QPushButton {
            background-color: #0066cc;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }
        
        QPushButton:hover {
            background-color: #0052a3;
        }
        
        QPushButton:pressed {
            background-color: #003d7a;
        }
        
        QPushButton#deleteBtn {
            background-color: #dc3545;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #c82333;
        }
        
        QTableWidget {
            background-color: white;
            alternate-background-color: #f9f9f9;
            gridline-color: #e0e0e0;
            border: 1px solid #d0d0d0;
        }
        
        QTableWidget::item {
            padding: 5px;
            border: none;
        }
        
        QHeaderView::section {
            background-color: #f0f0f0;
            color: #333333;
            padding: 5px;
            border: none;
            border-right: 1px solid #d0d0d0;
            font-weight: bold;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            background-color: white;
            font-size: 11px;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #0066cc;
        }
        
        QLabel {
            color: #333333;
            font-weight: 500;
        }
        
        QDialog {
            background-color: #f5f5f5;
        }
        
        QMessageBox {
            background-color: #f5f5f5;
        }
        """
        self.setStyleSheet(stylesheet)
