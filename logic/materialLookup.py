# gui/material_lookup.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGroupBox, QDialog, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class MaterialLookupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def load_data(self, manager):
        self.manager = manager
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        materials = self.manager.get_materials()
        for i, mat in enumerate(materials):
            name = mat.find("name").attrib.get("value", "Unnamed")
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, m=mat, idx=i: self.edit_material(m, idx))
            self.layout.addWidget(btn)

    def edit_material(self, mat, index):
        dialog = EditableMaterialDialog(mat, self.manager, index, on_update=self.refresh)
        dialog.exec_()

    def refresh(self):
        # Reloads buttons (in case name changed)
        self.load_data(self.manager)

class EditableMaterialDialog(QDialog):
    def __init__(self, material, manager, index, on_update=None):
        super().__init__()
        self.setWindowTitle(f"Edit Material: {material.find('name').attrib.get('value', '')}")
        self.material = material
        self.manager = manager
        self.index = index
        self.on_update = on_update

        self.layout = QVBoxLayout()
        self.form = QFormLayout()
        self.fields = {}

        for k in material:
            if "value" in k.attrib:
                field = QLineEdit(k.attrib["value"])
                self.fields[k.tag] = field
                self.form.addRow(QLabel(f"{k.tag}:"), field)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_material)

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.save_btn)
        self.setLayout(self.layout)

    def save_material(self):
        for tag, field in self.fields.items():
            value = field.text()
            if self.material.find(tag) is not None:
                self.material.find(tag).set("value", value)
        if self.on_update:
            self.on_update()
        self.accept()
