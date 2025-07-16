# main.py

import sys
from PyQt5.QtWidgets import QApplication
from Gui.InitialWindow import InitialWindow
from Gui.MainWindow import MainWindow
from Logic.XMLManager import XMLManager
from State.StateManager import StateManager


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    state_manager = StateManager()
    window = InitialWindow(state_manager)  # Pass state_manager here
    window.show()
    
    sys.exit(app.exec_())
    #test

