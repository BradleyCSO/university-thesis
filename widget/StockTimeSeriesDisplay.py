from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QSpacerItem, QSizePolicy
from json import loads

from core import AppCore, CurrencySymbol, MarketItem, QueryBuilder, SeriesData
from gen.ui_StockTimeSeriesDisplay import Ui_StockTimeSeriesDisplay
from qt import HistoricTreeModel, CandlestickChart, ItemRoles
from widget.LoadingWidget import LoadingWidget
from widget.ModeWidget import ModeWidget


class StockTimeSeriesDisplay(ModeWidget):
    """
    This class contains the main display with the search
    and data tree, and can be used to launch comparisons
    of the loaded data
    """
    # Generated UI
    ui = None

    # Core singleton
    core = AppCore()

    # Search model
    search_model = None
    filter_model = None

    # Last search results
    results = None

    # Data store
    historic_store = None

    # Data model
    data_model = None
    filter_data_model = None

    # Selected
    selected = None

    # Loading spacer
    loading_spacer = None

    # Chart data
    chart = None
    chart_days = 30

    # Chart space
    chart_spacer = None

    # Loading widget
    loading_widget = None

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Parent widget (none for standalone window)
        """
        # Initialise super
        super().__init__("StockTimeSeriesDisplay", parent)

        # Get data store
        self.historic_store = self.core.get_data_store()

        # Setup generated UI
        self.ui = Ui_StockTimeSeriesDisplay()
        self.ui.setupUi(self)

        # Loading widget and spacer
        self.loading_widget = LoadingWidget(self)
        self.loading_widget.move(self.rect().center() - self.loading_widget.rect().center())
        self.loading_widget.hide()
        self.loading_spacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # Search view
        self.ui.searchList.verticalHeader().hide()
        self.ui.searchList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.searchList.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Search model
        self.search_model = QStandardItemModel()
        self.filter_model = QSortFilterProxyModel()
        self.filter_model.setSourceModel(self.search_model)
        self.ui.searchList.setModel(self.filter_model)
        self.ui.searchList.setSortingEnabled(True)

        # History view
        self.ui.historicView.setHeaderHidden(True)

        # When search is inputted, perform query
        self.ui.searchEdit.textEdited.connect(self.launch_search)

        # When item is selected from search view, load data
        self.ui.searchList.clicked.connect(self.load_data)

        # Hide chart by default
        self.ui.chartView.setVisible(False)
        self.chart_spacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.ui.infoLayout.addItem(self.chart_spacer)

        # Chart updates
        self.ui.days_7.pressed.connect(lambda: self.chart.setup(self.selected, 7))
        self.ui.days_30.pressed.connect(lambda: self.chart.setup(self.selected, 30))
        self.ui.days_90.pressed.connect(lambda: self.chart.setup(self.selected, 90))

        # Chart config
        self.chart = CandlestickChart(self.historic_store)
        self.chart.setBackgroundVisible(False)
        self.ui.chartView.setChart(self.chart)
        self.ui.daysButtonArea.setVisible(False)

        self.ui.mainLayout.setEnabled(False)

        # Apply default headings
        self.set_default_table_headings()

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

    def set_default_table_headings(self):
        """
        Supply default headings to the table model
        for the search results
        """
        self.search_model.setHorizontalHeaderItem(0, QStandardItem("Symbol"))
        self.search_model.setHorizontalHeaderItem(1, QStandardItem("Name"))
        self.search_model.setHorizontalHeaderItem(2, QStandardItem("Type"))
        self.search_model.setHorizontalHeaderItem(3, QStandardItem("Region"))
        self.search_model.setHorizontalHeaderItem(4, QStandardItem("Currency"))
        self.search_model.setHorizontalHeaderItem(5, QStandardItem("Accuracy"))

    def update_search_results(self, item_list):
        """
        Create the model from the list, to be
        executed on the GUI thread only

        :param item_list: List
        """
        # Dump existing model
        self.search_model.clear()

        # Populate headings (well-known)
        self.set_default_table_headings()

        # Mark rows as ready to insert
        self.search_model.insertRows(0, len(item_list))

        # Populate the entire model
        r = 0
        for row in item_list:
            c = 0
            for col in row:
                self.search_model.setItem(r, c, col)
                c += 1
            r += 1

        # Clear busy
        self.ui.searchList.unsetCursor()

    @staticmethod
    def create_standard_item(value, match, raw):
        """
        Create a non-editable standard item using a
        provided value as reference

        :param value: Text value
        :param match: Match value
        :param raw: JSON value
        :return: Created item
        """
        item = QStandardItem()

        # Supply values
        item.setText(value)
        item.setData(float(match), Qt.UserRole + 1)
        item.setData(MarketItem(raw), ItemRoles.SERIES_DATA_ROLE)
        item.setEditable(False)
        return item

    @staticmethod
    def create_currency_item(value, match, raw):
        """
        Create a specially formatted currency
        item using ISO currency codes

        :param value: Currency value
        :param match: Match value
        :param raw: JSON value
        :return: Create item
        """
        item = QStandardItem()

        # Supply values
        item.setText(value + " (" + CurrencySymbol.get_symbol(value) + ")")
        item.setData(float(match), Qt.UserRole + 1)
        item.setData(MarketItem(raw), ItemRoles.SERIES_DATA_ROLE)
        item.setEditable(False)
        return item

    @staticmethod
    def create_match_item(value, raw):
        """
        Create a specifically formatted match
        value using a numeric value (0-1)

        :param value: Match value
        :param raw: JSON value
        :return:
        """
        item = QStandardItem()

        # Display text for match value
        text = None
        if value == 1:
            text = "Perfect"
        elif value > 0.9:
            text = "Very good"
        elif value > 0.75:
            text = "Good"
        elif value > 0.5:
            text = "Close"
        else:
            text = "Poor"

        # Supply values
        item.setText(text + " (" + str(int(value * 100)) + "%)")
        item.setData(value, Qt.UserRole + 1)
        item.setData(MarketItem(raw), ItemRoles.SERIES_DATA_ROLE)
        return item

    def process_search_results(self, result):
        """
        Process the JSON results generated by a search
        to produce a list model using the results

        :param result JSON results
        """
        # List to build
        item_list = []

        # Build a formatted list of strings from the result
        for value in result['bestMatches']:
            if value['4. region'] == 'United States':
                # Add all columns
                columns = [self.create_standard_item(value['1. symbol'], value['9. matchScore'], value),
                           self.create_standard_item(value['2. name'], value['9. matchScore'], value),
                           self.create_standard_item(value['3. type'], value['9. matchScore'], value),
                           self.create_standard_item(value['4. region'], value['9. matchScore'], value),
                           self.create_currency_item(value['8. currency'], value['9. matchScore'], value),
                           self.create_match_item(float(value['9. matchScore']), value)]

                # Add row
                item_list.append(columns)

        # Ensure the actual model update is applied on the GUI thread
        self.core.get_forwarder().forward(lambda: self.update_search_results(item_list))

    def launch_search(self):
        """
        Perform a search to get results based on
        the contents of the line edit
        """
        # Set cursor
        self.ui.searchList.setCursor(Qt.BusyCursor)

        # Build the URL string
        query_url = QueryBuilder.create() \
                                .function("SYMBOL_SEARCH") \
                                .key(self.core.get_api_key()) \
                                .keywords(self.ui.searchEdit.text()) \
                                .data_type("json") \
                                .url()

        # Execute query on thread pool so we don't
        # block our GUI while waiting for the result
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", query_url],
                                                callback=lambda result: self.process_search_results(loads(result.data)))

    def update_data_model(self):
        """
        Creates a tree model and assigns it to the
        configured view
        """
        # Create model
        self.data_model = HistoricTreeModel(self.historic_store)
        self.filter_data_model = QSortFilterProxyModel()
        self.data_model.initialise(self.selected.symbol)
        self.filter_data_model.setSourceModel(self.data_model)
        self.filter_data_model.setSortRole(Qt.UserRole + 1)
        self.ui.historicView.setSortingEnabled(True)
        self.ui.historicView.unsetCursor()

        # Chart setup
        self.chart.setup(self.selected, 30)

        # Set with view
        self.ui.historicView.setModel(self.filter_data_model)

        # Update analysis display
#        self.core.stock_time_series_analysis_window.update_linear_analysis(self.selected.symbol)
        self.core.stock_time_series_analysis_window.update_analysis(self.selected.symbol)

        # Hide loading widget
        self.loading_widget.hide()
        self.ui.searchLayout.removeItem(self.loading_spacer)
        self.ui.mainLayout.setEnabled(True)
        self.ui.mainLayout.setVisible(True)
        self.ui.chartView.setVisible(True)
        self.ui.daysButtonArea.setVisible(True)
        self.core.stock_time_series_analysis_window.show()
        self.ui.infoLayout.removeItem(self.chart_spacer)

    def process_time_series(self, series, index, currency):
        """
        Process all values found in a time series into
        market items to populate a historic data store,
        which can the nbe used to build models

        :param series: Series data
        :param index: Index to access
        :param currency: Currency symbol for display
        """
        # List to insert
        items = []

        for value in series[index]:
            # Extract data
            data = series[index][value]

            # Produce item
            items.append(SeriesData.from_json(self.selected.symbol, currency, value, data))

        # Add to historic data store
        self.historic_store.add_items(items)

        # Build model on GUI
        self.core.get_forwarder().forward(self.update_data_model)

    def load_data(self, index):
        """
        Update the UI with the selected data from the
        search model and load the full dataset for the
        symbol

        :param index: Selected index
        """
        # Setup loading widget
        self.loading_widget.show()
        self.ui.searchLayout.addItem(self.loading_spacer)
        self.ui.mainLayout.setVisible(False)
        self.ui.chartView.setVisible(False)
        self.ui.daysButtonArea.setVisible(False)
        self.core.stock_time_series_analysis_window.hide()
        self.ui.infoLayout.addItem(self.chart_spacer)

        # Set display to loading
        self.ui.historicView.setCursor(Qt.BusyCursor)

        item = self.search_model.item(index.row(),
                                      index.column())
        data = item.data(ItemRoles.SERIES_DATA_ROLE)

        # Selected data
        self.selected = data

        # Apply values to UI
        self.ui.symbolText.setText(data.symbol)
        self.ui.nameText.setText(data.name)
        self.ui.typeText.setText(data.type)
        self.ui.openText.setText(data.open)
        self.ui.closeText.setText(data.close)
        self.ui.zoneText.setText(data.zone)

        # Build query URL
        query_url = QueryBuilder.create() \
                                .function("TIME_SERIES_DAILY_ADJUSTED") \
                                .key(self.core.get_api_key()) \
                                .symbol(data.symbol) \
                                .data_type("json") \
                                .output_size("full") \
                                .url()

        # Execute query on thread pool so we don't
        # block our GUI while waiting for the result
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", query_url],
                                                callback=lambda result: self.process_time_series(loads(result.data),
                                                                                                 'Time Series (Daily)',
                                                                                                 data.currency))
