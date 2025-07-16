from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFormLayout, QLineEdit, QGroupBox
from PyQt5.QtCore import pyqtSignal

class LayerEditorWidget(QWidget):
    layer_updated = pyqtSignal(int, dict)

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

    def load_layers(self, layers):
        for i in reversed(range(self.inner_layout.count())):
            self.inner_layout.itemAt(i).widget().setParent(None)

        for index, layer in enumerate(layers):
            box = QGroupBox(f"Layer {index + 1}")
            form = QFormLayout()
            fields = {}
            for key, value in layer.items():
                input_field = QLineEdit(value)
                input_field.editingFinished.connect(lambda i=index, k=key, w=input_field: self.emit_layer_update(i, k, w.text()))
                form.addRow(QLabel(key), input_field)
            box.setLayout(form)
            self.inner_layout.addWidget(box)

    def emit_layer_update(self, index, key, value):
        self.layer_updated.emit(index, {key: value})