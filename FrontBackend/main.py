# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.initialWindow import InitialWindow
from gui.mainWindow import MainWindow
from logic.xmlManager import XMLManager


if __name__ == "__main__":
    app = QApplication(sys.argv)
    

    window = InitialWindow()
   # window = MainWindow("FrontBackend/assets/DotArray2 2.xml")
    window.show()
    
    sys.exit(app.exec_())

