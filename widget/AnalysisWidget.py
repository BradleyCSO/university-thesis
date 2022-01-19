from numpy import asarray
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QLineSeries, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter

from core import AppCore
from widget.GeometryRestoreWidget import GeometryRestoreWidget
from gen.ui_AnalysisWidget import Ui_AnalysisWidget
from qt.ChartWidget import ChartWidget
from widget.LinearTestWidget import LinearTestWidget


class AnalysisWidget(GeometryRestoreWidget):
    """
    Widget to display analysis graphs from
    transformations performed on DB data
    """
    core = AppCore()
    ui = None
    linear_analysis_widget = None
    linear_test_widget = None
    linear_analysis_chart = None
    linear_analyis_series = QLineSeries()

    def __init__(self, parent=None):
        """
        Create analysis widget

        :param parent: Parent widget
        """
        # Restore geometry
        super().__init__("AnalysisWidget", parent)

        # Load UI
        self.ui = Ui_AnalysisWidget()
        self.ui.setupUi(self)

        # Setup analysis widget
        self.linear_analysis_widget = ChartWidget()

        # Setup analysis chart
        self.linear_analysis_chart = QChart()
        self.linear_analysis_chart.setTheme(QChart.ChartThemeBlueCerulean)
        self.linear_analysis_chart.setBackgroundVisible(False)
        self.linear_analysis_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.linear_analysis_chart.legend().setVisible(True)
        self.linear_analysis_chart.legend().setAlignment(Qt.AlignBottom)
        self.linear_analysis_widget.ui.chartView.setRenderHint(QPainter.Antialiasing)
        self.linear_analysis_widget.ui.chartView.setChart(self.linear_analysis_chart)

        # Add to display
        self.ui.linearRegTab.layout().addWidget(self.linear_analysis_widget)

        # Create test widget
        self.linear_test_widget = LinearTestWidget()
        self.ui.linearTestTab.layout().addWidget(self.linear_test_widget)

        # Update analysis from test model config changes
        self.linear_test_widget.model_updated.connect(self.update_linear_analysis)

    def update_linear_analysis(self):
        """
        Populate the linear analysis for N days using
        the configuration from the test widget
        """
        # Load most recent open value
        query = "SELECT open FROM time_series_daily_adjusted WHERE symbol = " + \
                '\'' + self.linear_test_widget.symbol + '\'' + " ORDER BY timestamp DESC LIMIT 1"
        self.core.data_store.cursor.execute(query)
        value = self.core.data_store.cursor.fetchall()

        if len(value) == 0:
            # Some error
            return

        # Create a chart using the values, clear
        # any existing series from chart
        if len(self.linear_analysis_chart.series()) > 0:
            self.linear_analysis_chart.removeAllSeries()
            self.linear_analyis_series = QLineSeries()
            x_axis = self.linear_analysis_chart.axes(Qt.Horizontal)[0]
            y_axis = self.linear_analysis_chart.axes(Qt.Vertical)[0]
            self.linear_analysis_chart.removeAxis(y_axis)
            self.linear_analysis_chart.removeAxis(x_axis)

        # Predict 7 days ahead using the model generated
        # through the configuration widget for training and
        # test, starting with the current open value
        value = value[0][0]
        n = 0
        categories = []
        max = value
        min = value
        self.linear_analyis_series.append(n, value)
        categories.append((datetime.utcnow() + timedelta(days=n)).strftime("%Y-%m-%d"))
        while n < 7:
            n += 1
            prediction = self.linear_test_widget.model.predict(asarray(value).reshape(-1, 1))
            value = prediction.flatten()[0]
            categories.append((datetime.utcnow() + timedelta(days=n)).strftime("%Y-%m-%d"))
            self.linear_analyis_series.append(n, value)
            if value > max:
                max = value
            if value < min:
                min = value

        # Series names
        self.linear_analyis_series.setName("Forecast close values")
        self.linear_analysis_chart.setTitle(self.linear_test_widget.symbol + " Linear regression 7-day forecast")

        # Add series
        self.linear_analysis_chart.addSeries(self.linear_analyis_series)

        # Axis setup
        x_axis = QBarCategoryAxis()
        x_axis.setTitleText("Date")
        x_axis.setLabelsAngle(-90)
        x_axis.setCategories(categories)
        self.linear_analysis_chart.addAxis(x_axis, Qt.AlignBottom)
        self.linear_analyis_series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setLabelFormat("%f")
        y_axis.setTitleText("Value (USD)")
        pad = max - min
        y_axis.setRange(min - pad, max + pad)
        self.linear_analysis_chart.addAxis(y_axis, Qt.AlignLeft)
        self.linear_analyis_series.attachAxis(y_axis)

    def update_analysis(self, symbol):
        """
        Update the analysis configuration widget to let
        the user dynamically configure the parameter to
        use for linear regression training and display
        the test data
        """
        # Update test/train display
        self.linear_test_widget.update_symbol(symbol)

        # Perform initial analysis
        self.update_linear_analysis()
