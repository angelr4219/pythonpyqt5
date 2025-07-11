# gui/material_lookup.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGroupBox, QDialog, QLineEdit, QFormLayout, QMessageBox,QCheckBox, QScrollArea
)
from PyQt5.QtCore import Qt
from logic.ParameterDocs import parameter_docs

from logic.tooltipManager import show_parameter_tooltip
class MaterialLookupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.add_button = QPushButton("Add Material")
        self.add_button.clicked.connect(self.add_material)
        self._layout.addWidget(self.add_button)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self._layout.addWidget(self.scroll_area)

    def load_data(self, manager):
        self.manager = manager
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        materials = self.manager.get_materials()
        for idx, mat in enumerate(materials):
            name = mat.find("name").attrib.get("value", "Unnamed")
            box = QGroupBox(f"Material: {name}")
            inner_layout = QVBoxLayout()

            for elem in mat:
                if elem.tag == "name":
                    continue
                tag = elem.tag
                value = elem.attrib.get("value", "")
                line = QLabel(f"{tag}: {value}")
                inner_layout.addWidget(line)

            box.setLayout(inner_layout)
            self.scroll_layout.addWidget(box)

    def add_material(self):
        ml = self.root.find("./MaterialList")
        if ml is None:
            print("[x] No <MaterialList> found in XML.")
            return
        new_elem = ET.Element("Material")
        for key, value in material_dict.items():
            sub_elem = ET.Element(key)
            sub_elem.set("value", value)
            new_elem.append(sub_elem)
        ml.append(new_elem)
        print("[ok] Added new material.")

    def refresh(self):
        self.load_data(self.manager)

class EditableMaterialDialog(QDialog):
    def __init__(self, material, manager, index, on_update=None):
        super().__init__()
        self.setWindowTitle("Add Material" if material is None else f"Edit Material: {material.find('name').attrib.get('value', '')}")
        self.material = material
        self.manager = manager
        self.index = index
        self.on_update = on_update

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = QFormLayout()
        self.fields = {}

        tags = ["name", "dielectricConstant", "effectiveMass_x", "effectiveMass_y", "effectiveMass_z", "bandShift", "backgroundDopingDensity"]
        for tag in tags:
            default_value = material.find(tag).attrib.get("value", "") if material is not None else ""
            field = QLineEdit(default_value)
            self.fields[tag] = field
            self.form.addRow(QLabel(f"{tag}"), field)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_material)

        layout.addLayout(self.form)
        layout.addWidget(self.save_btn)

    def save_material(self):
        new_material = {tag: field.text() for tag, field in self.fields.items()}
        if self.material is None:
            self.add_material(new_material)
        else:
            for tag, value in new_material.items():
                self.material.find(tag).set("value", value)
        if self.on_update:
            self.on_update()
        self.accept()