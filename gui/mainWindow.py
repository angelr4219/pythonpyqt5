# gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QGroupBox, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea, QLineEdit, QFileDialog, QMessageBox,QMenuBar, QAction, QFontDialog ,QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from logic.xmlManager import XMLManager
from gui.layerWindow import LayerWindow
from xml.etree.ElementTree import Element 

class MainWindow(QMainWindow):
    def __init__(self, xml_path):
        super().__init__()
        self.setWindowTitle("Edit Simulation Parameters")
        self.resize(800, 600)
        # Initialize the main window with a title and size.

        self.xml_path = xml_path
        self.xml_manager = XMLManager()
        self.xml_manager.load_file(xml_path)
        # Load the XML file using the XMLManager.

        self.root = self.xml_manager.root
        # Get the root element of the XML file.

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        # Create a central widget and layout for the main window.

        self.combo = QComboBox()
        self.combo.addItems([child.tag for child in self.root])
        self.combo.currentIndexChanged.connect(self.display_section)
        self.layout.addWidget(self.combo)
        # Create a combo box to select different sections of the XML file.

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        # Create a scroll area to display the contents of the selected section.

        self.save_btn = QPushButton("Save XML")
        self.save_btn.clicked.connect(self.save_xml)
        self.layout.addWidget(self.save_btn)

        self.display_section(0)

    def display_section(self, index):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        selected_element = self.root[index]  # <RunParameters>, <GateBias>, etc.
        self.add_parameter_widgets(selected_element, self.scroll_layout)

        # Optional special case for LayeredStructure
        if selected_element.tag == "LayeredStructure":
            edit_btn = QPushButton("Edit Layers")
            edit_btn.clicked.connect(self.open_layer_editor)
            self.scroll_layout.addWidget(edit_btn)

    def open_layer_editor(self):
        self.layer_window = LayerWindow(self.xml_manager)
        self.layer_window.show()

    def save_xml(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save XML File", "", "XML Files (*.xml)")
        if file_path:
            self.xml_manager.save_file(file_path)
            QMessageBox.information(self, "Saved", f"Saved to {file_path}")
        
    def add_parameter_widgets(self, element, layout, prefix=""):
         # Recursively add widgets for each parameter in the XML element.
         for child in element:
            full_path = f"{prefix}/{child.tag}" if prefix else child.tag

            # If child has sub-elements → create collapsible group
            if list(child):
                group_box = QGroupBox(child.tag)
                
                group_layout = QVBoxLayout()
                group_box.setLayout(group_layout)
                layout.addWidget(group_box)

                self.add_parameter_widgets(child, group_layout, full_path)
            elif isinstance(child, Element) and 'value' in child.attrib:
                # Leaf node with a 'value' attribute
                row = QWidget()
                row_layout = QHBoxLayout(row)

                label = QLabel(f"{child.tag} ({child.attrib.get('type', 'string')})")
                label.setToolTip(full_path)
                font = label.font()
                font.setBold(True)
                label.setFont(font)


# Create input field based on the type attribute
                input_field = QLineEdit(child.attrib["value"])
                input_field.setEnabled(True)
                input_field.setToolTip(f"Expected type: {child.attrib.get('type', 'string')}")
                input_field.textChanged.connect(
                    lambda val, path=full_path, field_type=child.attrib.get('type', 'string'), widget=input_field:
                    self.edit_value(path, val, field_type, widget)
                )


                row_layout.addWidget(label)
                row_layout.addWidget(input_field)
                layout.addWidget(row)


    def edit_value(self, path, new_value: str, field_type: str, widget: QLineEdit):
        try:
            # Validate type
            if field_type in ("int", "long"):
                int(new_value)
            elif field_type == "double":
                float(new_value)
            elif field_type == "bool":
                if new_value.lower() not in ("true", "false"):
                    raise ValueError()

            # Find and update the node
            node = self.xml_manager.root.find(path)
            if node is not None:
                node.set("value", new_value)

            widget.setStyleSheet("QLineEdit { background-color: white; }")
            widget.setToolTip(f"Expected type: {field_type}")

        except ValueError:
            widget.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
            widget.setToolTip(f"Invalid {field_type} value")
    def edit_section(self, index):
                selected_element = self.root[index]
                new_tag, ok = QInputDialog.getText(self, "Edit Section", "Enter new tag name:", QLineEdit.Normal, selected_element.tag)
                if ok and new_tag:
                    selected_element.tag = new_tag
                    self.combo.setItemText(index, new_tag)       