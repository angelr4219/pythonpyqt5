from PyQt5.QtWidgets import QToolTip
from PyQt5.QtCore import QPoint,QTimer
from logic.ParameterDocs import parameter_docs

_active_timer = None 

def show_parameter_tooltip(widget, parameter_name):
    """Show tooltip next to widget for a given parameter name."""
    message = parameter_docs.get(parameter_name, f"No documentation found for {parameter_name}.")
    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget)



def show_parameter_tooltip_persistent(widget, parameter_name):
    from logic.ParameterDocs import parameter_docs
    global _active_timer

    def refresh_tooltip():
        message = parameter_docs.get(parameter_name, f"No documentation found for {parameter_name}.")
        QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget, widget.rect(), 2000)

    if _active_timer:
        _active_timer.stop()

    _active_timer = QTimer(widget)
    _active_timer.timeout.connect(refresh_tooltip)
    _active_timer.start(1500)  # Refresh every 1.5 seconds

    widget.destroyed.connect(_active_timer.stop)
