# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.initialWindow import InitialWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InitialWindow()
    window.show()
    sys.exit(app.exec_())

