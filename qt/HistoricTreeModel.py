from calendar import day_name, month_name
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from core import CurrencySymbol, SeriesData


class HistoricTreeModel(QStandardItemModel):
    """
    Standard item model backed by a historic data
    store to produce display information in a useful
    fashion
    """
    data_store = None

    def __init__(self, store, parent=None):
        """
        Create an object backed by a data store

        :param store: Data store
        :param parent: Qt parent
        """
        # Init parent
        super().__init__(parent)

        # Set store
        self.data_store = store

    def initialise(self, symbol):
        """
        Initialise the model (clearing any existing info)

        :param symbol: Symbol for display
        """
        # Clear current data
        self.clear()

        # Get unique years for top-level items
        years = self.data_store.list_years(symbol)

        # Insert
        self.insertRows(0, len(years))

        # Build base of years from data
        n = 0
        for year in years:
            year_item = QStandardItem(str(year[0]))
            year_item.setData(year[0])
            year_item.setEditable(False)

            # Build months
            months = self.data_store.list_months_for_year(year[0], symbol)
            for month in months:
                month_item = QStandardItem(self.get_month_name(month[0]))
                month_item.setData(month[0])
                month_item.setEditable(False)
                year_item.appendRow(month_item)

                # Build full value data
                data = self.data_store.list_data_for_month_year(year[0], month[0], symbol)
                for value in data:
                    # Acquire the information for the day
                    series = SeriesData.from_record(value)
                    data_item = QStandardItem()
                    data_item.setText(self.get_day_name(series.date)
                                      +
                                      " "
                                      +
                                      str(series.date.day)
                                      +
                                      self.get_date_suffix(series.date.day))
                    data_item.setData(series)
                    data_item.setEditable(False)

                    # Add children for each basic value
                    high_item = QStandardItem("High")
                    low_item = QStandardItem("Low")
                    open_item = QStandardItem("Open")
                    close_item = QStandardItem("Close")
                    adj_close_item = QStandardItem("Adj. Close")
                    volume_item = QStandardItem("Volume")

                    # RO
                    high_item.setEditable(False)
                    low_item.setEditable(False)
                    open_item.setEditable(False)
                    close_item.setEditable(False)
                    adj_close_item.setEditable(False)
                    volume_item.setEditable(False)

                    # Daily high
                    high_value = QStandardItem(self.format_currency(series.currency, series.high))
                    high_value.setData(series.high)
                    high_value.setEditable(False)
                    high_item.appendRow(high_value)

                    # Daily low
                    low_value = QStandardItem(self.format_currency(series.currency, series.low))
                    low_value.setData(series.low)
                    low_value.setEditable(False)
                    low_item.appendRow(low_value)

                    # Daily open
                    open_value = QStandardItem(self.format_currency(series.currency, series.open))
                    open_value.setData(series.open)
                    open_value.setEditable(False)
                    open_item.appendRow(open_value)

                    # Daily close
                    close_value = QStandardItem(self.format_currency(series.currency, series.close))
                    close_value.setData(series.close)
                    close_value.setEditable(False)
                    close_item.appendRow(close_value)

                    # Daily adj. close
                    adj_close_value = QStandardItem(self.format_currency(series.currency, series.adj_close))
                    adj_close_value.setData(series.adj_close)
                    adj_close_value.setEditable(False)
                    adj_close_item.appendRow(adj_close_value)

                    # Volume
                    volume_value = QStandardItem(str(int(series.volume)))
                    volume_value.setData(series.adj_close)
                    volume_value.setEditable(False)
                    volume_item.appendRow(volume_value)

                    # Add items to data point
                    data_item.appendRow(high_item)
                    data_item.appendRow(low_item)
                    data_item.appendRow(open_item)
                    data_item.appendRow(close_item)
                    data_item.appendRow(adj_close_item)
                    data_item.appendRow(volume_item)

                    # Add month data
                    month_item.appendRow(data_item)

            # Set item in model
            self.setItem(n, 0, year_item)
            n += 1

    @staticmethod
    def get_month_name(month):
        """
        Get the actual (english) month provided a point
        in time

        :param month: Month
        :return: Day name
        """
        return month_name[month]

    @staticmethod
    def get_day_name(datetime):
        """
        Get the actual (english) date provided a point
        in time

        :param datetime: Time point
        :return: Day name
        """
        return day_name[datetime.weekday()]

    @staticmethod
    def get_date_suffix(day):
        """
        Return the suffix string (E.g. nd, th) provided
        a day numeral

        Sourced from: https://stackoverflow.com/a/5891598

        :param day: Day number
        :return: Suffix string
        """
        suffix = ""
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return suffix

    @staticmethod
    def format_currency(currency, value):
        """
        Acquire formatted currency string

        :param currency: Currency string
        :param value: Value
        :return:
        """
        return CurrencySymbol.get_symbol(currency) + str(value)
