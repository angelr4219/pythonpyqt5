from PyQt5.QtWidgets import QWidget, QCheckBox, QMessageBox, QTabWidget, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QLineEdit
from Gui.ToolTips import show_parameter_tooltip_persistent
from PyQt5.QtCore import QTimer

class ManualParameterEditors(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.xml_manager = self.state_manager.xml_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self.layout.addWidget(self.tooltip_checkbox)

        self.main_tab_widget = QTabWidget()
        self.layout.addWidget(self.main_tab_widget)
        self.state_manager.set_unsaved_changes(True)
        self.input_field = QLineEdit()
        self.param_index = {}

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
        self.input_field.textChanged.connect(self.on_value_changed)

    def populate_main_tabs(self):
        self.main_tab_widget.clear()
        for tab_index, (group_name, section_keys) in enumerate(self.group_structure.items()):
            sub_tab_widget = QTabWidget()
            for section_key in section_keys:
                editor_widget = self.create_section_editor(section_key, tab_index)
                sub_tab_widget.addTab(editor_widget, section_key)
            self.main_tab_widget.addTab(sub_tab_widget, group_name)

    def create_section_editor(self, section_key, tab_index):
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
        tab_index = self.main_tab_widget.count()

        section = self.state_manager.xml_manager.root.find(f".//{section_key}")
        if section is not None:
            self.build_form_from_element(section, form_layout, tab_index, scroll, path=section_key)
        else:
            form_layout.addRow(QLabel(f"Section {section_key} not found."))

        return widget

    def build_form_from_element(self, element, form_layout, tab_index, scroll_area, path=""):
        for child in element:
            if list(child):
                sub_path = f"{path}/{child.tag}" if path else child.tag
                group_box = QWidget()
                group_layout = QVBoxLayout()
                group_box.setLayout(group_layout)
                group_label = QLabel(child.tag)
                group_layout.addWidget(group_label)
                sub_form = QFormLayout()
                self.build_form_from_element(child, sub_form, tab_index, scroll_area, sub_path)
                group_layout.addLayout(sub_form)
                form_layout.addRow(group_box)
            elif hasattr(child, 'tag') and isinstance(child.tag, str):
                label = QLabel(child.tag)
                value = QLineEdit(child.attrib.get("value", ""))
                show_parameter_tooltip_persistent(value, child.tag)
                form_layout.addRow(label, value)

                # Index the parameter for jump-to lookup
                param_name = child.tag
                self.param_index[param_name] = {
                    "widget": value,
                    "tab": tab_index,
                    "scroll_area": scroll_area
                }
                full_path = f"{path}/{param_name}" if path else param_name

                value.editingFinished.connect(
                    lambda p=full_path, w=value: self.on_field_edit(p, w.text())
                )
                form_layout.addRow(label, value)

    def save_changes(self):
        if self.state_manager.current_file:
            self.state_manager.save_file()
            QMessageBox.information(self, "Saved", f"All changes saved to {self.state_manager.current_file}")
        else:
            QMessageBox.warning(self, "Warning", "No file loaded.")

    def apply_changes_to_xml(self):
        if not self.state_manager.tree:
            return

        root = self.state_manager.tree.getroot()

        for param_name, widget in self.param_widgets.items():
            element = root.find(f".//*[@{param_name}]")  # fallback for bad xpath
            if element is None:
                element = root.find(f".//{param_name}")
            if element is not None:
                element.set("value", widget.text())

    def on_value_changed(self, path, widget):
        new_value = widget.text()
        self.state_manager.xml_manager.set_value(path, new_value)
        self.state_manager.set_unsaved_changes(True)
    def on_field_edit(self, path, new_value):
        self.state_manager.xml_manager.set_value(path, new_value)
        self.state_manager.set_unsaved_changes(True)
        self.state_manager.xml_updated.emit()
    def jump_to_parameter(self, name):
        info = self.param_index.get(name)
        if not info:
            QMessageBox.information(self, "Parameter Not Found", f"'{name}' is not currently displayed.")
            return

        self.main_tab_widget.setCurrentIndex(info["tab"])
        info["scroll_area"].ensureWidgetVisible(info["widget"])
        info["widget"].setFocus()
        info["widget"].setStyleSheet("background-color: yellow; border: 2px solid orange;")
        QTimer.singleShot(1500, lambda: info["widget"].setStyleSheet(""))