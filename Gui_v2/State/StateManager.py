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

    def open_file(self, filepath):
        self.xml_manager.load_file(filepath)
        self.current_file = filepath
        self.unsaved_changes = False
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.file_loaded.emit(filepath)

    def save_file(self, filepath=None):
        if filepath is None:
            filepath = self.current_file
        if filepath:
            self.xml_manager.save_file(filepath)
            self.unsaved_changes = False
            self.file_saved.emit(filepath)

    def apply_change(self, action):
        # Action example: {"type": "update_layer", "index": 1, "data": {"height": "50"}}
        self.undo_stack.append(copy.deepcopy(action))
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

    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        # Actual undo logic would depend on storing both forward and backward changes
        print("Undo not fully implemented yet")

    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        self.apply_change(action)

    def has_unsaved_changes(self):
        return self.unsaved_changes