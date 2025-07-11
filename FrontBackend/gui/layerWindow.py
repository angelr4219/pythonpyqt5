# gui/layer_window.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QWidget, QScrollArea
)
#testing againsdfgsdfg
class LayerWindow(QDialog):
    def __init__(self, layer_data, materials, callback, index):
        super().__init__()
        self.setWindowTitle(f"Edit Layer {index + 1}")
        self.callback = callback
        self.index = index
        test = "test"

        self.layout = QVBoxLayout()
        self.form = QFormLayout()

        self.name_input = QLineEdit(layer_data.get("name", ""))
        self.material_input = QComboBox()
        self.material_input.addItems(materials)
        self.material_input.setCurrentText(layer_data.get("materialType", ""))
        self.height_input = QLineEdit(layer_data.get("height", ""))
        self.density_input = QLineEdit(layer_data.get("panelDensity", ""))
        self.wave_type_input = QLineEdit(layer_data.get("localWaveCalcType", ""))

        self.form.addRow("Name:", self.name_input)
        self.form.addRow("Material:", self.material_input)
        self.form.addRow("Height:", self.height_input)
        self.form.addRow("Panel Density:", self.density_input)
        self.form.addRow("Wave Calc Type:", self.wave_type_input)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_changes)

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.save_btn)
        self.setLayout(self.layout)



    def save_changes(self):
        try:
            float(self.height_input.text())
            float(self.density_input.text())
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Height and Density must be numeric.")
            return

        updated = {
            "name": self.name_input.text(),
            "materialType": self.material_input.currentText(),
            "height": self.height_input.text(),
            "panelDensity": self.density_input.text(),
            "localWaveCalcType": self.wave_type_input.text(),
        }
        self.callback(self.index, updated)
        self.accept()
