import sys
from functools import partial
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QListWidget,
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QFrame,
    QCheckBox, QFileDialog, QMessageBox
)
import lxml.etree as ET

#this script creates a simple GUI application that allows users to select an XML file,
class MainWindow(QMainWindow):
    # The main window of the application
    def __init__(self):
        super().__init__() # Initialize the main window
        self.setWindowTitle("Input File Generator") # Set the title of the main window
        self.setGeometry(100, 100, 600, 400) #(x,y,width, height)
        self.setFont(QFont("Arial", 10)) # Set the font for the application

        layout = QVBoxLayout() # Create a vertical layout for the main window

        # File selection
        file_layout = QHBoxLayout() # Create a horizontal layout for file selection
        self.file_label = QLabel("No file selected") # Label to show selected file 
        select_button = QPushButton("Select XML File")  # Button to select an XML file
        select_button.clicked.connect(self.select_xml_file) # Connect the button click to the select_xml_file method
        file_layout.addWidget(select_button) # Add the button to the file layout 
        file_layout.addWidget(self.file_label) # Add the label to the file layout
        layout.addLayout(file_layout)  # Add the file layout to the main layout

        # Input field example
        self.input_field = QLineEdit()
        layout.addWidget(QLabel("Example Parameter Input:"))
        layout.addWidget(self.input_field)

        # Check box
        self.checkbox = QCheckBox("Enable Feature")
        layout.addWidget(self.checkbox)

        # Combo box
        self.combo = QComboBox()
        self.combo.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addWidget(self.combo)

        # Write button
        write_button = QPushButton("Generate XML")
        write_button.clicked.connect(self.write_xml)
        layout.addWidget(write_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
# and generate a new XML file based on user inputs.
    def select_xml_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select XML File", "", "XML Files (*.xml)")
        if file_path:
            self.file_label.setText(file_path)
            self.load_xml(file_path)

    # Load the XML file and display its root tag
    def load_xml(self, path):
        try:
            self.tree = ET.parse(path)
            self.root = self.tree.getroot()
            QMessageBox.information(self, "XML Loaded", f"Root tag: {self.root.tag}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load XML: {e}")
    
    # Write user inputs to a new XML file
    def write_xml(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Save XML", "", "XML Files (*.xml)")
        if not output_path:
            return
        root = ET.Element("GeneratedParameters")
        param = ET.SubElement(root, "Parameter", value=self.input_field.text(), type="string")
        enabled = ET.SubElement(root, "FeatureEnabled", value=str(self.checkbox.isChecked()), type="bool")
        choice = ET.SubElement(root, "SelectedOption", value=self.combo.currentText(), type="string")
        tree = ET.ElementTree(root)
        tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="utf-8")
        QMessageBox.information(self, "Success", f"File saved to {output_path}")


# Classes to represent the structure of the XML file
class Layer:
    def __init__(self, name, materialType, height, panelDensity, localWaveCalcType):
        self.name = name
        self.materialType = materialType
        self.height = height
        self.panelDensity = panelDensity
        self.localWaveCalcType = localWaveCalcType
# Classes to represent the materials used in the layers
class Material:
    def __init__(self, name, dielectricConstant, effectiveMass_x, effectiveMass_y, effectiveMass_z, bandShift, backgroundDopingDensity):
        self.name = name
        self.dielectricConstant = dielectricConstant
        self.effectiveMass_x = effectiveMass_x
        self.effectiveMass_y = effectiveMass_y
        self.effectiveMass_z = effectiveMass_z
        self.bandShift = bandShift
        self.backgroundDopingDensity = backgroundDopingDensity
        # Classes to represent the wave calculations
  
class XMLReader:
    def __init__(self):
    
        self.inputXmlParse = None # = ET.parse(...)
        self.inputXmlRoot = None # = self.inputXmlParse.getroot()
        self.tree = None
    def importXML(self, pathToXml):
        self.inputXmlParse = ET.parse(pathToXml)
        self.inputXmlRoot = self.inputXmlParse.getroot()
        self.tree = ET.ElementTree(self.inputXmlRoot)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
