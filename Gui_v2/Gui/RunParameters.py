from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QDialog, QLineEdit, QFormLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal
from Gui.ToolTips import setup_tooltips

class RunParameterWidget(QWidget):
    Parameter_updated = pyqtSignal(int, dict)

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.add_button = QPushButton("Add Material")
        self.add_button.clicked.connect(self.add_material)
        self.layout.addWidget(self.add_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.inner_widget = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner_widget.setLayout(self.inner_layout)
        self.scroll_area.setWidget(self.inner_widget)
        self.layout.addWidget(self.scroll_area)

        self.state_manager.file_loaded.connect(self.load_data)

    def load_data(self):
        self.inner_layout.setSpacing(10)
        for i in reversed(range(self.inner_layout.count())):
            self.inner_layout.itemAt(i).widget().setParent(None)

        materials = self.state_manager.xml_manager.get_materials()
        for idx, material in enumerate(materials):
            box = QGroupBox(f"Material {idx + 1}")
            form = QFormLayout()
            for key, value in material.items():
                label = QLabel(key)
                input_field = QLineEdit(value)
                setup_tooltips(input_field, key)
                input_field.editingFinished.connect(
                    lambda _, i=idx, k=key, w=input_field: self.material_updated.emit(i, {k: w.text()})
                )
                form.addRow(label, input_field)
            box.setLayout(form)
            self.inner_layout.addWidget(box)

    def add_Parameter(self):
        default_material = {
            "name": "NewMaterial",
            "dielectricConstant": "1.0",
            "effectiveMass_x": "0.1",
            "effectiveMass_y": "0.1",
            "effectiveMass_z": "0.1",
            "bandShift": "0.0",
            "backgroundDopingDensity": "0"
        }
        self.state_manager.apply_change({"type": "add_material", "data": default_material})
        self.load_data()

    def refresh(self):
        self.load_data()
