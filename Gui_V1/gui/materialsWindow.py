# gui.materials window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QDialog, QCheckBox
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
)

class MaterialDialog(QDialog):
    def __init__(self, material):
        super().__init__()
        self.setWindowTitle(f"Material: {material.find('name').attrib.get('value', '')}")
        layout = QVBoxLayout()
        for k in material:
            if k.tag == "name":
                continue
            label = QLabel(f"{k.tag}: {k.attrib.get('value', '')}")
            layout.addWidget(label)
        self.setLayout(layout)

       
       

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

        materials = manager.get_materials()
        for mat in materials:
            name = mat.find("name").attrib.get("value", "Unnamed")
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, m=mat: self.show_material(m))
            self.layout.addWidget(btn)

    def show_material(self, mat):
        dialog = MaterialDialog(mat)
        dialog.exec_()
