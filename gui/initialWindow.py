# gui/initial_window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog,QLabel
from functools import partial
from gui.mainWindow import MainWindow
from PyQt5.QtCore import Qt



class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select File")
        self.resize(400, 200)
        self.setAcceptDrops(True)

        self.label = QLabel("Drag and drop an XML file here", alignment=Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed gray; padding: 20px;")
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

        default_btn = QPushButton("Load Defaults")
        custom_btn = QPushButton("Load Custom XML")

        layout.addWidget(default_btn)
        layout.addWidget(custom_btn)
        layout.addWidget(self.label)

        default_btn.clicked.connect(partial(self.launch_main_window, "assets/Defaults.xml"))
        custom_btn.clicked.connect(self.select_custom_xml)

    def select_custom_xml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if file_path:
            self.launch_main_window(file_path)

    def launch_main_window(self, xml_path):
        print(f"Launching with: {xml_path}")
        self.main_window = MainWindow(xml_path)
        self.main_window.show()
        self.close()

    def dragEnterEvent(self, event):
        self.setAcceptDrops(True)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.setAcceptDrops(True)
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.endswith(".xml"):
                self.launch_main_window(path)


#from running main application, we get into initial window, which allows us to select a file to edit or just look at.
#this has buttons which allow us to load defaults or custom XML files.
## The selected XML file is then passed to the MainWindow for editing.