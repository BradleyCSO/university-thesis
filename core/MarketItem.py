class MarketItem:
    """
    Very basic storage class which contains all
    of the information de-serialised from a query
    result, ideally this would be a protocol buffer
    message or similar
    """
    symbol = None
    name = None
    type = None
    region = None
    open = None
    close = None
    zone = None
    currency = None
    match = None

    def __init__(self, json):
        self.symbol = json['1. symbol']
        self.name = json['2. name']
        self.type = json['3. type']
        self.region = json['4. region']
        self.open = json['5. marketOpen']
        self.close = json['6. marketClose']
        self.zone = json['7. timezone']
        self.currency = json['8. currency']
        self.match = json['9. matchScore']
