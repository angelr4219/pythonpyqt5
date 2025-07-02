# logic/layer_editor.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit

class LayerEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None

        if self.layout() is None:
            self._layout = QVBoxLayout()
            self.setLayout(self._layout)
        else:
            self._layout = self.layout()

    def load_data(self, manager):
        self.manager = manager

        # Clear previous content safely
        while self._layout.count():
            child = self._layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for idx, layer in enumerate(manager.get_layers()):
            box = QGroupBox(f"Layer {idx + 1}")
            form = QFormLayout()
            for elem in layer:
                label = elem.tag
                input_field = QLineEdit(elem.attrib.get("value", ""))
                input_field.editingFinished.connect(
                    lambda idx=idx, k=elem.tag, w=input_field:
                    manager.update_layer(idx, k, w.text())
                )
                form.addRow(QLabel(label), input_field)
            box.setLayout(form)
            self._layout.addWidget(box)
       

    def make_delete_handler(self, index):
        return lambda: (
            self.manager.delete_layer(index),
            self.load_data(self.manager)
        )

    def add_layer(self):
        self.manager.add_layer()
        self.load_data(self.manager)
