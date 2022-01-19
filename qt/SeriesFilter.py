from datetime import datetime


class SeriesFilter:
    """
    Simple class for filtering out excess data
    from a time series query result
    """
    interval = None
    last = None

    def __init__(self, interval):
        """
        Set a filter with a provided interval

        :param interval: Interval
        """
        # Apply values
        self.interval = interval
        self.last = datetime.fromtimestamp(0)

    def in_interval(self, timestamp):
        """
        See if timestamp is within the interval,
        returns true if it it does, otherwise false

        :param timestamp: Timestamp to compare
        :return: In interval or not
        """
        point = self.last + self.interval
        if timestamp >= point:
            self.last = timestamp
            return True
        else:
            return False
