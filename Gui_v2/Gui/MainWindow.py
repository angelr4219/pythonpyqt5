
from PyQt5.QtWidgets import QMainWindow, QTabWidget,QMessageBox , QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QApplication , QCheckBox , QLabel, QLineEdit , QFormLayout
from PyQt5.QtCore import pyqtSlot
from State.StateManager import StateManager
#from Gui.ParameterEditors import ParameterEditors
from Gui.LayerEditor import LayerEditorWidget
from Gui.MaterialEditor import MaterialEditorWidget
from Gui.ManualParameterEditors import ManualParameterEditors
from Gui.ToolTips import setup_tooltips, show_parameter_tooltip_persistent , show_parameter_tooltip 
from Gui.StartHere import StartHereTab
from Logic.ParameterDocs import *

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
        
         # Tooltip Toggle
        self.tooltip_checkbox = QCheckBox("Show Tooltifps")
        self.tooltip_checkbox.setChecked(True)
        self.layout.addWidget(self.tooltip_checkbox)

         # Tooltip Demo Section (temporary example)
        self.tooltip_demo_form = QFormLayout()
        self.param_widgets = {}
        self.dummy_param_dict = {
            "SCstopTolerance": "1.0e-9",
            "RKinitTimestep": "0.5",
            "RKmaxSteps": "50"
        }
        for param_name, param_value in self.dummy_param_dict.items():
            label = QLabel(param_name)
            edit = QLineEdit()
            edit.setText(str(param_value))
            if self.tooltip_checkbox.isChecked():
                setup_tooltips(edit, param_name)
            edit.setToolTip(param_name)
            self.param_widgets[param_name] = edit
            self.tooltip_demo_form.addRow(label, edit)


        #load/Save
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

        #load/Save
        undo_button = QPushButton("Undo")
        redo_button = QPushButton("Redo")
        undo_button.clicked.connect(self.state_manager.undo)
        redo_button.clicked.connect(self.state_manager.redo)
        button_layout.addWidget(undo_button)
        button_layout.addWidget(redo_button)
        
        def save_xml(self):
                self.apply_changes_to_xml()
                path, _ = QFileDialog.getSaveFileName(self, "Save XML", "", "XML Files (*.xml)")
                if path:
                    self.state_manager.apply_change({"type": "generic_update"}, record_undo=False)
                    self.state_manager.save_file(path)


        # Connect state signals
        self.state_manager.file_loaded.connect(self.refresh_tabs)
        self.state_manager.xml_updated.connect(self.refresh_tabs)

    @pyqtSlot()
    def refresh_tabs(self):
        print("Refreshing all tabs")

    def load_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if path:
            self.state_manager.open_file(path)

    def save_xml(self):
        self.apply_changes_to_xml()
        path, _ = QFileDialog.getSaveFileName(self, "Save XML", "", "XML Files (*.xml)")
        if path:
            self.state_manager.save_file(path)

    def apply_changes_to_xml(self):
        if not self.state_manager.xml_manager.tree:
            return

        root = self.state_manager.xml_manager.tree.getroot()

        for param_name, widget in self.param_widgets.items():
            element = root.find(f".//{param_name}")
            if element is not None:
                element.set("value", widget.text())
