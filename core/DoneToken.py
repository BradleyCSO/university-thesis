from core.SafeCounter import SafeCounter


class DoneToken(SafeCounter):
    """
    Safe token which can be configured to
    execute a callback function
    """
    callback = None
    count = None

    def __init__(self, callback, count, value=0):
        """
        Initialise with callback and count

        :param callback: Callback to invoke upon reaching count
        :param count: Count to invoke callback at
        :param value: Starting value (default: 0)
        """
        super().__init__(value)

        # Assign values
        self.callback = callback
        self.count = count

    def inc(self):
        """
        Increment stored value by 1 and invoke
        callback is count is met

        :return New value
        """
        val = super().inc()
        self.invoke()

    def dec(self):
        """
        Decrement stored value by 1 and invoke
        callback is count is met

        :return New value
        """
        val = super().dec()
        self.invoke()

    def invoke(self):
        """
        Invokes the function if the stored
        value matches count
        """
        if self.val() == self.count:
            self.callback()
