
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QApplication
from PyQt5.QtCore import pyqtSlot
from State.StateManager import StateManager
#from Gui.ParameterEditors import ParameterEditors
from Gui.LayerEditor import LayerEditorWidget
from Gui.MaterialEditor import MaterialEditorWidget
from Gui.ManualParameterEditors import ManualParameterEditors

from Gui.StartHere import StartHereTab

class MainWindow(QMainWindow):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.setWindowTitle("DotArray2 XML Editor ")
        self.setGeometry(200, 100, 900, 700)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
        #self.parameter_editor = ParameterEditors(self.state_manager)
        #self.tabs.addTab(self.parameter_editor, "Simulation Parameters")    
        self.layer_editor = LayerEditorWidget(self.state_manager)
        self.tabs.addTab(self.layer_editor, "Layer Editor")    
        self.material_editor = MaterialEditorWidget(self.state_manager)
        self.tabs.addTab(self.material_editor, "Materials Look-Up")    
        self.start_here = StartHereTab(self.state_manager)
        self.tabs.addTab(self.start_here, "Instructions")

        self.parameter_editor = ManualParameterEditors(self.state_manager)
        self.tabs.addTab(self.parameter_editor, "Simulation Parameters")    
        
 

        self.layout.addWidget(self.tabs)
        button_layout = QHBoxLayout()
        load_btn = QPushButton("Load XML")
        save_btn = QPushButton("Save XML")
        load_btn.clicked.connect(self.load_xml)
        save_btn.clicked.connect(self.save_xml)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(save_btn)
        self.layout.addLayout(button_layout)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        undo_button = QPushButton("Undo")
        redo_button = QPushButton("Redo")
        undo_button.clicked.connect(self.state_manager.undo)
        redo_button.clicked.connect(self.state_manager.redo)
        button_layout.addWidget(undo_button)
        button_layout.addWidget(redo_button)


        # Connect state signals
        self.state_manager.file_loaded.connect(self.refresh_tabs)
        self.state_manager.xml_updated.connect(self.refresh_tabs)

    @pyqtSlot()
    def refresh_tabs(self):
        print("Refreshing all tabs")
        # Calls to refresh UI contents would go here

    def load_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if path:
            self.state_manager.open_file(path)

    def save_xml(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save XML", "", "XML Files (*.xml)")
        if path:
            self.state_manager.save_file(path)