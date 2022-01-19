from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtChart import QChart, QLineSeries
from PyQt5.QtGui import QPainter, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QMessageBox
from sklearn import model_selection
from numpy import asarray

from core import AppCore, LinearRegression
from qt import ChartWidget
from gen.ui_LinearTestWidget import Ui_LinearTestWidget


class LinearTestWidget(QWidget):
    """
    Simple widget which has the capacity to display
    linear regression data n days into the future
    provided an x, y relationship between open and
    close values
    """
    ui = None
    core = AppCore()
    chart = None
    chart_widget = None
    symbol = ""
    min_val = ""
    max_val = ""
    day_val = ""
    growth = True
    test_split = 0.2
    pred_series = QLineSeries()
    test_series = QLineSeries()
    model = None
    model_updated = pyqtSignal()

    def __init__(self, parent=None):
        """
        Create widget with a parent

        :param parent: Parent widget
        """
        # Initialise parent
        super().__init__(parent)

        # Create UI
        self.ui = Ui_LinearTestWidget()
        self.ui.setupUi(self)

        # Add chart widget
        self.chart_widget = ChartWidget()
        self.chart_widget.ui.chartView.setRenderHint(QPainter.Antialiasing)
        self.ui.chartWidget.layout().addWidget(self.chart_widget)

        # Input masks
        minValidator = QDoubleValidator()
        maxValidator = QDoubleValidator()
        dayValidator = QIntValidator()
        minValidator.setBottom(1)
        maxValidator.setBottom(1)
        dayValidator.setBottom(7)
        self.ui.minValue.setValidator(minValidator)
        self.ui.maxValue.setValidator(maxValidator)
        self.ui.dayValue.setValidator(dayValidator)

        # Connect signals
        self.ui.minValue.textChanged.connect(self.update_min_load)
        self.ui.maxValue.textChanged.connect(self.update_max_load)
        self.ui.dayValue.textChanged.connect(self.update_day_load)
        #self.ui.checkBox.stateChanged.connect(self.update_growth)
        self.ui.testValue.valueChanged.connect(self.update_test_value)

        # Create chart
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeBlueCerulean)
        self.chart.setBackgroundVisible(False)
        self.chart.setTitle("Linear regression tuning")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # Set chart view
        self.chart_widget.ui.chartView.setChart(self.chart)

    @staticmethod
    def invalid_message():
        """
        Show an invalid configuration message
        """
        box = QMessageBox()
        box.setWindowTitle("Invalid configuration")
        box.setStandardButtons(QMessageBox.Ok)
        box.setText("One or more of the configuration parameters "
                    "produced an invalid dataset to perform analysis on")
        box.setIcon(QMessageBox.Warning)
        box.exec_()

    def update_symbol(self, symbol):
        """
        Update the symbol and re-perform analysis

        :param symbol: Symbol
        """
        self.symbol = symbol
        self.update_chart()

    def update_chart(self):
        """
        Perform dynamic query and update chart from contents
        """
        # Query string
        query = self.build_query()

        # Perform query
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        if len(data) == 0:
            self.invalid_message()
            return

        # Clear any existing series from chart
        if len(self.chart.series()) > 0:
            self.chart.removeAllSeries()
            self.pred_series = QLineSeries()
            self.test_series = QLineSeries()
            x_axis = self.chart.axes(Qt.Horizontal)[0]
            y_axis = self.chart.axes(Qt.Vertical)[0]
            self.chart.removeAxis(y_axis)
            self.chart.removeAxis(x_axis)

        # Series names
        self.pred_series.setName("Predicted values")
        self.test_series.setName("Test values")

        # Categorise query results into x (open)
        # and y (close) by processing result query
        open = []
        close = []
        for value in data:
            open.append(value[0])
            close.append(value[1])
        open_train, open_test, close_train, close_test = None, None, None, None

        # Split data into train/test
        try:
            open_train, open_test, close_train, close_test = model_selection.train_test_split(open,
                                                                                              close,
                                                                                              test_size=self.test_split,
                                                                                              random_state=5)
        except ValueError:
            self.invalid_message()
            return

        # Create model
        self.model = LinearRegression.create_model(open_train, close_train)
        self.model_updated.emit()
        predicted_close = self.model.predict(asarray(open_test).reshape(-1, 1)).flatten()

        # Plot
        n = 0
        while n < len(close_test):
            self.pred_series.append(n, predicted_close[n])
            self.test_series.append(n, close_test[n])
            n += 1

        # Add series
        self.chart.addSeries(self.pred_series)
        self.chart.addSeries(self.test_series)

        # Axis setup
        self.chart.createDefaultAxes()
        x_axis = self.chart.axes(Qt.Horizontal)[0]
        x_axis.setTickCount(n)

    def update_min_load(self, min_val):
        """
        Update min open value

        :param min_val: Open value
        """
        self.min_val = min_val
        self.update_chart()

    def update_max_load(self, max_val):
        """
        Update max open value

        :param max_val: Open value
        """
        self.max_val = max_val
        self.update_chart()

    def update_day_load(self, day_val):
        """
        Update day config value

        :param day_val: Day value
        """
        self.day_val = day_val
        self.update_chart()

    def update_test_value(self, value):
        """
        Update test config value

        :param value: Test split
        """
        self.test_split = value / 100
        self.update_chart()

    def build_query(self):
        """
        Build a SQL query string based on the UI parameters

        :return: Query string
        """
        # Base string
        base = "SELECT open,close FROM time_series_daily_adjusted WHERE symbol=" + '\'' + self.symbol + '\''

        # Defaults
        where_min = ""
        where_max = ""
        in_range = ""
        sort_by = ""

        if self.min_val is not "":
            where_min = " AND open >= " + '\'' + self.min_val + '\''

        if self.max_val is not "":
            where_max = " AND open <= " + '\'' + self.max_val + '\''

        if self.day_val is not "":
            in_range = " AND timestamp > " + '\'' + str((datetime.utcnow()
                                                         -
                                                         timedelta(days=int(self.day_val))).timestamp()) + '\''

        #if self.growth is True:
        #    sort_by = " ORDER BY open ASC"
        #else:
        #    sort_by = " ORDER BY open DESC"

        # Full query
        query = base + where_min + where_max + in_range + sort_by
        return query
