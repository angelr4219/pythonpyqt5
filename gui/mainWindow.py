
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QTextEdit, QMessageBox, QStackedLayout
)
from logic.xmlManager import XMLManager

from logic.layerEditor import LayerEditorWidget
from gui.layerWindow import LayerWindow

from logic.materialLookup import MaterialLookupWidget
from gui.materialsWindow import MaterialDialog

from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, xml_path):
        super().__init__()
        self.setWindowTitle("DotArray2 XML Editor")
        self.setGeometry(200, 100, 900, 700)
        self.manager = XMLManager()
        self.file_name = "edited.xml"

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.file_button = QPushButton("Load XML File")
        self.file_button.clicked.connect(self.load_xml)

        self.download_button = QPushButton("Download Edited XML")
        self.download_button.clicked.connect(self.save_xml)

        self.main_view = QTextEdit()
        self.layer_view = LayerEditorWidget()
        self.material_view = MaterialLookupWidget()

        self.view_stack = QStackedLayout()
        self.view_stack.addWidget(self.main_view)
        self.view_stack.addWidget(self.layer_view)
        self.view_stack.addWidget(self.material_view)

        self.button_bar = QHBoxLayout()
        self.main_btn = QPushButton("Main")
        self.layer_btn = QPushButton("Edit Layers")
        self.material_btn = QPushButton("Material Lookup")

        views = {
            self.main_btn: 0,
            self.layer_btn: 1,
            self.material_btn: 2,
        }
        for btn, idx in views.items():
            btn.clicked.connect(partial(self.view_stack.setCurrentIndex, idx))
            self.button_bar.addWidget(btn)
        self.button_bar.addWidget(self.download_button)

        layout.addWidget(self.file_button)
        layout.addLayout(self.button_bar)
        layout.addLayout(self.view_stack)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def load_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if not path:
            return
        self.manager.load_file(path)
        self.file_name = path.replace(".xml", "_edited.xml")
        self.main_view.setPlainText(self.manager.dump_pretty())

        #self.layer_view.load_data(self.manager)
        #self.material_view.load_data(self.manager)

    def save_xml(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save XML", self.file_name, "XML Files (*.xml)")
        if path:
            self.manager.save_file(path)
            QMessageBox.information(self, "Saved", f"File saved to {path}")