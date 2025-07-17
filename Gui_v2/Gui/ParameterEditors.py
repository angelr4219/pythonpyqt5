from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton, QScrollArea, QFormLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSignal
from Gui.ToolTips import setup_tooltips

#left temporarily as legacy code, meant to dynamically add tab groups

class ParameterEditors(QWidget):
    parameter_edited = pyqtSignal(str, str, str)

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.section_group = {
            1: ["RunParameters", "PoissonSolver_NumericalParameters", "SP_Parameters", "SingleParticleEigensystemParameters"],
            2: ["GateBias"],
            3: ["AutoTuningData", "ImportExportAutoTuningState", "AutoTuningInput", "AutoTuningOutput", "EffectiveBC", "EffectiveBC_Parameters", "GateSmoothingParameters", "InterfaceBCparameters"],
            4: ["TransverseParameters", "GateSmoothingParameters"],
            5: ["MultiDomainParameters", "ComputationalSubdomains"]
        }

        self.tab_names = {
            1: "Run Parameters",
            2: "Gate Bias",
            3: "Auto Tuning Related",
            4: "Transverse Meshing",
            5: "MultiDomain Settings"
        }

        self.save_btn = QPushButton("Save All Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

        self.state_manager.file_loaded.connect(self.populate_tabs)

    def populate_tabs(self):
        print("Refreshing tabs...")
        self.tab_widget.clear()
        for group_number, section_keys in self.section_group.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            tab_layout.addWidget(scroll_area)
            tab.setLayout(tab_layout)

            for section_key in section_keys:
                section = self.state_manager.xml_manager.root.find(f".//{section_key}")
                print("Checking section:", section_key, section)
                if section is not None and hasattr(section, '__iter__'):
                    form = QFormLayout()
                    group_box = QWidget()
                    group_layout = QVBoxLayout()
                    group_box.setLayout(group_layout)
                    group_layout.addLayout(form)

                    for elem in section:
                        if hasattr(elem, 'tag') and isinstance(elem.tag, str):
                            tag = str(elem.tag)
                            if not elem.attrib.get("value"):
                                continue
                            label = QLabel(tag)
                            value_text = elem.attrib.get("value", "")
                            value = QLineEdit(value_text)
                            setup_tooltips(value, tag)
                            value.editingFinished.connect(
                                lambda _, s=section_key, k=tag, w=value: self.parameter_edited.emit(s, k, w.text())
                            )
                            form.addRow(label, value)
                        else:
                            print(f"Skipped element: {elem} -> {type(elem)}")
                    scroll_layout.addWidget(group_box)
                else:
                    scroll_layout.addWidget(QLabel(f"Section {section_key} not found."))
            self.tab_widget.addTab(tab, self.tab_names.get(group_number, f"Group {group_number}"))

    def save_changes(self):
        if self.state_manager.current_file:
            self.state_manager.save_file()
            QMessageBox.information(self, "Saved", f"All changes saved to {self.state_manager.current_file}")
        else:
            QMessageBox.warning(self, "Warning", "No file loaded.")
