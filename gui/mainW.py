
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem,
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QAction, QSplitter, QStatusBar
)
from PyQt5.QtCore import Qt



   
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML Editor GUI")
        self.setGeometry(100, 100, 900, 600)

        self._create_menu()
        self._create_widgets()
        self._create_layout()
        self._create_status_bar()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open XML", self)
        save_action = QAction("Save XML", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        # Hook up later
        open_action.triggered.connect(self._open_xml)
        save_action.triggered.connect(self._save_xml)

    def _create_widgets(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Tag", "Attributes"])

        self.tag_input = QLineEdit()
        self.attr_input = QLineEdit()
        self.text_input = QTextEdit()

        self.save_btn = QPushButton("Save Changes")
        self.add_btn = QPushButton("Add Element")
        self.del_btn = QPushButton("Delete Element")

    def _create_layout(self):
        editor = QWidget()
        editor_layout = QVBoxLayout()

        editor_layout.addWidget(QLabel("Tag Name:"))
        editor_layout.addWidget(self.tag_input)

        editor_layout.addWidget(QLabel("Attributes:"))
        editor_layout.addWidget(self.attr_input)

        editor_layout.addWidget(QLabel("Text Content:"))
        editor_layout.addWidget(self.text_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        editor_layout.addLayout(btn_layout)

        editor.setLayout(editor_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(editor)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

    def _create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def _open_xml(self):
        # Placeholder
        self.status.showMessage("Open XML clicked")

    def _save_xml(self):
        # Placeholder
        self.status.showMessage("Save XML clicked")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
