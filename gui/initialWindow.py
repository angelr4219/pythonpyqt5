# gui/initial_window.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog
from functools import partial
from .mainWindow import MainWindow
from logic.xmlManager import XMLManager

class InitialWindow(QMainWindow):
    def __init__(self):
        # Initialize the initial window , with a title and two buttons for loading XML files.
        super().__init__()
        self.setWindowTitle("Select File")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

        default_btn = QPushButton("Load Defaults")
        custom_btn = QPushButton("Load Custom XML")

        # Create buttons for loading default XML and custom XML files.
        layout.addWidget(default_btn)
        layout.addWidget(custom_btn)

        default_btn.clicked.connect(partial(self.launch_main_window, "fullstack/assets/Defaults.xml"))
        custom_btn.clicked.connect(self.select_custom_xml)

    def select_custom_xml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if file_path:
            self.launch_main_window(file_path)

    def launch_main_window(self, xml_path):
        self.main_window = MainWindow(xml_path)
        self.main_window.show()
        self.close()

#from running main application, we get into initial window, which allows us to select a file to edit or just look at.
#this has buttons which allow us to load defaults or custom XML files.
## The selected XML file is then passed to the MainWindow for editing.