#logic.tooltip.py
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtCore import QPoint,QTimer
from logic.ParameterDocs import parameter_docs

_active_timer = None 

def show_parameter_tooltip(widget, parameter_name):
    """Show tooltip next to widget for a given parameter name."""
    message = parameter_docs.get(parameter_name, f"No documentation found for {parameter_name}.")
    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget)



def show_parameter_tooltip_persistent(widget, label, duration=60000):
    global _active_timer

    try:
        if _active_timer is not None and _active_timer.isActive():
            _active_timer.stop()
    except RuntimeError:
        _active_timer = None

    QToolTip.showText(widget.mapToGlobal(widget.rect().bottomLeft()), label, widget)

    _active_timer = QTimer(widget)
    _active_timer.setSingleShot(True)
    _active_timer.timeout.connect(lambda: QToolTip.hideText())
    _active_timer.start(duration)