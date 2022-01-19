from core import AppCore
from widget.GeometryRestoreWidget import GeometryRestoreWidget


class ModeWidget(GeometryRestoreWidget):
    core = AppCore()

    def __init__(self, name, parent=None):
        """
        Construct

        :param name: Widget name
        :param parent: Widget parent
        """
        super().__init__(name, parent)

    def showEvent(self, ev):
        self.core.launcher.hide()
        super().showEvent(ev)

    def closeEvent(self, ev):
        self.core.launcher.show()
        super().closeEvent(ev)
