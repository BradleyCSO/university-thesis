from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from core import AppCore


class CurrencyListModel(QStandardItemModel):
    """
    Model which fetches all known symbols
    from the DB and displays them in a list
    """
    core = AppCore()
    items = {}

    def __init__(self, parent=None):
        """
        Initialise with optional parent

        :param parent: Parent object
        """
        super().__init__(parent)

        # Get currencies from DB
        self.core.get_data_store().cursor.execute("SELECT symbol from currency_symbols")
        results = self.core.get_data_store().cursor.fetchall()

        # Insert list into view
        for currency in results:
            symbol = currency[0]
            item = QStandardItem()
            item.setText(symbol)
            item.setEditable(False)
            self.items[symbol] = item
            self.appendRow(item)

    def item_for(self, symbol):
        """
        Get the item for a provided symbol

        :param symbol: Symbol
        :return: Item for symbol (invalid if not found)
        """
        try:
            item = self.items[symbol]
            return item
        finally:
            return QStandardItem()

    def index_for(self, symbol):
        """
        Get the index for a provided symbol

        :param symbol: Symbol
        :return: Index for symbol (invalid if not found)
        """
        try:
            item = self.items[symbol]
            return item.index()
        finally:
            return QModelIndex()
