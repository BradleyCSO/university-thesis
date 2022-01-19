from datetime import datetime, timedelta

from core import AppCore
from widget.ModeWidget import ModeWidget
from widget.LoadingWidget import LoadingWidget
from gen.ui_DollarIndexDisplay import Ui_DollarIndexDisplay
from qt import DollarIndexChart


class DollarIndexDisplay(ModeWidget):
    """
    Class which displays US dollar index figures
    """
    ui = None
    core = AppCore()
    first = True
    loading_widget = None
    chart = None
    widget = None

    def __init__(self, parent=None):
        """
        Create the display and load the initial data

        :param parent: Parent object
        """
        # Setup parent
        super().__init__("DollarIndexDisplay", parent)

        # Setup UI
        self.ui = Ui_DollarIndexDisplay()
        self.ui.setupUi(self)

        # Create and assign chart
        self.chart = DollarIndexChart()
        self.ui.chartView.setChart(self.chart)

        # Loading widget
        self.loading_widget = LoadingWidget(self)
        self.loading_widget.setVisible(True)
        self.loading_widget.move(self.rect().center() - self.loading_widget.rect().center())

        # Hide UI by default
        self.ui.chartView.setVisible(False)
        self.ui.horizontalWidget.setVisible(False)
        self.ui.buttonWidget.setVisible(False)

        # Connect up UI
        self.ui.button7d.pressed.connect(self.load_7d)
        self.ui.button30d.pressed.connect(self.load_30d)
        self.ui.button1y.pressed.connect(self.load_1y)
        self.ui.button5y.pressed.connect(self.load_5y)

    def resizeEvent(self, ev):
        """
        Executed on window resize, reorganises any
        widgets

        :param ev: Event
        """
        # Re-locate
        self.loading_widget.move(self.rect().center() - self.loading_widget.rect().center())

        # Defer to super
        super().resizeEvent(ev)

    def showEvent(self, ev):
        """
        If this is the first time the display has been
        shown, ensure the loading animation is set and
        perform the load

        :param ev: Show event
        """
        # Perform on first load
        if self.first:
            # Update with all display values
            self.build_display()

        # Defer to base
        return super().showEvent(ev)

    def get_current_index(self):
        """
        Calculate the current index value from the latest
        prices for each currency
        :return:
        """
        self.core.data_store.cursor.execute("SELECT close FROM dollar_index ORDER BY timestamp DESC LIMIT 1")
        index = self.core.data_store.cursor.fetchall()
        self.ui.currentText.setText(str(index[0][0]))

    def load_data_for_time(self, rng, title):
        """
        Load data for all currencies in the index for
        a provided time range

        :param rng: Range of time to load (back)
        :param title: Title of the chart
        """
        # List of values
        self.core.data_store.cursor.execute("SELECT timestamp,close FROM dollar_index WHERE timestamp > "
                                            + '\'' + str(rng.timestamp()) + '\'' + "ORDER BY timestamp DESC")
        values = self.core.data_store.cursor.fetchall()

        # Base for area
        self.core.data_store.cursor.execute("SELECT MIN(close) FROM dollar_index WHERE timestamp > "
                                            + '\'' + str(rng.timestamp()) + '\'')
        base = self.core.data_store.cursor.fetchall()

        # Setup chart
        self.chart.populate(title, values, base[0][0] - 5)

    def load_7d(self):
        """
        Load 7 days of USDX data
        """
        self.load_data_for_time(datetime.utcnow() - timedelta(days=7), "USDX 7 day")

    def load_30d(self):
        """
        Load 30 days of USDX data
        """
        self.load_data_for_time(datetime.utcnow() - timedelta(days=30), "USDX 30 day")

    def load_1y(self):
        """
        Load 1 year of USDX data
        """
        self.load_data_for_time(datetime.utcnow() - timedelta(days=365), "USDX 1 year")

    def load_5y(self):
        """
        Load 5 years of USDX data
        """
        self.load_data_for_time(datetime.utcnow() - timedelta(days=1825), "USDX 5 year")

    def build_display(self):
        """
        Process the results of the dollar index query to
        produce a chart containing USDX data
        """
        # Update current price
        self.get_current_index()

        # Load 30 day chart by default
        self.load_30d()

        # Reveal UI
        self.loading_widget.setVisible(False)
        self.ui.chartView.setVisible(True)
        self.ui.horizontalWidget.setVisible(True)
        self.ui.buttonWidget.setVisible(True)

        # Load dataset for regression
        self.core.data_store.cursor.execute("SELECT open,close FROM dollar_index ORDER BY timestamp DESC")
        values = self.core.data_store.cursor.fetchall()

        # Build dataset for regression
        x = []
        y = []
        for value in values:
            x.append(value[0])
            y.append(value[1])

        #self.widget = LinearTrendlineWidget(x,
        #                                    y,
        #                                    series_name="UDSX close",
        #                                    chart_title="Linear regression 7 day forecast",
        #                                    days=7)

        #self.widget.setWindowTitle("Market Analysis - Trend Prediction")
        #self.widget.show()
