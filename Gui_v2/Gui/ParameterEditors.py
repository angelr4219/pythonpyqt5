
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton, QScrollArea, QFormLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSignal

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
            3: ["TransverseParameters", "GateSmoothingParameters"],
            4: ["LayeredStructure"],
            5: ["MultiDomainParameters", "ComputationalSubdomains"],
            6: ["MaterialList"],
            7: ["AutoTuningData", "ImportExportAutoTuningState", "AutoTuningInput", "AutoTuningOutput", "EffectiveBC", "EffectiveBC_Parameters", "GateSmoothingParameters", "InterfaceBCparameters"]
        }
        self.populate_tabs()

        self.save_btn = QPushButton("Save All Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

    def populate_tabs(self):
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
                if section is not None and hasattr(section, '__iter__'):
                    form = QFormLayout()
                    group_box = QWidget()
                    group_layout = QVBoxLayout()
                    group_box.setLayout(group_layout)
                    group_layout.addLayout(form)

                    for elem in section:
                        if hasattr(elem, 'tag') and isinstance(elem.tag, str):
                            tag = str(elem.tag)
                            label = QLabel(tag)
                            value_text = elem.attrib.get("value", "")
                            value = QLineEdit(value_text)
                            value.editingFinished.connect(
                                lambda _, s=section_key, k=tag, w=value: self.parameter_edited.emit(s, k, w.text())
                            )
                            form.addRow(label, value)
                        else:
                            print(f"Skipped element: {elem} -> {type(elem)}")
                    scroll_layout.addWidget(group_box)
                else:
                    scroll_layout.addWidget(QLabel(f"Section {section_key} not found."))
            self.tab_widget.addTab(tab, f"Group {group_number}")

    def save_changes(self):
        if self.state_manager.current_file:
            self.state_manager.save_file()
            QMessageBox.information(self, "Saved", f"All changes saved to {self.state_manager.current_file}")
        else:
            QMessageBox.warning(self, "Warning", "No file loaded.")
