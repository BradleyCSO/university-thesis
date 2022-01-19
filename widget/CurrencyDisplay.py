from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from json import loads

from core import AppCore, QueryBuilder, DoneToken
from widget.ModeWidget import ModeWidget
from widget.LoadingWidget import LoadingWidget
from qt import CurrencyListModel, CurrencyChart, SeriesFilter

from gen.ui_CurrencyDisplay import Ui_CurrencyDisplay


class CurrencyDisplay(ModeWidget):
    """
    Widget which contains display information
    for currency pairings
    """
    ui = None
    core = AppCore()
    from_model = None
    from_sort_model = None
    to_model = None
    to_sort_model = None
    from_symbol = None
    to_symbol = None
    daily_chart = None
    loading_widget = None
    loading_spacer = None
    current_rate = 0

    def __init__(self, parent=None):
        """
        Initialise widget with parent

        :param parent: Parent
        """
        super().__init__("CurrencyDisplay", parent)
        self.ui = Ui_CurrencyDisplay()
        self.ui.setupUi(self)

        # Loading widget
        self.loading_widget = LoadingWidget(self)
        self.loading_widget.setVisible(False)
        self.loading_widget.move(self.rect().center() - self.loading_widget.rect().center())
        self.loading_spacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # Setup charts
        self.daily_chart = CurrencyChart()

        # Chart display
        self.ui.chartDisplay.setChart(self.daily_chart)

        # Setup two currency views
        self.from_model = CurrencyListModel()
        self.to_model = CurrencyListModel()

        # Setup sort models
        self.from_sort_model = QSortFilterProxyModel()
        self.to_sort_model = QSortFilterProxyModel()
        self.from_sort_model.setSourceModel(self.from_model)
        self.to_sort_model.setSourceModel(self.to_model)
        self.from_sort_model.sort(0)
        self.to_sort_model.sort(0)

        # Hide all in to model
        self.to_sort_model.setFilterRegularExpression("^((?!).)*$")

        # Set models on view
        self.ui.fromCurrencyView.setModel(self.from_sort_model)
        self.ui.toCurrencyView.setModel(self.to_sort_model)
        self.ui.toCurrencyView.setEnabled(False)

        # Disable view and add spacer
        self.ui.infoWidget.setVisible(False)
        self.ui.viewWidget.setVisible(False)
        self.ui.primaryLayout.addItem(self.loading_spacer)

        # Connect signals
        self.ui.fromCurrencyView.pressed.connect(self.update_from_selection)
        self.ui.toCurrencyView.pressed.connect(self.update_to_selection)

        self.ui.button15m.pressed.connect(self.populate_chart_15m)
        self.ui.button1h.pressed.connect(self.populate_chart_60m)
        self.ui.button24h.pressed.connect(self.populate_chart_24h)
        self.ui.button7d.pressed.connect(self.populate_chart_7d)
        self.ui.button30d.pressed.connect(self.populate_chart_30d)

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

    def populate_chart_15m(self):
        """
        Load 15 minutes of data from the DB and display it
        """
        # Query for 15 minute data
        timestamp = (datetime.utcnow() - timedelta(minutes=15)).timestamp()
        query = 'SELECT timestamp,open,high,low,close FROM currency_intraday WHERE to_symbol=' + \
                '\'' + self.to_symbol + '\'' + ' AND from_symbol=' + '\'' + self.from_symbol + '\'' + \
                ' AND timestamp > ' + str(timestamp)
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        # Add results to chart
        self.daily_chart.populate(self.from_symbol + " to " + self.to_symbol + " 15 minute data",
                                  data,
                                  self.from_symbol + " to " + self.to_symbol)

    def populate_chart_60m(self):
        """
        Load 60 minutes of data from the DB and display it
        """
        # Query for 60 minute data
        timestamp = (datetime.utcnow() - timedelta(minutes=60)).timestamp()
        query = 'SELECT timestamp,open,high,low,close FROM currency_intraday WHERE to_symbol=' + \
                '\'' + self.to_symbol + '\'' + ' AND from_symbol=' + '\'' + self.from_symbol + '\'' + \
                ' AND timestamp > ' + str(timestamp)
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        # Add results to chart
        self.daily_chart.populate(self.from_symbol + " to " + self.to_symbol + " 1 hour data",
                                  data,
                                  self.from_symbol + " to " + self.to_symbol)

    def populate_chart_24h(self):
        """
        Load 24 hours of data from the DB and display it
        """
        # Query for 24 hour data
        timestamp = (datetime.utcnow() - timedelta(hours=24)).timestamp()
        query = 'SELECT timestamp,open,high,low,close FROM currency_intraday WHERE to_symbol=' + \
                '\'' + self.to_symbol + '\'' + ' AND from_symbol=' + '\'' + self.from_symbol + '\'' + \
                ' AND timestamp > ' + str(timestamp)
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        # Filter out data in 30 minute chunks
        series_filter = SeriesFilter(timedelta(minutes=15))

        # Add results to chart
        self.daily_chart.populate(self.from_symbol + " to " + self.to_symbol + " 24 hour data",
                                  data,
                                  self.from_symbol + " to " + self.to_symbol,
                                  series_filter=series_filter)

    def populate_chart_7d(self):
        """
        Load 7 days of data from the DB and display it
        """
        # Query for 15 minute data
        timestamp = (datetime.utcnow() - timedelta(days=7)).timestamp()
        query = 'SELECT timestamp,open,high,low,close FROM currency_daily WHERE to_symbol=' + \
                '\'' + self.to_symbol + '\'' + ' AND from_symbol=' + '\'' + self.from_symbol + '\'' + \
                ' AND timestamp > ' + str(timestamp)
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        # Add results to chart
        self.daily_chart.populate(self.from_symbol + " to " + self.to_symbol + " 7 day data",
                                  data,
                                  self.from_symbol + " to " + self.to_symbol)

    def populate_chart_30d(self):
        """
        Load 30 days of data from the DB and display it
        """
        # Query for 15 minute data
        timestamp = (datetime.utcnow() - timedelta(days=30)).timestamp()
        query = 'SELECT timestamp,open,high,low,close FROM currency_daily WHERE to_symbol=' + \
                '\'' + self.to_symbol + '\'' + ' AND from_symbol=' + '\'' + self.from_symbol + '\'' + \
                ' AND timestamp > ' + str(timestamp)
        self.core.data_store.cursor.execute(query)
        data = self.core.data_store.cursor.fetchall()

        # Add results to chart
        self.daily_chart.populate(self.from_symbol + " to " + self.to_symbol + " 30 day data",
                                  data,
                                  self.from_symbol + " to " + self.to_symbol)

    def hide_ui(self):
        """
        Hide UI components, default state or while a query
        is loading
        """
        # Show loading spinner
        self.loading_widget.setVisible(True)
        self.ui.primaryLayout.addItem(self.loading_spacer)

        # Hide chart
        self.ui.infoWidget.setVisible(False)
        self.ui.viewWidget.setVisible(False)

    def show_ui(self):
        """
        Show UI components once a query has completed
        """
        # Hide loading spinner
        self.loading_widget.setVisible(False)
        self.ui.primaryLayout.removeItem(self.loading_spacer)

        # Set rate
        self.ui.currentRateArea.setText("1 " + self.from_symbol + " = " + self.current_rate + " " + self.to_symbol)

        # Show chart
        self.ui.infoWidget.setVisible(True)
        self.ui.viewWidget.setVisible(True)

        # Start with display of 60 min data
        self.populate_chart_60m()

    def populate_table(self, result, token, from_symbol, to_symbol, table, date_format, index):
        """
        Populate a specified DB table with currency data

        :param result: JSON data
        :param token: Done token
        :param from_symbol: From currency
        :param to_symbol: To currency
        :param table: Table to insert to
        :param date_format: Date parsing format
        :param index: JSON index
        """
        data = result[index]
        for index in data:
            # Get values at index
            value = data[index]

            # Time
            date = datetime.strptime(index, date_format)

            # Extract values
            open = float(value['1. open'])
            high = float(value['2. high'])
            low = float(value['3. low'])
            close = float(value['4. close'])
            timestamp = date.timestamp()

            # Insert into table
            command = "INSERT OR IGNORE INTO " + table + " VALUES (?,?,?,?,?,?,?)"
            self.core.data_store.cursor.execute(command,
                                                (from_symbol,
                                                 to_symbol,
                                                 timestamp,
                                                 open,
                                                 high,
                                                 low,
                                                 close))

            # Commit
            self.core.data_store.connection.commit()

        # Use token
        token.inc()

    def set_currency_rate(self, result, token):
        """
        Set the current rate of the currency provided
        the JSON data

        :param result: JSON data
        :param token: Done token
        """
        self.current_rate = result['Realtime Currency Exchange Rate']['5. Exchange Rate']
        token.inc()

    def populate_daily(self, result, token, from_symbol, to_symbol):
        """
        Insert data into the daily table

        :param result: JSON data
        :param token: Done token
        :param from_symbol: From currency
        :param to_symbol: To currency
        """
        self.populate_table(result,
                            token,
                            from_symbol,
                            to_symbol,
                            "currency_daily",
                            "%Y-%m-%d",
                            "Time Series FX (Daily)")

    def populate_intraday(self, result, token, from_symbol, to_symbol):
        """
        Insert data into the daily table

        :param result: JSON data
        :param token: Done token
        :param from_symbol: From currency
        :param to_symbol: To currency
        """
        self.populate_table(result,
                            token,
                            from_symbol,
                            to_symbol,
                            "currency_intraday",
                            "%Y-%m-%d %H:%M:%S",
                            "Time Series FX (1min)")

    def load_data(self):
        """
        Load the currency exchange data for various query
        pairings for the currently selected currencies
        """
        ex_url = QueryBuilder.create().function("CURRENCY_EXCHANGE_RATE") \
                                      .from_currency(self.from_symbol) \
                                      .to_currency(self.to_symbol) \
                                      .output_size("full") \
                                      .key(self.core.get_api_key()) \
                                      .url()

        # Token to show the UI after both
        # async queries have completed populating
        # the charts
        token = DoneToken(lambda: self.core.forwarder.forward(self.show_ui), 3)

        # Perform queries to populate tables/charts
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", ex_url],
                                                callback=lambda result: self.set_currency_rate(loads(result.data),
                                                                                               token))

        fx_url = QueryBuilder.create().function("FX_INTRADAY") \
                                      .from_symbol(self.from_symbol) \
                                      .to_symbol(self.to_symbol) \
                                      .output_size("full") \
                                      .interval("1min") \
                                      .key(self.core.get_api_key()) \
                                      .url()
        # Perform query
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", fx_url],
                                                callback=lambda result: self.populate_intraday(loads(result.data),
                                                                                               token,
                                                                                               self.from_symbol,
                                                                                               self.to_symbol))

        fx_daily_url = QueryBuilder.create().function("FX_DAILY") \
                                            .from_symbol(self.from_symbol) \
                                            .to_symbol(self.to_symbol) \
                                            .output_size("full") \
                                            .key(self.core.get_api_key()) \
                                            .url()
        # Perform query
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", fx_daily_url],
                                                callback=lambda result: self.populate_daily(loads(result.data),
                                                                                            token,
                                                                                            self.from_symbol,
                                                                                            self.to_symbol))

    def update_from_selection(self, index):
        """
        Remove and deselect the item from the from
        view it is selected in the to view

        :param index: Index
        """
        # Get from symbol
        symbol = self.from_sort_model.data(index, Qt.DisplayRole)
        change = not (self.from_symbol == symbol)

        # If it's a change, redraw the UI and query
        # for the data ranges
        if change:
            # Update symbol
            self.from_symbol = symbol

            # Ensure 'to' is now enabled
            self.ui.toCurrencyView.setEnabled(True)

            # Filter out the undesirable item from the to model
            self.to_sort_model.setFilterRegularExpression("^((?!" + self.from_symbol + ").)*$")
            self.to_sort_model.sort(0)

            if self.to_symbol:
                self.hide_ui()

                # Load data if to is also supplied
                self.load_data()

    def update_to_selection(self, index):
        """
        Remove and deselect the item from the to
        view it is selected in the from view

        :param index: Index
        """
        # Get from symbol
        symbol = self.to_sort_model.data(index, Qt.DisplayRole)
        change = not (self.to_symbol == symbol)

        # If it's a change, redraw the UI and query
        # for the data ranges
        if change:
            # Update symbol
            self.to_symbol = symbol

            self.hide_ui()

            # Reload data
            self.load_data()
