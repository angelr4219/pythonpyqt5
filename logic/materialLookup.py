# gui/material_lookup.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGroupBox

class MaterialLookupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def load_data(self, manager):
        self.manager = manager
        self.layout.setParent(None)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        materials = manager.get_materials()
        for mat in materials:
            btn = QPushButton(mat.find("name").attrib.get("value", "Unnamed"))
            btn.clicked.connect(lambda _, m=mat: self.show_material(m))
            self.layout.addWidget(btn)

        self.detail_box = QGroupBox("Material Info")
        self.detail_layout = QVBoxLayout()
        self.detail_box.setLayout(self.detail_layout)
        self.layout.addWidget(self.detail_box)

    def show_material(self, mat):
        for i in reversed(range(self.detail_layout.count())):
            self.detail_layout.itemAt(i).widget().setParent(None)
        for k in mat:
            if k.tag == "name":
                continue
            label = QLabel(f"{k.tag}: {k.attrib.get('value', '')}")
            self.detail_layout.addWidget(label)