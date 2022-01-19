from babel import numbers


class CurrencySymbol:
    """
    Simple class used to get a currency symbol
    provided an ISO compatible currency code e.g.
    AUD, GBP, USD and CAD
    """

    @staticmethod
    def get_symbol(iso_symbol):
        """
        Get the UTF symbol provided an ISO
        currency code

        :param iso_symbol: Currency code (e.g. GBP)
        :return: Currency symbol (e.g. £)
        """
        return numbers.format_currency(0, iso_symbol, locale='en_GB', currency_digits=False).replace("0.00", "")
