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
        ls = self.root.find("./LayeredStructure")
        if ls is None:
            print("Warning: No <LayeredStructure> found in XML.")
            return []
        return ls.findall("Layer")

    def get_materials(self):
        ml = self.root.find("./MaterialList")
        if ml is None:
            print(" Warning: No <MaterialList> found in XML.")
            return []
        return ml.findall("Material")
    def add_material(self, material_dict):
        ml = self.root.find("./MaterialList")
        if ml is None:
            print("[x] No <MaterialList> found in XML.")
            return
        new_elem = ET.Element("Material")
        for key, value in material_dict.items():
            sub_elem = ET.Element(key)
            sub_elem.set("value", value)
            new_elem.append(sub_elem)
        ml.append(new_elem)
        print("[ok] Added new material.")

    

    def update_layer(self, index, key, value):
        layers = self.get_layers()
        if not (0 <= index < len(layers)):
            print(f"[x] Layer index {index} out of range.")
            return

        element = layers[index].find(key)
        if element is None:
            print(f"[x] Layer {index} missing tag <{key}>.")
            return

        old_value = element.attrib.get("value", "<none>")
        element.set("value", value)
        print(f"[ok] Updated Layer {index} <{key}>: {old_value} → {value}")