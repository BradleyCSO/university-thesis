from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QChart

from gen.ui_ChartWidget import Ui_ChartWidget


class ChartWidget(QWidget):
    """
    Simple widget containing a chart view
    """
    ui = None

    def __init__(self, parent=None):
        """
        Create new widget with default parent

        :param parent: Parent widget
        """
        super().__init__(parent)
        self.ui = Ui_ChartWidget()
        self.ui.setupUi(self)
