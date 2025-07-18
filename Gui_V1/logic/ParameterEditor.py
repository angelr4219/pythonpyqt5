# logic.baseeditor.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QGroupBox, QScrollArea, QCheckBox, QMainWindow,   QTabWidget,
     QPushButton, QTextEdit, QFileDialog, QHBoxLayout, QMessageBox, QDialog
)

from logic.tooltipManager import show_parameter_tooltip_persistent

class ParameterEditor(QWidget):
    def __init__(self, xml_manager, path, title):
        super().__init__()
        self.xml_manager = xml_manager
        self.path = path
        self.root = self.xml_manager.root.find(path)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self._layout.addWidget(self.tooltip_checkbox)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self._layout.addWidget(self.scroll_area)

        self.setWindowTitle(title)
        self.inputs = {}

        self.populate_fields()

    def populate_fields(self):
        if self.root is None:
            return

        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        box = QGroupBox(self.path)
        form = QFormLayout()

        for child in self.root:
            tag = child.tag
            val = child.attrib.get("value", "")
            input_field = QLineEdit(val)

            if self.tooltip_checkbox.isChecked():
                input_field.focusInEvent = self.make_focus_event(input_field, tag)

            input_field.editingFinished.connect(lambda tag=tag, w=input_field: self.update_value(tag, w.text()))
            form.addRow(QLabel(tag), input_field)
            self.inputs[tag] = input_field

        box.setLayout(form)
        self.scroll_layout.addWidget(box)

    def make_focus_event(self, widget, label):
        def event(event):
            show_parameter_tooltip_persistent(widget, label)
            QLineEdit.focusInEvent(widget, event)
        return event

    def update_value(self, tag, value):
        if self.root is None:
            return
        node = self.root.find(tag)
        if node is not None:
            node.attrib["value"] = value
    
    def load_data(self, manager):
        self.manager = manager
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        section = self.manager.root.find(f".//{self.section_key}")
        if section is None:
            self.layout.addRow(QLabel(f"No section {self.section_key} found."))
            return

        for elem in section:
            tag = elem.tag
            value = elem.attrib.get("value", "")
            line_edit = QLineEdit(value)
            line_edit.editingFinished.connect(
                lambda le=line_edit, el=elem: el.set("value", le.text())
            )
            self.layout.addRow(QLabel(tag), line_edit)
