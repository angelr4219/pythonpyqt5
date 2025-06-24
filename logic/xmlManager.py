# logic/xml_manager.py
from lxml import etree as ET

class XMLManager:
    def __init__(self):
        self.tree = None
        self.root = None

    def load_file(self, filepath):
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()

    def get_parameter(self, path):
        return self.root.find(path)

    def update_value(self, path, value):
        node = self.root.find(path)
        if node is not None:
            node.set("value", value)

    def save_file(self, filepath):
        ET.indent(self.tree, '    ')
        self.tree.write(filepath, encoding='utf-8', xml_declaration=True)
