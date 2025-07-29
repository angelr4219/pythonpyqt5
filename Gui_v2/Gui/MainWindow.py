
from PyQt5.QtWidgets import QMainWindow, QShortcut,QTabWidget,QMessageBox , QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QApplication , QCheckBox , QLabel, QLineEdit , QFormLayout, QDialog, QPlainTextEdit, QDialogButtonBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont,QKeySequence

from State.StateManager import StateManager
from Gui.LayerEditor import LayerEditorWidget
from Gui.MaterialEditor import MaterialEditorWidget
from Gui.ManualParameterEditors import ManualParameterEditors
from Gui.ToolTips import setup_tooltips, show_parameter_tooltip_persistent , show_parameter_tooltip 
from Gui.StartHere import StartHereTab
from Logic.ParameterDocs import *
from Gui.LivePreview import LivePreviewWidget 
from Gui.SearchBar import ParameterSearchBar


class MainWindow(QMainWindow):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.setWindowTitle("DotArray2 XML Editor ")
        self.setGeometry(200, 100, 900, 700)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.param_widgets = {}


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
        # SearchBar
        self.search_bar = ParameterSearchBar(self.state_manager.xml_manager, self)
        self.layout.insertWidget(0, self.search_bar)


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

        # Create buttons
        undo_button = QPushButton("Undo")
        redo_button = QPushButton("Redo")

        # Store in self
        self.undo_button = undo_button
        self.redo_button = redo_button

        # Connect to StateManager
        undo_button.clicked.connect(self.state_manager.undo)
        redo_button.clicked.connect(self.state_manager.redo)

        # Add to layout
        button_layout.addWidget(undo_button)
        button_layout.addWidget(redo_button)
        # Keyboard shortcuts (Ctrl+Z / Ctrl+Y)
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.activated.connect(self.state_manager.undo)

        redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        redo_shortcut.activated.connect(self.state_manager.redo)

        # Update button states based on stack state
        self.state_manager.undo_state_changed.connect(self.update_undo_redo_buttons)



        # Connect state signals
        self.state_manager.file_loaded.connect(self.refresh_tabs)
        self.state_manager.xml_updated.connect(self.refresh_tabs)
        #preview
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        preview_tab = LivePreviewWidget(self.state_manager)
        self.tab_widget.addTab(preview_tab, "Preview XML")
        #viewChanges
        view_changes_btn = QPushButton("View Changes")
        view_changes_btn.clicked.connect(self.show_diff_dialog)
        button_layout.addWidget(view_changes_btn)


    def update_undo_redo_buttons(self, can_undo, can_redo):
        self.undo_button.setEnabled(can_undo)
        self.redo_button.setEnabled(can_redo)


    @pyqtSlot()
    def refresh_tabs(self):
        print("Refreshing all tabs")

    def load_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if path:
            self.state_manager.apply_change({"type": "generic_update"}, record_undo=False)
            self.state_manager.save_file(path)

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
    
    def show_diff_dialog(self):
        diff_lines = self.state_manager.get_xml_diff()
        diff_text = ''.join(diff_lines) or "No changes."

        dialog = QDialog(self)
        dialog.setWindowTitle("XML Diff Viewer")
        dialog.resize(800, 600)

        layout = QVBoxLayout(dialog)

        text_area = QPlainTextEdit()
        text_area.setReadOnly(True)
        text_area.setFont(QFont("Courier New", 10))
        text_area.setPlainText(diff_text)
        layout.addWidget(text_area)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec_()
