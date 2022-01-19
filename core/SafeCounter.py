from threading import Lock


class SafeCounter:
    """
    Simple class which provides a thread-safe
    implementation for counting integers
    """
    lock = Lock()

    def __init__(self, value=0):
        """
        Initialise counter with value

        :param value: Start value (default: 0)
        """
        self.value = value

    def inc(self):
        """
        Increment stored value by 1

        :return New value
        """
        self.lock.acquire()
        self.value += 1
        value = self.value
        self.lock.release()
        return value

    def dec(self):
        """
        Decrement stored value by 1

        :return New value
        """
        self.lock.acquire()
        self.value -= 1
        value = self.value
        self.lock.release()
        return value

    def val(self):
        """
        Returns stored value

        :return Stored value
        """
        self.lock.acquire()
        val = self.value
        self.lock.release()
        return val
