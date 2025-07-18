from PyQt5.QtWidgets import QMainWindow,QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from functools import partial
from Gui.MainWindow import MainWindow
from State.StateManager import StateManager

class InitialWindow(QMainWindow):
    def __init__(self, state_manager):
        super().__init__()
        self.setWindowTitle("Select XML File")
        self.setGeometry(200, 200, 400, 200)

        self.state_manager = state_manager
        

        layout = QVBoxLayout()
        default_btn = QPushButton("Load Defaults")
        custom_btn = QPushButton("Load Custom XML")
        self.label = QLabel("Drag and drop XML here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed gray; padding: 20px;")
        self.open_file_dialog()
        default_btn.clicked.connect(partial(self.launch_main_window, "assets/Defaults.xml"))
        custom_btn.clicked.connect(self.select_custom_xml)

        container = QWidget()
        container.setLayout(layout)
        layout.addWidget(default_btn)
        layout.addWidget(custom_btn)
        layout.addWidget(self.label)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)

    def select_custom_xml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if path:
            self.launch_main_window(path)

    def launch_main_window(self, xml_path):
        self.state_manager.open_file(xml_path)
        self.main_window = MainWindow(self.state_manager)
        self.main_window.show()
        self.close()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.endswith(".xml"):
                self.launch_main_window(path)
            else:
                QMessageBox.critical(self, "Invalid File", "Only .xml files are supported.")


    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML Files (*.xml)")
        if path:
            self.launch_main_windows(path)

    def launch_main_windows(self, xml_path):
        state_manager = StateManager()
        state_manager.open_file(xml_path)

        self.main_window = MainWindow(state_manager)
        self.main_window.show()

        self.raw_window = QMainWindow()
        self.raw_window.setWindowTitle("Raw XML Viewer")
        self.raw_window.resize(800, 600)
        self.raw_editor = QTextEdit()
        self.raw_editor.setReadOnly(True)
        self.raw_editor.setPlainText(state_manager.xml_manager.get_raw_xml())
        self.raw_window.setCentralWidget(self.raw_editor)
        self.raw_window.show()
