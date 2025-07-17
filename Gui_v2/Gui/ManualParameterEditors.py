from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QLineEdit

class ManualParameterEditors(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.section_group = {
            "Run Parameters": ["RunParameters", "PoissonSolver_NumericalParameters", "SP_Parameters", "SingleParticleEigensystemParameters"],
            "Gate Bias": ["GateBias"],
            "Auto Tuning Related": ["AutoTuningData", "ImportExportAutoTuningState", "AutoTuningInput", "AutoTuningOutput", "EffectiveBC", "EffectiveBC_Parameters", "GateSmoothingParameters", "InterfaceBCparameters"],
            "Transverse Meshing": ["TransverseParameters", "GateSmoothingParameters"],
            "MultiDomain Settings": ["MultiDomainParameters", "ComputationalSubdomains"]
        }

        self.populate_tabs()

    def populate_tabs(self):
        self.tab_widget.clear()

        for tab_name, section_keys in self.section_group.items():
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
                            if not elem.attrib.get("value"):
                                continue
                            label = QLabel(tag)
                            value_text = elem.attrib.get("value", "")
                            value = QLineEdit(value_text)
                            form.addRow(label, value)
                    scroll_layout.addWidget(group_box)
                else:
                    scroll_layout.addWidget(QLabel(f"Section {section_key} not found."))
            self.tab_widget.addTab(tab, tab_name)
