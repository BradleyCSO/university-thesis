from datetime import datetime, timedelta
from numpy import average
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtChart import QChart, QCandlestickSeries, QCandlestickSet, QLineSeries


class CandlestickChart(QChart):
    """
    Simple cart that displays chart data from
    the historic DB
    """
    historic_store = None
    data_series = QCandlestickSeries()
    sma_series = QLineSeries()

    def __init__(self, store, parent=None):
        """
        Construct a chart object provided the
        data store

        :param parent: Parent QObject
        :param store: Data store
        """
        super().__init__(parent)

        # Display
        self.setTheme(QChart.ChartThemeBlueCerulean)
        self.setBackgroundVisible(False)

        # Apply store
        self.historic_store = store

    @staticmethod
    def create_closed_day(date, value):
        """
        Create a set for a day the exchange
        was not trading which simply populates
        all fields with the same value

        :param date: Date
        :param value: Value
        :return: Created set
        """
        set = QCandlestickSet()
        set.setTimestamp(date.timestamp())
        set.setOpen(value)
        set.setHigh(value)
        set.setLow(value)
        set.setClose(value)
        return set

    def setup(self, selected, days):
        """
        Populate the chart model and setup
        the axis data for visualisation

        :param selected: Stock selection
        :param days: Days to load (back in time)
        """
        # Clear any existing series
        if len(self.series()) > 0:
            self.removeAllSeries()
            self.data_series = QCandlestickSeries()
            self.sma_series = QLineSeries()
            x_axis = self.axes(Qt.Horizontal)[0]
            y_axis = self.axes(Qt.Vertical)[0]
            self.removeAxis(y_axis)
            self.removeAxis(x_axis)

        # Extract symbol
        symbol = selected.symbol

        # Setup series
        self.data_series.setName("Daily candlestick")
        self.data_series.setIncreasingColor(QColor(Qt.green))
        self.data_series.setDecreasingColor(QColor(Qt.red))

        self.sma_series.setName("SMA")
        self.sma_series.setColor(QColor(Qt.yellow))

        # Legend
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

        # Get most recent year in data
        years = self.historic_store.list_years(symbol)
        year = max(years)
        year = str(year[0])

        # Query window
        latest = datetime.utcnow()
        earliest = latest - timedelta(days=days)

        # Query for data in specified year
        self.historic_store.cursor.execute('SELECT timestamp,open,high,low,close FROM time_series_daily_adjusted WHERE \
                                            timestamp BETWEEN ' + '\'' + str(earliest.timestamp()) + '\'' + 'AND' +
                                           '\'' + str(latest.timestamp()) + '\'' + 'AND symbol=' + '\'' + symbol +
                                           '\'')
        data = self.historic_store.cursor.fetchall()

        # Axis categories
        categories = []
        sma_vals = []

        # Process each record and add to the model
        for value in data:
            # Date
            date = datetime.fromtimestamp(value[0])

            # SMA values
            sma_vals.append(value[4])
            sma = average(sma_vals)

            # Remove oldest when at 5 (total) values
            if len(sma_vals) == 4:
                sma_vals.pop(0)

            # Add SMA to line
            self.sma_series.append(date.timestamp(), float(sma))

            # Create item in index
            dataset = QCandlestickSet()
            dataset.setTimestamp(date.timestamp())
            dataset.setOpen(value[1])
            dataset.setHigh(value[2])
            dataset.setLow(value[3])
            dataset.setClose(value[4])

            # Add date to category
            date_str = date.strftime("%Y-%m-%d")
            categories.append(date_str)

            # Add zero-movement days for weekends (as long as it doesn't
            # send us to the future) for the 7-day chart
            if days <= 7:
                wd = date.weekday()
                if wd == 4 and date is not datetime.utcnow():
                    # Weekend
                    sat_date = date + timedelta(days=1)
                    sun_date = date + timedelta(days=2)

                    # Create sets
                    sat = self.create_closed_day(sat_date, value[4])
                    sun = self.create_closed_day(sun_date, value[4])

                    # Add categories
                    categories.append(sat_date.strftime("%Y-%m-%d"))
                    categories.append(sun_date.strftime("%Y-%m-%d"))

                    # Add to set
                    self.data_series.append(sat)
                    self.data_series.append(sun)

            # Add to chart
            self.data_series.append(dataset)

        # Apply model
        self.addSeries(self.data_series)
        self.setTitle(selected.name + " " + str(days) + " day performance")
        self.setAnimationOptions(QChart.SeriesAnimations)

        # Axis setup
        self.createDefaultAxes()
        x_axis = self.axes(Qt.Horizontal)[0]
        x_axis.setCategories(categories)
        x_axis.setLabelsAngle(-90)

        # Add SMA series to existing axis
        self.addSeries(self.sma_series)
