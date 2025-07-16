from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QScrollArea, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal

class ParameterEditorWidget(QWidget):
    parameter_edited = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.inner_widget = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner_widget.setLayout(self.inner_layout)
        self.scroll_area.setWidget(self.inner_widget)
        self.layout.addWidget(self.scroll_area)

    def load_parameters(self, parameter_sections):
        for i in reversed(range(self.inner_layout.count())):
            self.inner_layout.itemAt(i).widget().setParent(None)

        for section_name, parameters in parameter_sections.items():
            box = QGroupBox(section_name)
            form = QFormLayout()
            for key, value in parameters.items():
                input_field = QLineEdit(value)
                input_field.editingFinished.connect(
                    lambda s=section_name, k=key, w=input_field: self.emit_parameter_edit(s, k, w.text())
                )
                form.addRow(QLabel(key), input_field)
            box.setLayout(form)
            self.inner_layout.addWidget(box)

    def emit_parameter_edit(self, section, key, value):
        self.parameter_edited.emit(section, key, value)