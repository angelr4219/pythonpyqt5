from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QDialog,
    QLineEdit, QFormLayout, QScrollArea, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from Gui.ToolTips import show_parameter_tooltip_persistent

class MaterialEditorWidget(QWidget):
    material_updated = pyqtSignal(int, dict)

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.edit_mode = False
        self.show_display = True

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top toolbar
        toolbar = QHBoxLayout()
        self.layout.addLayout(toolbar)

        self.present_btn = QPushButton("Present Materials")
        self.present_btn.clicked.connect(self.load_data)
        toolbar.addWidget(self.present_btn)

        self.add_btn = QPushButton("Add Material")
        self.add_btn.clicked.connect(self.add_material)
        toolbar.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Toggle Edit Mode")
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        toolbar.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Delete Last Material")
        self.delete_btn.clicked.connect(self.delete_last_material)
        toolbar.addWidget(self.delete_btn)

        self.display_btn = QPushButton("Toggle Display")
        self.display_btn.clicked.connect(self.toggle_display)
        toolbar.addWidget(self.display_btn)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.inner_widget = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner_widget.setLayout(self.inner_layout)
        self.scroll_area.setWidget(self.inner_widget)
        self.layout.addWidget(self.scroll_area)

        self.state_manager.file_loaded.connect(self.load_data)
        self.state_manager.set_unsaved_changes(True)
        self.load_data()

    def load_data(self):
        for i in reversed(range(self.inner_layout.count())):
            widget = self.inner_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        materials = self.state_manager.xml_manager.get_materials()
        for idx, material in enumerate(materials):
            box = QGroupBox(f"Material {idx + 1}")
            form = QFormLayout()
            for key, value in material.items():
                label = QLabel(key)
                input_field = QLineEdit(value)
                input_field.setReadOnly(not self.edit_mode)

                show_parameter_tooltip_persistent(input_field, key)
                input_field.editingFinished.connect(
                    lambda _, i=idx, k=key, w=input_field: self.material_updated.emit(i, {k: w.text()})
                )
                form.addRow(label, input_field)

            if self.show_display:
                box.setLayout(form)
                self.inner_layout.addWidget(box)

    def add_material(self):
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

    def delete_last_material(self):
        materials = self.state_manager.xml_manager.get_materials()
        if materials:
            self.state_manager.apply_change({"type": "delete_material", "index": len(materials) - 1})
            self.load_data()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.load_data()

    def toggle_display(self):
        self.show_display = not self.show_display
        self.load_data()

    def refresh(self):
        self.load_data()
