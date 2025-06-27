# logic/xml_manager.py
from lxml import etree as ET

class XMLManager:
    def __init__(self):
        self.tree = None
        self.root = None
        # Initialize the XMLManager with no tree or root element

    def load_file(self, filepath):
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        # Load an XML file and set the root element

    def get_parameter(self, path):
        return self.root.find(path)
    # Get a parameter from the XML tree by its path

    def update_value(self, path, value):
        node = self.root.find(path)
        if node is not None:
            node.set("value", value)
    # Update the value of a node in the XML tree by its path

    def save_file(self, filepath):
        ET.indent(self.tree, '    ')
        self.tree.write(filepath, encoding='utf-8', xml_declaration=True)
# Save the XML tree to a file with proper indentation and encoding
    
    def get_element_tree(self):
        return self.root
    # Get the root element of the XML tree

    def get_element_info(self, element):
        tag = element.tag
        attribs = ", ".join([f'{k}={v}' for k, v in element.attrib.items()])
        return tag, attribs
    # Get the tag and attributes of an element as a string
    
    def update_element(self, element, tag=None, attribs=None, text=None):
        if tag:
            element.tag = tag
        if attribs:
            element.attrib.clear()
            element.attrib.update(attribs)
        if text is not None:
            element.text = text

    def add_element(self, parent, tag="NewTag", attrib=None, text=None):
        attrib = attrib or {}
        new_elem = ET.SubElement(parent, tag, attrib)
        new_elem.text = text
        return new_elem

    def delete_element(self, parent, element):
        parent.remove(element)

    def save_file(self, filepath):
        ET.indent(self.tree, space="    ")
        self.tree.write(filepath, encoding='utf-8', xml_declaration=True)