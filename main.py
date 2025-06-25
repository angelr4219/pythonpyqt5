# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.initialWindow import InitialWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #styling.qss
    try:
        with open("style.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("style.qss not found, running without custom styles")

    
    window = InitialWindow()
    window.show()
    sys.exit(app.exec_())

