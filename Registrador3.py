# -*- coding: utf-8 -*-
"""
Registro para Farmacia (PySide6)
--------------------------------
Aplicación de escritorio para registrar medicamentos.
Incluye: QApplication, QWidget, QMainWindow, QDialog, QLabel,
QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout,
QGridLayout, QFormLayout, QCheckBox, QRadioButton y QComboBox.
Tema: rosado suave (tonos pastel, nada estridente).
Creado por Jhudith Romero - 2026
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QCheckBox,
    QRadioButton,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt


# ---------------------------------------------------------------------------
# Paleta de color rosado suave
# ---------------------------------------------------------------------------
COLOR_FONDO = "#FBEEEF"       # rosado muy claro (fondo general)
COLOR_PANEL = "#F6DEE3"       # rosado pastel (panel lateral)
COLOR_ACENTO = "#D9A5B3"      # rosado medio (bordes / acentos)
COLOR_BOTON = "#E4B7C2"       # rosado suave (botones)
COLOR_BOTON_HOVER = "#D9A0B0" # hover de botones
COLOR_TEXTO = "#6B4B57"       # guinda suave (texto)
COLOR_BLANCO = "#FFF9FA"      # blanco rosado (campos)

ESTILO = f"""
QMainWindow, QDialog {{
    background-color: {COLOR_FONDO};
}}
QWidget {{
    color: {COLOR_TEXTO};
    font-size: 13px;
}}
QLabel#titulo {{
    font-size: 18px;
    font-weight: bold;
    color: {COLOR_TEXTO};
    background-color: {COLOR_PANEL};
    padding: 10px;
    border-radius: 8px;
}}
QLineEdit, QTextEdit, QComboBox {{
    background-color: {COLOR_BLANCO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 5px;
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 2px solid {COLOR_BOTON_HOVER};
}}
QPushButton {{
    background-color: {COLOR_BOTON};
    color: {COLOR_TEXTO};
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLOR_BOTON_HOVER};
}}
QCheckBox, QRadioButton {{
    spacing: 6px;
}}
QTableWidget {{
    background-color: {COLOR_BLANCO};
    alternate-background-color: {COLOR_PANEL};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    gridline-color: {COLOR_PANEL};
}}
QHeaderView::section {{
    background-color: {COLOR_BOTON};
    color: {COLOR_TEXTO};
    padding: 6px;
    border: none;
    font-weight: bold;
}}
"""


# ---------------------------------------------------------------------------
# QDialog: ventana para registrar un proveedor
# ---------------------------------------------------------------------------
class DialogoProveedor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar proveedor")
        self.setMinimumWidth(420)

        titulo = QLabel("Datos del proveedor")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        # QLineEdit para los datos del proveedor
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre de la farmacéutica")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("Teléfono de contacto")
        self.txt_correo = QLineEdit()
        self.txt_correo.setPlaceholderText("correo@ejemplo.com")

        # QCheckBox y QRadioButton
        self.chk_distribuidor = QCheckBox("Es distribuidor autorizado")
        self.chk_distribuidor.setChecked(True)

        self.rb_nacional = QRadioButton("Nacional")
        self.rb_internacional = QRadioButton("Internacional")
        self.rb_nacional.setChecked(True)

        # QComboBox
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Mayorista", "Minorista", "Laboratorio"])

        # QTextEdit para notas
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Notas adicionales...")
        self.txt_notas.setMaximumHeight(80)

        # QFormLayout para organizar el formulario
        form = QFormLayout()
        form.addRow("Nombre:", self.txt_nombre)
        form.addRow("Teléfono:", self.txt_telefono)
        form.addRow("Correo:", self.txt_correo)
        form.addRow("Tipo:", self.cmb_tipo)
        form.addRow("Origen:", self.rb_nacional)
        form.addRow("", self.rb_internacional)
        form.addRow("", self.chk_distribuidor)
        form.addRow("Notas:", self.txt_notas)

        # QPushButton del diálogo
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        fila_botones = QHBoxLayout()
        fila_botones.addStretch()
        fila_botones.addWidget(self.btn_cancelar)
        fila_botones.addWidget(self.btn_guardar)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addLayout(fila_botones)
        self.setLayout(layout)

    def datos(self):
        """Devuelve un diccionario con los datos capturados."""
        return {
            "nombre": self.txt_nombre.text(),
            "telefono": self.txt_telefono.text(),
            "correo": self.txt_correo.text(),
            "tipo": self.cmb_tipo.currentText(),
            "origen": "Nacional" if self.rb_nacional.isChecked() else "Internacional",
            "autorizado": self.chk_distribuidor.isChecked(),
            "notas": self.txt_notas.toPlainText(),
        }


# ---------------------------------------------------------------------------
# QMainWindow: ventana principal
# ---------------------------------------------------------------------------
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farmacia - Registro de Medicamentos")
        self.resize(960, 640)

        central = QWidget()
        self.setCentralWidget(central)

        titulo = QLabel("Registro de Medicamentos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        # ---------------- Pie de página ----------------
        pie = QLabel("Creado por Jhudith Romero - 2026")
        pie.setAlignment(Qt.AlignCenter)
        pie.setStyleSheet(
            f"background-color: {COLOR_PANEL}; color: {COLOR_TEXTO}; "
            "border-radius: 8px; padding: 6px; font-style: italic;"
        )

        # ---------------- Panel del formulario ----------------
        panel = QWidget()
        panel.setMaximumWidth(400)

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej. Paracetamol")
        self.txt_dosis = QLineEdit()
        self.txt_dosis.setPlaceholderText("Ej. 500 mg")
        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Ej. 45.50")

        self.cmb_categoria = QComboBox()
        self.cmb_categoria.addItems([
            "Analgésico", "Antibiótico", "Antihistamínico",
            "Antiinflamatorio", "Vitaminas", "Otro",
        ])

        self.cmb_presentacion = QComboBox()
        self.cmb_presentacion.addItems(["Tabletas", "Jarabe", "Cápsula", "Inyección", "Crema"])

        self.chk_receta = QCheckBox("Requiere receta médica")
        self.chk_stock = QCheckBox("Disponible en stock")
        self.chk_stock.setChecked(True)

        self.rb_oral = QRadioButton("Vía oral")
        self.rb_inyectable = QRadioButton("Inyectable")
        self.rb_topica = QRadioButton("Tópica")
        self.rb_oral.setChecked(True)

        self.txt_obs = QTextEdit()
        self.txt_obs.setPlaceholderText("Observaciones o indicaciones...")
        self.txt_obs.setMaximumHeight(90)

        # QGridLayout: reparte los campos en una cuadrícula
        grid = QGridLayout()
        grid.addWidget(QLabel("Nombre:"), 0, 0)
        grid.addWidget(self.txt_nombre, 0, 1)
        grid.addWidget(QLabel("Dosis:"), 1, 0)
        grid.addWidget(self.txt_dosis, 1, 1)
        grid.addWidget(QLabel("Precio:"), 2, 0)
        grid.addWidget(self.txt_precio, 2, 1)
        grid.addWidget(QLabel("Categoría:"), 3, 0)
        grid.addWidget(self.cmb_categoria, 3, 1)
        grid.addWidget(QLabel("Presentación:"), 4, 0)
        grid.addWidget(self.cmb_presentacion, 4, 1)
        grid.addWidget(self.chk_receta, 5, 0, 1, 2)
        grid.addWidget(self.chk_stock, 6, 0, 1, 2)
        grid.addWidget(self.rb_oral, 7, 0)
        grid.addWidget(self.rb_inyectable, 7, 1)
        grid.addWidget(self.rb_topica, 8, 0)
        grid.addWidget(QLabel("Observaciones:"), 9, 0, 1, 2)
        grid.addWidget(self.txt_obs, 10, 0, 1, 2)

        self.btn_agregar = QPushButton("Agregar registro")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_agregar.clicked.connect(self.agregar_registro)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

        fila_botones = QHBoxLayout()
        fila_botones.addWidget(self.btn_agregar)
        fila_botones.addWidget(self.btn_limpiar)

        layout_panel = QVBoxLayout()
        layout_panel.addLayout(grid)
        layout_panel.addLayout(fila_botones)
        panel.setLayout(layout_panel)

        # ---------------- Tabla de registros ----------------
        self.tabla = QTableWidget(0, 6)
        self.tabla.setHorizontalHeaderLabels(
            ["Nombre", "Dosis", "Categoría", "Presentación", "Precio", "Receta"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setAlternatingRowColors(True)

        # ---------------- Botones laterales ----------------
        self.btn_proveedor = QPushButton("Registrar proveedor")
        self.btn_proveedor.clicked.connect(self.abrir_dialogo_proveedor)
        self.btn_resumen = QPushButton("Mostrar resumen")
        self.btn_resumen.clicked.connect(self.mostrar_resumen)

        botones_laterales = QVBoxLayout()
        botones_laterales.addWidget(self.btn_proveedor)
        botones_laterales.addWidget(self.btn_resumen)
        botones_laterales.addStretch()

        # QTextEdit con notas generales (registro sencillo)
        self.txt_registro = QTextEdit()
        self.txt_registro.setReadOnly(True)
        self.txt_registro.setPlaceholderText("Aquí aparecerá el historial...")
        self.txt_registro.setMaximumHeight(140)

        # ---------------- Layout principal ----------------
        derecha = QVBoxLayout()
        derecha.addWidget(QLabel("Medicamentos registrados:"))
        derecha.addWidget(self.tabla)
        derecha.addWidget(self.txt_registro)

        contenido = QHBoxLayout()
        contenido.addWidget(panel)
        contenido.addLayout(derecha)
        contenido.addLayout(botones_laterales)

        layout_central = QVBoxLayout()
        layout_central.addWidget(titulo)
        layout_central.addLayout(contenido)
        layout_central.addWidget(pie)
        central.setLayout(layout_central)

    # ------------------------- Métodos -------------------------
    def agregar_registro(self):
        nombre = self.txt_nombre.text().strip()
        dosis = self.txt_dosis.text().strip()
        precio = self.txt_precio.text().strip()

        if not nombre or not dosis or not precio:
            QMessageBox.warning(self, "Datos incompletos",
                                "Completa nombre, dosis y precio.")
            return

        via = ("Oral" if self.rb_oral.isChecked()
               else "Inyectable" if self.rb_inyectable.isChecked()
               else "Tópica")
        receta = "Sí" if self.chk_receta.isChecked() else "No"

        fila = self.tabla.rowCount()
        self.tabla.insertRow(fila)
        self.tabla.setItem(fila, 0, QTableWidgetItem(nombre))
        self.tabla.setItem(fila, 1, QTableWidgetItem(dosis))
        self.tabla.setItem(fila, 2, QTableWidgetItem(self.cmb_categoria.currentText()))
        self.tabla.setItem(fila, 3, QTableWidgetItem(self.cmb_presentacion.currentText()))
        self.tabla.setItem(fila, 4, QTableWidgetItem(precio))
        self.tabla.setItem(fila, 5, QTableWidgetItem(receta))

        self.txt_registro.append(
            f"• {nombre} ({dosis}) - {self.cmb_categoria.currentText()}, "
            f"{self.cmb_presentacion.currentText()}, vía {via}, ${precio}, "
            f"receta: {receta}, stock: {'Sí' if self.chk_stock.isChecked() else 'No'}"
        )

        if self.txt_obs.toPlainText().strip():
            self.txt_registro.append(f"  Obs: {self.txt_obs.toPlainText().strip()}")

        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.txt_nombre.clear()
        self.txt_dosis.clear()
        self.txt_precio.clear()
        self.txt_obs.clear()
        self.chk_receta.setChecked(False)
        self.chk_stock.setChecked(True)
        self.rb_oral.setChecked(True)
        self.cmb_categoria.setCurrentIndex(0)
        self.cmb_presentacion.setCurrentIndex(0)

    def abrir_dialogo_proveedor(self):
        dialogo = DialogoProveedor(self)
        if dialogo.exec() == QDialog.Accepted:
            datos = dialogo.datos()
            if datos["nombre"]:
                self.txt_registro.append(
                    f"• Proveedor: {datos['nombre']} ({datos['tipo']}, "
                    f"{datos['origen']}) - {datos['telefono']}"
                )

    def mostrar_resumen(self):
        total = self.tabla.rowCount()
        QMessageBox.information(
            self, "Resumen",
            f"Hay {total} medicamento(s) registrado(s) en la farmacia."
        )


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ESTILO)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())
