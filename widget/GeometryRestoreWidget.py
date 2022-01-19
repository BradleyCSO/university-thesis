from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QWidget


class GeometryRestoreWidget(QWidget):
    """
    Simple widget which saves geometry to
    QSettings on close event and loads again
    on a show event
    """
    name = None

    def __init__(self, name, parent=None):
        """
        Construct with optional parent

        :param parent: Parent widget
        """
        super().__init__(parent)
        self.name = name

    def showEvent(self, ev):
        # Save geometry
        settings = QSettings("bsco", "project")
        geo = settings.value(self.name + "/geo")
        if geo is not None:
            self.restoreGeometry(geo)

        # Defer to super
        super().showEvent(ev)

    def closeEvent(self, ev):
        # Save geometry
        settings = QSettings("bsco", "project")
        settings.setValue(self.name + "/geo", self.saveGeometry())

        # Defer to super
        super().closeEvent(ev)
