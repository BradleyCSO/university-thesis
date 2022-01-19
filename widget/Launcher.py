from PyQt5.QtCore import Qt, QSortFilterProxyModel

from core import AppCore
from qt import ModeModel, ItemRoles
from widget.AnalysisWidget import AnalysisWidget
from widget.CurrencyDisplay import CurrencyDisplay
from widget.GeometryRestoreWidget import GeometryRestoreWidget
from widget.StockTimeSeriesDisplay import StockTimeSeriesDisplay
from widget.DollarIndexDisplay import DollarIndexDisplay

from gen.ui_Launcher import Ui_Launcher


class Launcher(GeometryRestoreWidget):
    """
    Launcher widget which allows the
    user to select which application
    functionality they wish to use
    """
    # Generated UI
    ui = None

    # App core
    core = AppCore()

    # Model for mode list
    model = None
    sort_model = None

    def __init__(self, parent=None):
        """
        Constructor with optional
        parent

        :param parent: Parent widget
        """
        super().__init__("Launcher", parent)

        # Initialise generated UI
        self.ui = Ui_Launcher()
        self.ui.setupUi(self)

        # Size (fixed)
        self.setFixedWidth(700)
        self.setFixedHeight(400)

        # Create empty model
        self.model = ModeModel(self)
        self.sort_model = QSortFilterProxyModel()
        self.sort_model.setSourceModel(self.model)
        self.sort_model.setSortRole(Qt.DisplayRole)

        # Set model to view and increase text size
        self.ui.modeView.setModel(self.sort_model)
        self.ui.modeView.setStyleSheet("font: 18px;")

        # Connect load signal
        self.ui.modeView.clicked.connect(self.launch_mode_widget)

    def setup_application_widgets(self):
        """
        Setup all the widgets which will be used in
        the application
        """
        # Create stock time series displays
        self.core.stock_time_series_window = StockTimeSeriesDisplay()
        self.core.stock_time_series_window.setWindowFlags(Qt.Window)
        self.core.stock_time_series_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self.core.stock_time_series_analysis_window = AnalysisWidget(self.core.stock_time_series_window)
        self.core.stock_time_series_analysis_window.setWindowFlags(Qt.Window)

        # Create currency display
        self.core.currency_window = CurrencyDisplay()

        # Create dollar index display
        self.core.dollar_index_window = DollarIndexDisplay()

        # Add modes to view
        self.model.add_mode("Stock Time Series (NYSE/NASDAQ)",
                            "Search and analyse US stocks over a period of time",
                            self.core.stock_time_series_window)

        self.model.add_mode("Currency (FOREX)",
                            "Analyse data for common foreign exchange and crypto-currency pairings",
                            self.core.currency_window)

        self.model.add_mode("US Dollar Index (USDX/DXY)",
                            "Display visual breakdown for US dollar index over time",
                            self.core.dollar_index_window)

        # Sort options alphabetically
        self.sort_model.sort(0, Qt.AscendingOrder)

    def launch_mode_widget(self, index):
        """
        Show the widget that has been launched by
        the user

        :param index: Index clicked
        """
        widget = self.sort_model.data(index, ItemRoles.MODE_WIDGET_ROLE)
        if widget is not None:
            widget.show()
