from logic.xmlManager import XMLManager
from PyQt5.QtWidgets import QMainWindow, QGroupBox, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea, QLineEdit,  QMessageBox,QMenuBar, QAction, QFontDialog ,QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QFileDialog, QTreeWidgetItem
from gui.layerWindow import LayerWindow
from xml.etree.ElementTree import Element

class MainWindow(QMainWindow):
    def __init__(self, xml_path):
        super().__init__()
        self.setWindowTitle("XML Editor GUI")
        self.setGeometry(100, 100, 900, 600)


        self.xml_manager = XMLManager()
        self.xml_path = xml_path
        self.xml_manager.load_file(xml_path)
        #loads the XML file using the XMLManager class.
        self.root = self.xml_manager.root
        # gets the root element of the XML file.

        

        self.create_menu()
        self.create_widgets()
        self.create_layout()
        self.create_status_bar()

        self.combo = QComboBox()
        self.combo.addItems([child.tag for child in self.root])
        self.combo.currentIndexChanged.connect(self.display_section)

        

    def open_xml_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if filepath:
            self.xml_manager.load_file(filepath)
            self.current_file = filepath
            self.tree.clear()
            self.populate_tree()
            self.status.showMessage(f"Loaded: {filepath}")

    def save_xml(self):
        if not self.current_file:
            filepath, _ = QFileDialog.getSaveFileName(self, "Save XML File", "", "XML Files (*.xml)")
        else:
            filepath = self.current_file
        if filepath:
            self.xml_manager.save_file(filepath)
            self.status.showMessage(f"Saved to: {filepath}")

    def populate_tree(self):
        def add_items(parent_widget, parent_elem):
            for child in parent_elem:
                tag, attrs = self.xml_manager.get_element_info(child)
                item = QTreeWidgetItem([tag, attrs])
                parent_widget.addChild(item)
                add_items(item, child)

        root = self.xml_manager.get_element_tree()
        if root is not None:
            top = QTreeWidgetItem([root.tag, ""])
            self.tree.addTopLevelItem(top)
            add_items(top, root)
            self.tree.expandAll()

    def create_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open XML", self)
        save_action = QAction("Save XML As...", self)

        open_action.triggered.connect(self.open_xml_file)
        save_action.triggered.connect(self.save_xml)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)


    def create_widgets(self):
        self.combo = QComboBox()
        self.combo.addItems([child.tag for child in self.root])
        self.combo.currentIndexChanged.connect(self.display_section)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.save_btn = QPushButton("Save XML")
        self.save_btn.clicked.connect(self.save_xml)

    def create_layout(self):
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.save_btn)

        self.display_section(0)  # Load initial content
    def create_status_bar(self):
        self.status = self.statusBar()
        self.status.showMessage("Ready")
    
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




    
