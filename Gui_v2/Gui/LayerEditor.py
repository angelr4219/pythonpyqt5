from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit,
    QFormLayout, QMessageBox, QScrollArea, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from Gui.ToolTips import show_parameter_tooltip_persistent

class LayerEditorWidget(QWidget):
    layer_updated = pyqtSignal(int, dict)

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.edit_mode = False
        self.show_display = True

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Toolbar
        self.toolbar = QHBoxLayout()
        self.layout.addLayout(self.toolbar)

        self.present_btn = QPushButton("Present Layers")
        self.present_btn.clicked.connect(self.load_data)
        self.toolbar.addWidget(self.present_btn)

        self.add_btn = QPushButton("Add Layer")
        self.add_btn.clicked.connect(self.add_layer)
        self.toolbar.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Toggle Edit Mode")
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.toolbar.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Delete Last Layer")
        self.delete_btn.clicked.connect(self.delete_last_layer)
        self.toolbar.addWidget(self.delete_btn)

        self.display_btn = QPushButton("Toggle Display")
        self.display_btn.clicked.connect(self.toggle_display)
        self.toolbar.addWidget(self.display_btn)

        self.tooltip_checkbox = QCheckBox("Show Tooltips")
        self.tooltip_checkbox.setChecked(True)
        self.layout.addWidget(self.tooltip_checkbox)

        # Scrollable content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.inner_widget = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner_widget.setLayout(self.inner_layout)
        self.scroll_area.setWidget(self.inner_widget)
        self.layout.addWidget(self.scroll_area)

        self.state_manager.file_loaded.connect(self.load_data)
        self.load_data(None)
    def load_data(self, _):
        # Clear current layout without resetting QWidget layout
        while self.inner_layout.count():
            child = self.inner_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        layers = self.state_manager.xml_manager.get_layers()
        for index, layer_data in enumerate(layers):
            group_box = QGroupBox(f"Layer {index + 1}")
            form_layout = QFormLayout()

            for key, element in layer_data.items():
                value = element.get("@_value") if isinstance(element, dict) else str(element)
                line_edit = QLineEdit(value)
                line_edit.editingFinished.connect(
                    lambda i=index, k=key, w=line_edit: self.state_manager.apply_change({
                        "type": "update_layer_param",
                        "index": i,
                        "key": k,
                        "value": w.text()
                    })
                )
                form_layout.addRow(QLabel(key), line_edit)

            group_box.setLayout(form_layout)
            self.inner_layout.addWidget(group_box)

    def update_layer(self, index, key, value):
        layer_data = self.state_manager.xml_manager.get_layers()[index].copy()
        layer_data[key] = value
        self.state_manager.apply_change({
            "type": "update_layer",
            "index": index,
            "data": layer_data
    })

    def add_layer(self):
        default_layer = {
            "name": "NewLayer",
            "materialType": "DefaultMaterial",
            "height": "10",
            "panelDensity": "1.0",
            "localWaveCalcType": "none"
        }
        self.state_manager.apply_change({"type": "add_layer", "data": default_layer})
        self.load_data()

    def delete_last_layer(self):
        layers = self.state_manager.xml_manager.get_layers()
        if layers:
            self.state_manager.apply_change({"type": "delete_layer", "index": len(layers) - 1})
            self.load_data()
        else:
            QMessageBox.information(self, "No Layers", "No layers to delete.")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.load_data()

    def toggle_display(self):
        self.show_display = not self.show_display
        self.load_data()

    def refresh(self):
        self.load_data()
