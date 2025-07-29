from lxml import etree as ET
import copy

class XMLManager:
    def __init__(self):
        self.tree = None
        self.root = None

    def load_file(self, filepath):
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()

    def save_file(self, filepath):
        if self.root is not None:
            try:
                print(f"[XMLManager] Saving file to: {filepath}")
                tree = ET.ElementTree(self.root)  # Build tree from updated root
                tree.write(filepath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
                print("[XMLManager] File saved successfully.")
            except Exception as e:
                print(f"[XMLManager] Error saving file: {e}")
        else:
            print("[XMLManager] No root element to save.")

    def get_raw_xml(self, target_tag=None):
        if self.tree is not None:
            if target_tag:
                matches = self.root.findall(f".//{target_tag}")
                if matches:
                    return ET.tostring(matches[0], pretty_print=True, encoding="unicode")
            return ET.tostring(self.tree, pretty_print=True, encoding="unicode")
        return "No XML loaded."
    
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
        
    def update_layer_parameter(self, index, key, value):
        layers = self.root.findall(".//LayeredStructure/Layer")
        if 0 <= index < len(layers):
            layer = layers[index]
            if key in layer.attrib:
                layer.set(key, value)
            else:
                
                layer.set(key, value)
        else:
            print(f"[XMLManager] Layer index {index} out of range.")
    def get_pretty_xml(self):
        if self.tree is not None:
            return ET.tostring(self.tree, pretty_print=True).decode()
        return ""
    def get_all_param_names(self):
        param_names = set()

        def recurse(node):
            if isinstance(node.tag, str) and 'value' in node.attrib:
                param_names.add(node.tag)
            for child in node:
                recurse(child)

        if self.tree is not None:
            recurse(self.tree.getroot())

        return sorted(param_names)
    def get_param_to_section_map(self, full_path=False):
        param_to_section = {}

        def recurse(node, section_path=""):
            tag = node.tag
            current_path = f"{section_path} > {tag}" if section_path else tag

            if isinstance(tag, str) and 'value' in node.attrib:
                if full_path:
                    param_to_section[tag] = current_path
                else:
                    param_to_section[tag] = section_path.split(" > ")[-1]

            for child in node:
                recurse(child, current_path)

        if self.tree is not None:
            recurse(self.tree.getroot())

        return param_to_section
        
    def remove_layer(self, index):
        layers_parent = self.root.find("./LayeredStructure")
        layers = layers_parent.findall("Layer")
        if 0 <= index < len(layers):
            print(f"[XMLManager] Removing layer at index {index}")
            layers_parent.remove(layers[index])

    def remove_material(self, index):
        materials_parent = self.root.find("./MaterialList")
        materials = materials_parent.findall("Material")
        if 0 <= index < len(materials):
            print(f"[XMLManager] Removing material at index {index}")
            materials_parent.remove(materials[index])
        

    def update_material_parameter(self, index, key, value):
        materials = self.root.findall(".//MaterialList/Material")
        if 0 <= index < len(materials):
            material = materials[index]
            for child in material:
                if child.tag == key:
                    child.set("value", value)
                    break
            else:
                # Add new element if key doesn't exist
                new_elem = ET.Element(key)
                new_elem.set("value", value)
                material.append(new_elem)
        else:
            print(f"[XMLManager] Material index {index} out of range.")
    def set_value(self, xpath, value):

        if not self.root:
            print("[XMLManager] No XML loaded.")
            return

        element = self.root.find(xpath)
        if element is not None:
            element.set("value", value)
        else:
            print(f"[XMLManager] No element found at path: {xpath}")
