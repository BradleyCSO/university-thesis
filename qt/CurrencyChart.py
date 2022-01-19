from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QCandlestickSeries, QCandlestickSet
from PyQt5.QtGui import QColor

from core import AppCore


class CurrencyChart(QChart):
    """
    Chart which can display information about
    a currency over a period of time
    """
    core = AppCore()
    data_series = QCandlestickSeries()

    def __init__(self, parent=None):
        """
        Initialise with optional parent

        :param parent: Parent
        """
        super().__init__(parent)

        # Display config
        self.setBackgroundVisible(False)
        self.setTheme(QChart.ChartThemeBlueCerulean)

    def populate(self, title, data, series, series_filter=None):
        """
        Populate the chart with series data
        :param title: Chart title
        :param data: Series data
        :param series: Series name
        :param series_filter: Optional series filter to reduce noise
        """
        # Clear any existing series
        if len(self.series()) > 0:
            self.removeAllSeries()
            self.data_series = QCandlestickSeries()
            x_axis = self.axes(Qt.Horizontal)[0]
            y_axis = self.axes(Qt.Vertical)[0]
            self.removeAxis(y_axis)
            self.removeAxis(x_axis)

        # Axis categories
        categories = []

        # Setup series
        self.data_series.setName(series)
        self.data_series.setIncreasingColor(QColor(Qt.green))
        self.data_series.setDecreasingColor(QColor(Qt.red))

        # Legend
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

        # Parse all records
        for value in data:
            # Date
            date = datetime.fromtimestamp(value[0])

            # Filter out excess data points using
            # optional filter
            if series_filter is not None:
                if not series_filter.in_interval(date):
                    continue

            # Data
            timestamp = date.timestamp()
            open = value[1]
            high = value[2]
            low = value[3]
            close = value[4]

            # Create set
            values = QCandlestickSet()
            values.setTimestamp(timestamp)
            values.setOpen(open)
            values.setHigh(high)
            values.setLow(low)
            values.setClose(close)

            # Add category
            categories.append(date.strftime("%Y-%m-%d %H:%M:%S"))

            # Add to series
            self.data_series.append(values)

        # Apply model
        self.addSeries(self.data_series)
        self.setTitle(title)
        self.setAnimationOptions(QChart.SeriesAnimations)

        # Axis setup
        self.createDefaultAxes()
        x_axis = self.axes(Qt.Horizontal)[0]
        x_axis.setCategories(categories)
        x_axis.setLabelsAngle(-90)
