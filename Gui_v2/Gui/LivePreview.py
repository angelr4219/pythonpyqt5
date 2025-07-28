from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QFont, QTextCharFormat, QSyntaxHighlighter, QColor, QClipboard
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QApplication


class XMLHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("blue"))
        self.highlighting_rules.append((QRegExp("</?\\b[^>]+>"), tag_format))

        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("darkgreen"))
        self.highlighting_rules.append((QRegExp("\\b\\w+(?=\\=)"), attribute_format))

        value_format = QTextCharFormat()
        value_format.setForeground(QColor("red"))
        self.highlighting_rules.append((QRegExp('\"[^"]*\"'), value_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)

class LivePreviewWidget(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier New", 10))
        self.layout.addWidget(self.text_edit)

        self.highlighter = XMLHighlighter(self.text_edit.document())

        # Toolbar buttons
        button_layout = QHBoxLayout()

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_btn)

        self.word_wrap_checkbox = QCheckBox("Word Wrap")
        self.word_wrap_checkbox.setChecked(True)
        self.word_wrap_checkbox.stateChanged.connect(self.toggle_word_wrap)
        button_layout.addWidget(self.word_wrap_checkbox)

        self.refresh_btn = QPushButton("Refresh Manually")
        self.refresh_btn.clicked.connect(self.refresh_preview)
        button_layout.addWidget(self.refresh_btn)

        self.layout.addLayout(button_layout)

        # Initial rendering
        self.refresh_preview()
        self.state_manager.xml_updated.connect(self.refresh_preview)

    def refresh_preview(self):
        xml_string = self.state_manager.xml_manager.get_pretty_xml()
        self.last_valid_xml = xml_string
        self.text_edit.setPlainText(xml_string)

    def handle_text_change(self):
        current = self.text_edit.toPlainText()
        for keyword in self.locked_keywords:
            if self._locked_section_modified(current, keyword):
                self.text_edit.blockSignals(True)
                self.text_edit.setPlainText(self.last_valid_xml)
                self.text_edit.blockSignals(False)
                return
        self.last_valid_xml = current  # update if valid

    def _locked_section_modified(self, new_text, keyword):
        return keyword not in new_text or new_text.count(keyword) != self.last_valid_xml.count(keyword)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def toggle_word_wrap(self, state):
        self.text_edit.setLineWrapMode(
            QPlainTextEdit.WidgetWidth if state == Qt.Checked else QPlainTextEdit.NoWrap
        )