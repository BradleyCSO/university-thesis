from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget

from gen.ui_LoadingWidget import Ui_LoadingWidget


class LoadingWidget(QWidget):
    """
    Simple loading widget with an indicator
    """
    ui = None
    movie = None

    def __init__(self, parent=None):
        """
        Initialise the loading widget and load the
        resource

        :param parent: Parent widget
        """
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Initialise UI
        self.ui = Ui_LoadingWidget()
        self.ui.setupUi(self)

        # Modal
        self.setWindowModality(Qt.WindowModal)

        # Setup display
        self.movie = QMovie("widget/ajax-loader.gif")
        self.ui.loadingLabel.setMovie(self.movie)
        self.movie.start()

        # Tooltip
        self.setToolTip("Loading...")

        # Size
        self.setFixedWidth(80)
        self.setFixedHeight(80)
