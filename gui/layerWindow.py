
# gui/layer_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class LayerWindow(QWidget):
    def __init__(self, xml_manager):
        super().__init__()
        self.setWindowTitle("Edit Layers")
        self.resize(400, 300)
        self.xml_manager = xml_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layers = self.xml_manager.root.find("LayeredStructure").findall("Layer")

        for layer in self.layers:
            self.add_layer_editor(layer)

        self.save_btn = QPushButton("Save and Close")
        self.save_btn.clicked.connect(self.close)
        self.layout.addWidget(self.save_btn)

    def add_layer_editor(self, layer_elem):
        group = QVBoxLayout()

        for tag in ["name", "materialType", "height", "panelDensity", "localWaveCalcType"]:
            child = layer_elem.find(tag)
            if child is not None:
                row = QHBoxLayout()
                row.addWidget(QLabel(f"{tag}:"))
                field = QLineEdit(child.attrib.get("value", ""))
                field.textChanged.connect(lambda val, elem=child: elem.set("value", val))
                row.addWidget(field)
                group.addLayout(row)

        container = QWidget()
        container.setLayout(group)
        self.layout.addWidget(container)
