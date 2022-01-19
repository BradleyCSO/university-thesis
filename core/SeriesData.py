from datetime import datetime


class SeriesData:
    """
    Container class for timed series data
    """
    hash = None
    symbol = None
    timestamp = None
    date = None
    open = None
    high = None
    low = None
    close = None
    adj_close = None
    volume = None
    dividend = None
    currency = None
    split = None

    @staticmethod
    def from_json(symbol, currency, date, value):
        """
        Construct the object

        :param symbol: Item symbol
        :param currency: Currency code
        :param date: Date stamp
        :param value: JSON record data
        """
        # Parse date
        series = SeriesData()
        series.symbol = symbol
        series.date = datetime.strptime(date, "%Y-%m-%d")
        series.timestamp = series.date.timestamp()
        series.currency = currency

        # Parse record info
        for index in value:
            data = value[index]
            if index == '1. open':
                series.open = float(data)
            elif index == '2. high':
                series.high = float(data)
            elif index == '3. low':
                series.low = float(data)
            elif index == '4. close':
                series.close = float(data)
            elif index == '5. adjusted close':
                series.adj_close = float(data)
            elif index == '6. volume':
                series.volume = float(data)
            elif index == '7. dividend amount':
                series.dividend = float(data)
            elif index == '8. split coefficient':
                series.split = float(data)

        series.hash = hash(series)

        return series

    @staticmethod
    def from_record(record):
        """
        Produce series data from a DB record tuple

        :param record: Record tuple
        :return: Complete series data
        """
        series = SeriesData()
        series.hash = record[0]
        series.symbol = record[1]
        series.timestamp = record[2]
        series.date = datetime(record[3], record[4], record[5])
        series.open = record[6]
        series.high = record[7]
        series.low = record[8]
        series.close = record[9]
        series.adj_close = record[10]
        series.volume = record[11]
        series.dividend = record[12]
        series.currency = record[13]
        series.split = record[14]

        series.hash = hash(series)

        return series

    def __hash__(self):
        """
        Acquire a hash which is the unique timepoint
        combined with the symbol fo this record

        :return: Hash
        """
        return hash(self.symbol) + hash(self.timestamp)

    def in_year(self, year):
        """
        Returns whether the year matches

        :param year: Year to check
        :return: True if match
        """
        return self.date.year == year

    def in_month(self, month):
        """
        Returns whether the month matches

        :param month: Month to check
        :return: True if match
        """
        return self.date.month == month

    def in_date(self, date):
        """
        Returns whether the date matches

        :param date: Date to check
        :return: True if match
        """
        return self.date.date == date

    def serialise(self):
        """
        Serialise data for build-insertion

        :return: Serialised data
        """
        return (self.hash,
                self.symbol,
                self.timestamp,
                self.date.year,
                self.date.month,
                self.date.day,
                self.open,
                self.high,
                self.low,
                self.close,
                self.adj_close,
                self.volume,
                self.dividend,
                self.currency,
                self.split)
