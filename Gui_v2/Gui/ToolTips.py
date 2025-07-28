from PyQt5.QtWidgets import QToolTip
from PyQt5.QtCore import QPoint, QTimer
from Logic.ParameterDocs import ParameterDocs

_active_timer = None


def setup_tooltips(widget, parameter_name, duration=60000):
    global _active_timer
    message = ParameterDocs.get(parameter_name, f"No documentation found for {parameter_name}.")

    if _active_timer is not None and _active_timer.isActive():
        _active_timer.stop()

    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget)

    _active_timer = QTimer()
    _active_timer.setSingleShot(True)
    _active_timer.timeout.connect(QToolTip.hideText)
    _active_timer.start(duration)


def show_parameter_tooltip(widget, parameter_name):
    message = ParameterDocs.get(parameter_name)
    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), message, widget)


def show_parameter_tooltip_persistent(widget, parameter_name):

    tooltip = ParameterDocs.get(parameter_name, f"No documentation found for {parameter_name}.")
    widget.setToolTip(tooltip)  # hover-based
    QToolTip.showText(widget.mapToGlobal(QPoint(10, widget.height())), tooltip, widget)  # one-time popup
