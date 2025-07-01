
# logic/layer_editor.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit

class LayerEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = None
        if self.layout() is None:
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)
        else:
            self.layout = self.layout()


    def load_data(self, manager):
        self.manager = manager
        self.layout.setParent(None)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

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
            self.layout.addWidget(box)
