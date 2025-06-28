# logic/xml_manager.py
from lxml import etree as ET

class XMLManager:
    def __init__(self):
        self.tree = None
        self.root = None

    def load_file(self, filepath):
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()

    def save_file(self, filepath):
        ET.indent(self.tree, '    ')
        self.tree.write(filepath, encoding='utf-8', xml_declaration=True)

    def dump_pretty(self):
        return ET.tostring(self.root, pretty_print=True, encoding='unicode')

    def get_layers(self):
        return self.root.find(".//LayeredStructure").findall("Layer")

    def get_materials(self):
        return self.root.find(".//MaterialList").findall("Material")

    def update_layer(self, index, key, value):
        layers = self.get_layers()
        if index < len(layers):
            element = layers[index].find(key)
            if element is not None:
                element.set("value", value)