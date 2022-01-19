class QueryBuilder(object):
    """
    Simple builder pattern for producing query
    URLs compatible with the AlphaVantage API
    """
    function = None
    key = None
    keywords = None
    data_type = None
    output_size = None
    symbol = None
    from_currency = None
    to_currency = None
    from_symbol = None
    to_symbol = None
    interval = None

    # Base query string (built upon)
    query = "/query?"

    # First item (determine whether to append with &)
    first = None

    def __init__(self):
        """
        Constructor, ensures first item built is
        applied without '&'
        """
        self.first = True

    @staticmethod
    def create():
        """
        Static method for creating objects built
        in-line

        :return instance
        """
        return QueryBuilder()

    def function(self, function):
        """
        Supply the function

        :param function Function
        """
        text = None
        if self.first is True:
            text = "function="
            self.first = False
        else:
            text = "&function="
        self.query = self.query + text + function
        return self

    def key(self, key):
        """
        Supply the api key

        :param key Key
        """
        text = None
        if self.first is True:
            text = "apikey="
            self.first = False
        else:
            text = "&apikey="
        self.query = self.query + text + key
        return self

    def keywords(self, keywords):
        """
        Supply the keywords

        :param keywords Keywords
        """
        text = None
        if self.first is True:
            text = "keywords="
            self.first = False
        else:
            text = "&keywords="
        self.query = self.query + text + keywords
        return self

    def data_type(self, data_type):
        """
        Supply the data type

        :param data_type Data type
        """
        text = None
        if self.first is True:
            text = "datatype="
            self.first = False
        else:
            text = "&datatype="
        self.query = self.query + text + data_type
        return self

    def output_size(self, size):
        """
        Supply the output size

        :param size Size
        """
        text = None
        if self.first is True:
            text = "outputsize="
            self.first = False
        else:
            text = "&outputsize="
        self.query = self.query + text + size
        return self

    def symbol(self, symbol):
        """
        Supply the symbol

        :param symbol Symbol
        """
        text = None
        if self.first is True:
            text = "symbol="
            self.first = False
        else:
            text = "&symbol="
        self.query = self.query + text + symbol
        return self

    def from_currency(self, currency):
        """
        Supply the from currency

        :param currency Currency
        """
        text = None
        if self.first is True:
            text = "from_currency="
            self.first = False
        else:
            text = "&from_currency="
        self.query = self.query + text + currency
        return self

    def to_currency(self, currency):
        """
        Supply the to currency

        :param currency Currency
        """
        text = None
        if self.first is True:
            text = "to_currency="
            self.first = False
        else:
            text = "&to_currency="
        self.query = self.query + text + currency
        return self

    def from_symbol(self, currency):
        """
        Supply the from currency

        :param currency Currency
        """
        text = None
        if self.first is True:
            text = "from_symbol="
            self.first = False
        else:
            text = "&from_symbol="
        self.query = self.query + text + currency
        return self

    def to_symbol(self, currency):
        """
        Supply the to currency

        :param currency Currency
        """
        text = None
        if self.first is True:
            text = "to_symbol="
            self.first = False
        else:
            text = "&to_symbol="
        self.query = self.query + text + currency
        return self

    def interval(self, interval):
        """
        Supply the interval

        :param interval Interval
        """
        text = None
        if self.first is True:
            text = "interval="
            self.first = False
        else:
            text = "&interval="
        self.query = self.query + text + interval
        return self

    def url(self):
        """
        Get the built URL

        :return: URL
        """
        return self.query
