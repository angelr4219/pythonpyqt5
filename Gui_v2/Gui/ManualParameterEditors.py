from PyQt5.QtWidgets import QWidget, QCheckBox ,QMessageBox, QTabWidget, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QLineEdit


class ManualParameterEditors(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self.layout.addWidget(self.tooltip_checkbox)

        self.main_tab_widget = QTabWidget()
        self.layout.addWidget(self.main_tab_widget)

        self.group_structure = {
            "Run Parameters": [
                "RunParameters",
                "PoissonSolver_NumericalParameters",
                "SP_Parameters",
                "SingleParticleEigensystemParameters"
            ],
            "Auto Tuning": [
                "AutoTuningData",
                "AutoTuningInput",
                "AutoTuningOutput",
                "ImportExportSPiterate",
                "CreateInitialSPiterate"
            ],
            "Boundary Conditions": [
                "InterfaceBCparameters",
                "EffectiveBC_Parameters",
                "LowerSurfaceBoundaryConditions"
            ],
            "Transverse Meshing and Gate Smoothing": [
                "TransverseParameters",
                "GateSmoothingParameters"
            ],
            "Import/Export Initial Solution": [
                "ImportExportSPiterate",
                "CreateInitialSPiterate"
            ],
            "Computational Subdomains and Settings": [
                "MultiDomainParameters",
                "ComputationalSubdomains"
            ],
            "Tunneling and Excluded Potential Calculation": [
                "TunnelingRateCalculation",
                "ExcludedPotentialCalculation"
            ]
        }

        self.populate_main_tabs()

    def populate_main_tabs(self):
        self.main_tab_widget.clear()
        for group_name, section_keys in self.group_structure.items():
            sub_tab_widget = QTabWidget()
            for section_key in section_keys:
                editor_widget = self.create_section_editor(section_key)
                sub_tab_widget.addTab(editor_widget, section_key)
            self.main_tab_widget.addTab(sub_tab_widget, group_name)

    def create_section_editor(self, section_key):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        section = self.state_manager.xml_manager.root.find(f".//{section_key}")
        if section is not None:
            self.build_form_from_element(section, form_layout)
        else:
            form_layout.addRow(QLabel(f"Section {section_key} not found."))

        return widget

    def build_form_from_element(self, element, form_layout):
        for child in element:
            if list(child):
                group_box = QWidget()
                group_layout = QVBoxLayout()
                group_box.setLayout(group_layout)
                label = QLabel(child.tag)
                group_layout.addWidget(label)
                sub_form = QFormLayout()
                self.build_form_from_element(child, sub_form)
                group_layout.addLayout(sub_form)
                form_layout.addRow(group_box)
            elif hasattr(child, 'tag') and isinstance(child.tag, str):
                label = QLabel(child.tag)
                value = QLineEdit(child.attrib.get("value", ""))
                form_layout.addRow(label, value)
    def save_changes(self):
        if self.state_manager.current_file:
            self.state_manager.save_file()
            QMessageBox.information(self, "Saved", f"All changes saved to {self.state_manager.current_file}")
        else:
            QMessageBox.warning(self, "Warning", "No file loaded.")

