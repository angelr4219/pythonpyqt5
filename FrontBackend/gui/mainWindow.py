from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QGroupBox, QScrollArea, QCheckBox, QMainWindow,   QTabWidget,
     QPushButton, QTextEdit, QFileDialog, QHBoxLayout, QMessageBox, QDialog
)
from logic.xmlManager import XMLManager
from logic.layerEditor import LayerEditorWidget
from logic.materialLookup import MaterialLookupWidget
from logic.BaseEditor import ParameterEditor
from logic.tooltipManager import show_parameter_tooltip_persistent


class ParameterDialog(QDialog):
    def __init__(self, manager, section_key):
        super().__init__()
        self.setWindowTitle(section_key)
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        form_layout = QFormLayout()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        section = manager.root.find(f".//{section_key}")
        if section is not None:
            for elem in section:
                label = QLabel(elem.tag)
                value = QLineEdit(elem.attrib.get("value", ""))
                value.focusInEvent = self.make_focus_event(value, elem.tag)
                value.editingFinished.connect(lambda le=value, el=elem: el.set("value", le.text()))
                form_layout.addRow(label, value)
        else:
            form_layout.addRow(QLabel("Section not found"))
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def make_focus_event(self, widget, label):
        def event(event):
            show_parameter_tooltip_persistent(widget, label)
            QLineEdit.focusInEvent(widget, event)
        return event

class BaseEditor(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.sections = [
            
            "AutoTuningData",
            "ImportExportAutoTuningState",
            "AutoTuningInput",
            "AutoTuningOutput",
            "EffectiveBC",
            "EffectiveBC_Parameters",
            "GateBias",
            "TransverseParameters",
            "GateSmoothingParameters",
            "InterfaceBCparameters"
        ]

        for section in self.sections:
            btn = QPushButton(section)
            btn.clicked.connect(lambda checked, s=section: self.open_dialog(s))
            layout.addWidget(btn)

    def open_dialog(self, section_key):
        dialog = ParameterDialog(self.manager, section_key)
        dialog.setMinimumSize(500, 600)
        dialog.exec_()

class MainWindow(QMainWindow):
    def __init__(self, xml_path):
        super().__init__()
        self.setWindowTitle("DotArray2 XML Editor - Grouped Tabs")
        self.setGeometry(200, 100, 900, 700)

        self.manager = XMLManager()
        self.manager.load_file(xml_path)
        self.file_name = xml_path.replace(".xml", "_edited.xml")
        

        self.initUI()
        self.load_views()

    def initUI(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.tabs = QTabWidget()

#main
        self.main_editor = QTextEdit()
        self.main_editor.setReadOnly(True)
        self.main_editor.setPlainText(self.manager.dump_pretty())

        self.tabs = QTabWidget()
        self.main_view = QTextEdit()
        self.layer_view = LayerEditorWidget()
        self.material_view = MaterialLookupWidget()
        self.base_editor = BaseEditor(self.manager)


        self.run_parameters_editor = self.make_parameter_tab("RunParameters", "Run Parameters")
        self.gate_bias_editor = self.make_parameter_tab("GateBias", "Gate Bias")
        self.transverse_editor = self.make_parameter_tab("TransverseParameters", "Transverse Meshing")
        self.layered_structure_editor = self.make_parameter_tab("LayeredStructure", "Layered Structure")
        self.multi_domain_editor = self.make_parameter_tab("MultiDomainParameters", "MultiDomain Settings")
        self.material_list_editor = self.make_parameter_tab("MaterialList", "Material List")

        self.base_editor = BaseEditor(self.manager)
        self.auto_tuning_editor = self.make_section(self.base_editor, "Auto Tuning & Related")

        self.layer_view = LayerEditorWidget()
        self.layer_view.load_data(self.manager)
        self.layers_editor = self.make_section(self.layer_view, "Layers & Materials")

        self.material_view = MaterialLookupWidget()
        self.material_view.load_data(self.manager)
        self.material_lookup_editor = self.make_section(self.material_view, "Material Lookup")

        # Now adding to tabs in clean one-line each:
        self.tabs.addTab(self.main_editor, "Main")
        self.tabs.addTab(self.run_parameters_editor, "Run Parameters")
        self.tabs.addTab(self.gate_bias_editor, "Gate Bias")
        self.tabs.addTab(self.transverse_editor, "Transverse Meshing")
        self.tabs.addTab(self.layered_structure_editor, "Layered Structure")
        self.tabs.addTab(self.multi_domain_editor, "MultiDomain Settings")
        self.tabs.addTab(self.material_list_editor, "Material List")
        self.tabs.addTab(self.auto_tuning_editor, "Auto Tuning & Related")
        self.tabs.addTab(self.layers_editor, "Layers")
        self.tabs.addTab(self.material_lookup_editor, "Material Lookup")

        self.central_layout.addWidget(self.tabs)

        button_layout = QHBoxLayout()
        load_button = QPushButton("Load XML File")
        save_button = QPushButton("Save Edited XML")
        load_button.clicked.connect(self.load_xml)
        save_button.clicked.connect(self.save_xml)
        button_layout.addWidget(load_button)
        button_layout.addWidget(save_button)

        self.central_layout.addLayout(button_layout)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def make_section(self, widget, title):
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def make_parameter_tab(self, section_key, title):
        editor = ParameterEditor(self.manager, section_key, title)
        return self.make_section(editor, title)

    def load_views(self):
        self.main_view.setPlainText(self.manager.dump_pretty())
        self.layer_view.load_data(self.manager)
        self.material_view.load_data(self.manager)

    def load_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if path:
            self.manager.load_file(path)
            self.file_name = path.replace(".xml", "_edited.xml")
            self.load_views()

    def save_xml(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save XML", self.file_name, "XML Files (*.xml)")
        if path:
            self.manager.save_file(path)
            QMessageBox.information(self, "Saved", f"File saved to {path}")
