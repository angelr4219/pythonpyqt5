from PyQt5.QtWidgets import QLineEdit, QCompleter, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt
import difflib
from Logic.ParameterDocs import ParameterDocs

class ParameterSearchBar(QLineEdit):
    def __init__(self, xml_manager, parent_window):
        super().__init__()
        self.xml_manager = xml_manager
        self.parent_window = parent_window

        self.setPlaceholderText("Search parameter")

        self.param_to_section = self.xml_manager.get_param_to_section_map(full_path=True)
        self.param_names = list(self.param_to_section.keys())

        self.dropdown = QListWidget()
        self.dropdown.setWindowFlags(Qt.Popup)
        self.dropdown.setFocusPolicy(Qt.NoFocus)
        self.dropdown.setFocusProxy(self)
        self.dropdown.setMouseTracking(True)
        self.dropdown.setUniformItemSizes(True)
        self.dropdown.itemClicked.connect(self.select_suggestion)

        self.textChanged.connect(self.show_suggestions)
        self.returnPressed.connect(self.jump_to_parameter)
        
        # Attach QCompleter using known parameter names
        self.completer = QCompleter(list(ParameterDocs.keys()))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)

        # Make sure it jumps when a suggestion is selected
        self.completer.activated[str].connect(
            lambda name: self.parent_window.parameter_editor.jump_to_parameter(name)
        )

    def show_suggestions(self, text):
        self.dropdown.clear()
        text = text.strip().lower()

        if not text:
            self.dropdown.hide()
            return

        matches = difflib.get_close_matches(text, self.param_names, n=10, cutoff=0.3)

        if not matches:
            self.dropdown.hide()
            return

        for name in matches:
            section = self.param_to_section.get(name, "Unknown")
            item = QListWidgetItem(f"{name}  [in {section}]")
            item.setData(Qt.UserRole, name)
            self.dropdown.addItem(item)

        self.dropdown.setMinimumWidth(self.width())
        self.dropdown.move(self.mapToGlobal(self.rect().bottomLeft()))
        self.dropdown.show()

    def select_suggestion(self, item):
        param = item.data(Qt.UserRole)
        self.setText(param)
        self.jump_to_parameter()
        self.dropdown.hide()

    def jump_to_parameter(self):
        name = self.text().strip()

        for editor in getattr(self.parent_window, "views", []):
            param_widgets = getattr(editor, "param_widgets", {})
            scroll_area = getattr(editor, "scroll_area", None)

            if name in param_widgets and scroll_area:
                widget = param_widgets[name]
                scroll_area.ensureWidgetVisible(widget)
                widget.setStyleSheet("background-color: yellow; border: 2px solid orange;")
                QTimer.singleShot(1500, lambda: widget.setStyleSheet(""))
                return

        QMessageBox.information(self, "Not Found", f"Parameter '{name}' not found.")
