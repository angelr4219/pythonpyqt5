# logic/layer_editor.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGroupBox, QDialog, QLineEdit, QFormLayout, QMessageBox, QScrollArea, QCheckBox
)
from logic.ParameterDocs import parameter_docs

from logic.tooltipManager import show_parameter_tooltip_persistent

class LayerEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self._layout.addWidget(self.tooltip_checkbox)

        self.add_button = QPushButton("Add Layer")
        self.add_button.clicked.connect(self.add_layer)
        self._layout.addWidget(self.add_button)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self._layout.addWidget(self.scroll_area)

    def load_data(self, manager):
        self.manager = manager
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for idx, layer in enumerate(manager.get_layers()):
            box = QGroupBox(f"Layer {idx + 1}")
            form = QFormLayout()
            for elem in layer:
                label = elem.tag
                input_field = QLineEdit(elem.attrib.get("value", ""))
                if self.tooltip_checkbox.isChecked():
                    input_field.focusInEvent = self.make_focus_event(input_field, label)
                input_field.editingFinished.connect(
                    lambda idx=idx, k=elem.tag, w=input_field:
                    manager.update_layer(idx, k, w.text())
                )
                form.addRow(QLabel(label), input_field)
            box.setLayout(form)
            self.scroll_layout.addWidget(box)

    def make_focus_event(self, widget, label):
        def event(event):
            show_parameter_tooltip_persistent(widget, label)
            QLineEdit.focusInEvent(widget, event)
        return event

    def make_delete_handler(self, index):
        return lambda: (self.manager.delete_layer(index), self.load_data(self.manager))

    def add_layer(self):
        if self.manager:
            self.manager.add_layer()
            self.load_data(self.manager)

    def refresh(self):
        self.load_data(self.manager)
