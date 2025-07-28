from PyQt5.QtCore import QObject, pyqtSignal
from Logic.XMLManager import XMLManager
import copy

class StateManager(QObject):
    xml_updated = pyqtSignal()
    file_loaded = pyqtSignal(str)
    file_saved = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.xml_manager = XMLManager()
        self.current_file = None
        self.unsaved_changes = False
        self.undo_stack = []
        self.redo_stack = []
        self.action_history = []

    def open_file(self, filepath):
        self.xml_manager.load_file(filepath)
        self.current_file = filepath
        self.unsaved_changes = False
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.action_history.clear()
        self.file_loaded.emit(filepath)

    def save_file(self, filepath=None):
        if filepath is None:
            filepath = self.current_file
        if filepath:
            print(f"[StateManager] Saving to {filepath}")
            self.xml_manager.save_file(filepath)
            self.set_unsaved_changes(False)
            self.file_saved.emit(filepath)

    def get_root(self):
        if self.xml_manager.tree:
            return self.xml_manager.tree.getroot()
        return None
    def has_tree(self):
        return self.xml_manager.tree is not None


    def apply_change(self, action, record_undo=True):
        if record_undo:
            reverse_action = self.generate_reverse_action(action)
            self.undo_stack.append(reverse_action)
            self.action_history.append(action)
            self.redo_stack.clear()

        self.unsaved_changes = True

        action_type = action.get("type")
        if action_type == "update_layer":
            self.xml_manager.set_layer(action["index"], action["data"])
        elif action_type == "update_material":
            self.xml_manager.set_material(action["index"], action["data"])
        elif action_type == "add_layer":
            self.xml_manager.add_layer(action["data"])
        elif action_type == "add_material":
            self.xml_manager.add_material(action["data"])
        else:
            print(f"[StateManager] Unknown action: {action}")

        self.xml_updated.emit()

    def generate_reverse_action(self, action):
        if action["type"] == "add_layer":
            layers = self.xml_manager.get_layers()
            if layers:
                return {"type": "remove_layer", "index": len(layers) - 1}
        elif action["type"] == "add_material":
            materials = self.xml_manager.get_materials()
            if materials:
                return {"type": "remove_material", "index": len(materials) - 1}
        elif action["type"] == "update_layer":
            current_data = self.xml_manager.get_layers()[action["index"]]
            return {"type": "update_layer", "index": action["index"], "data": current_data}
        elif action["type"] == "update_material":
            current_data = self.xml_manager.get_materials()[action["index"]]
            return {"type": "update_material", "index": action["index"], "data": current_data}
        else:
            print("[StateManager] No reverse action for type:", action["type"])
            return action

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo")
            return
        action = self.undo_stack.pop()
        self.apply_change(action, record_undo=False)
        self.redo_stack.append(action)
        print("Undo applied")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo")
            return
        action = self.redo_stack.pop()
        self.apply_change(action)
        print("Redo applied")

    def has_unsaved_changes(self):
        return self.unsaved_changes
    def refresh(self):
        self.load_data()
    def set_unsaved_changes(self, changed=True):
        self.unsaved_changes = changed
        self.xml_updated.emit()



