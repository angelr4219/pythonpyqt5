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

    def get_layers(self):
        layers = self.root.find("./LayeredStructure")
        return [self._element_to_dict(layer) for layer in layers.findall("Layer")]

    def set_layer(self, index, layer_data):
        layers = self.root.find("./LayeredStructure").findall("Layer")
        if 0 <= index < len(layers):
            self._update_element_from_dict(layers[index], layer_data)

    def get_materials(self):
        materials = self.root.find("./MaterialList")
        return [self._element_to_dict(material) for material in materials.findall("Material")]

    def set_material(self, index, material_data):
        materials = self.root.find("./MaterialList").findall("Material")
        if 0 <= index < len(materials):
            self._update_element_from_dict(materials[index], material_data)

    def _element_to_dict(self, element):
        return {child.tag: child.attrib.get("value", "") for child in element}

    def _update_element_from_dict(self, element, data_dict):
        for child in element:
            if child.tag in data_dict:
                child.set("value", data_dict[child.tag])

    def add_layer(self, layer_data):
        layered_structure = self.root.find("./LayeredStructure")
        new_layer = ET.Element("Layer")
        for key, value in layer_data.items():
            sub_elem = ET.Element(key)
            sub_elem.set("value", value)
            new_layer.append(sub_elem)
        layered_structure.append(new_layer)

    def add_material(self, material_data):
        material_list = self.root.find("./MaterialList")
        new_material = ET.Element("Material")
        for key, value in material_data.items():
            sub_elem = ET.Element(key)
            sub_elem.set("value", value)
            new_material.append(sub_elem)
        material_list.append(new_material)
