import sqlite3
from threading import Lock


class ApplicationDataStore:
    """
    Class which stores historic query data with
    the ability to perform 'queries' against this
    data to find information for specific time points
    """
    connection = None
    cursor = None
    lock = Lock()

    def __init__(self):
        # Create an in-memory DB
        self.connection = sqlite3.connect("data_store.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Setup the table
        table = open('sql/initialise_data.sql').read()

        # Create the table
        self.cursor.executescript(table)
        self.connection.commit()

    def __del__(self):
        # Drop connection to DB
        self.cursor.close()
        self.connection.close()

    def add_items(self, items):
        """
        Add a bulk set of items to the store with the
        correct categorisation

        :param items: Items to add
        """
        insert_data = []
        for item in items:
            insert_data.append(item.serialise())

        query = 'INSERT OR IGNORE INTO time_series_daily_adjusted VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

        # Bulk insert
        self.cursor.executemany(query, insert_data)

        # Commit
        self.connection.commit()

    def list_years(self, symbol):
        """
        List unique years in DB

        :param symbol: Symbol to filter

        :return: Years
        """
        self.cursor.execute("SELECT DISTINCT year FROM time_series_daily_adjusted WHERE symbol=" + '\'' + symbol + '\'')
        data = self.cursor.fetchall()
        return data

    def list_months_for_year(self, year, symbol):
        """
        List unique months for a given year

        :param year: Year
        :param symbol: Symbol to filter

        :return: Months
        """
        self.cursor.execute("SELECT DISTINCT month FROM time_series_daily_adjusted WHERE year="
                            + str(year) + " AND symbol=" + '\'' + symbol + '\'')
        data = self.cursor.fetchall()
        return data

    def list_data_for_month_year(self, year, month, symbol):
        """
        Get all the data for a month within a year

        :param year: Year
        :param month: Month
        :param symbol: Symbol to filter

        :return: Data for period
        """
        self.cursor.execute("SELECT * FROM time_series_daily_adjusted WHERE year=" + str(year) +
                            " AND month=" + str(month) + " AND symbol=" + '\'' + symbol + '\'' +
                            "ORDER BY timestamp DESC")
        data = self.cursor.fetchall()
        return data
