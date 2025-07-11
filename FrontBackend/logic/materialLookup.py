# gui/material_lookup.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGroupBox, QDialog, QLineEdit, QFormLayout, QMessageBox,QCheckBox
)
from PyQt5.QtCore import Qt
from logic.ParameterDocs import parameter_docs

from logic.tooltipManager import show_parameter_tooltip
class MaterialLookupWidget(QWidget):
    def add_material(self, material_data):
        if self.manager:
            self.manager.add_material(material_data)
            self.load_data(self.manager)
    def __init__(self):
        super().__init__()
        self.manager = None
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self._layout.addWidget(self.tooltip_checkbox)

    def load_data(self, manager):
        self.manager = manager
        while self._layout.count() > 1:
            child = self._layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        materials = self.manager.get_materials()
        for mat in materials:
            name = mat.find("name").attrib.get("value", "Unnamed")
            box = QGroupBox(f"Material: {name}")
            inner_layout = QVBoxLayout()
            for elem in mat:
                if elem.tag == "name":
                    continue
                tag = elem.tag
                value = elem.attrib.get("value", "")
                line = QLabel(f"{tag}: {value}")
                if self.tooltip_checkbox.isChecked():
                    line.mousePressEvent = self.make_mouse_event(line, tag)
                inner_layout.addWidget(line)
            box.setLayout(inner_layout)
            self._layout.addWidget(box)

    def make_mouse_event(self, widget, tag):
        def event(event):
            show_parameter_tooltip(widget, tag)
        return event

    def edit_material(self, mat, index):
        dialog = EditableMaterialDialog(mat, self.manager, index, on_update=self.refresh)
        dialog.exec_()

    def refresh(self):
        self.load_data(self.manager)

class EditableMaterialDialog(QDialog):
    def __init__(self, material, manager, index, on_update=None):
        super().__init__()
        self.setWindowTitle(f"Edit Material: {material.find('name').attrib.get('value', '')}")
        self.material = material
        self.manager = manager
        self.index = index
        self.on_update = on_update
        self.setLayout(QVBoxLayout())
        self.form = QFormLayout()
        self.fields = {}
        for k in material:
            if "value" in k.attrib:
                field = QLineEdit(k.attrib["value"])
                field.focusInEvent = lambda event, w=field, p=k.tag: (
                    show_parameter_tooltip(w, p),
                    QLineEdit.focusInEvent(w, event)
                )
                self.fields[k.tag] = field
                self.form.addRow(QLabel(f"{k.tag}:"), field)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_material)
        self.layout().addLayout(self.form)
        self.layout().addWidget(self.save_btn)

    def save_material(self):
        for tag, field in self.fields.items():
            value = field.text()
            if self.material.find(tag) is not None:
                self.material.find(tag).set("value", value)
        if self.on_update:
            self.on_update()
        self.accept()