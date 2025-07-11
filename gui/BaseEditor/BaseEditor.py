from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QGroupBox
)

# base_editor.py

class ParameterEditor(QWidget):
    def __init__(self, xml_manager, path, title):
        super().__init__()
        self.xml_manager = xml_manager
        self.path = path
        self.root = self.xml_manager.root.find(path)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle(title)
        self.inputs = {}

        self.form = QFormLayout()
        self.group = QGroupBox(title)
        self.group.setLayout(self.form)
        self.layout.addWidget(self.group)

        self.populate_fields()

    def populate_fields(self):
        for child in self.root:
            tag = child.tag
            val = child.attrib.get("value", "")
            input_field = QLineEdit(val)
            input_field.editingFinished.connect(lambda tag=tag, w=input_field: self.update_value(tag, w.text()))
            self.form.addRow(QLabel(tag), input_field)
            self.inputs[tag] = input_field

    def update_value(self, tag, value):
        node = self.root.find(tag)
        if node is not None:
            node.attrib["value"] = value
