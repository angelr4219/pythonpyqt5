from PyQt5.QtWidgets import QToolTip
from PyQt5.QtCore import QPoint, QTimer
from Logic.ParameterDocs import ParameterDocs

_active_timer = None

def setup_tooltips(widget, parameter_name, duration=60000):
    global _active_timer
    message = ParameterDocs.get(parameter_name, f"No documentation for {parameter_name}")

    if _active_timer is not None and _active_timer.isActive():
        _active_timer.stop()
    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget)

    _active_timer = QTimer()
    _active_timer.setSingleShot(True)
    _active_timer.timeout.connect(QToolTip.hideText)
    _active_timer.start(duration)
