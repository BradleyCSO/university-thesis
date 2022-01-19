from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QLineSeries, QAreaSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QColor


class DollarIndexChart(QChart):
    """
    Line chart to display USDX data
    """
    data_series = None

    def __init__(self, parent=None):
        """
        Initialise with optional parent

        :param parent: Parent
        """
        super().__init__(parent)

        # Display config
        self.setBackgroundVisible(False)
        self.setTheme(QChart.ChartThemeBlueCerulean)

        # Create series
        self.data_series = QLineSeries()
        self.base_series = QLineSeries()
        self.area_series = None

    def populate(self, title, data, base):
        """
        Populate the chart with data

        :param title: Chart title
        :param data: Chart data
        :param base: Base value for area series
        """
        # Clear any existing series
        if len(self.series()) > 0:
            self.removeAllSeries()
            self.data_series = QLineSeries()
            self.base_series = QLineSeries()
            self.area_series = None
            x_axis = self.axes(Qt.Horizontal)[0]
            y_axis = self.axes(Qt.Vertical)[0]
            self.removeAxis(y_axis)
            self.removeAxis(x_axis)

        # Setup series
        self.data_series.setName("USDX")
        self.data_series.setColor(QColor(Qt.white))

        # Legend
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

        # Build line series
        for value in data:
            # Append value and time point to series
            self.data_series.append(value[0] * 1000, value[1])
            self.base_series.append(value[0] * 1000, base)

        # Create area series
        self.area_series = QAreaSeries(self.data_series,
                                       self.base_series)
        self.area_series.setColor(Qt.darkCyan)
        self.area_series.setOpacity(0.1)

        # Apply model
        self.area_series.setName("USDX benchmark")
        self.addSeries(self.data_series)
        self.addSeries(self.area_series)
        self.setTitle(title)
        self.setAnimationOptions(QChart.SeriesAnimations)

        # Axis setup
        x_axis = QDateTimeAxis()
        x_axis.setTickCount(24)
        x_axis.setFormat("MMM yyyy")
        x_axis.setTitleText("Date")
        x_axis.setLabelsAngle(-90)
        self.addAxis(x_axis, Qt.AlignBottom)
        self.data_series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setLabelFormat("%f")
        self.addAxis(y_axis, Qt.AlignLeft)
        self.data_series.attachAxis(y_axis)
