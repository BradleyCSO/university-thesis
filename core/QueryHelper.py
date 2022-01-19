from time import sleep
from json import loads

from core.AppCore import AppCore


class QueryHelper:
    """
    Query helper which retries failed API queries
    """
    core = AppCore()
    query = None
    callback = None
    builder = None

    def __init__(self, builder, callback):
        """
        Create a query helper around a configured
        QueryBuilder object and callback

        :param builder: Function which creates builder
        :param callback: Callback to execute
        """
        self.query = builder()
        self.builder = builder
        self.callback = callback

    def retry(self):
        """
        Issued when a failure/timeout response comes in
        """
        # Delay for 5 seconds
        sleep(5.0)

        # Create new builder and wait
        self.query = self.builder()
        self.execute()

    def handle_status(self, response):
        """
        Handle an API response, either retrying upon
        failure or submitting the user provided callback

        :param response: API response
        """
        if response['Note'] == 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per ' \
                               'minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if ' \
                               'you would like to target a higher API call frequency.':
            # Retry later
            self.core.get_thread_pool().apply_async(self.retry)
        else:
            # Forward response
            self.callback(response)

    def execute(self):
        """
        Execute a query provided a builder to create
        the API URL and examine the callback
        """
        self.core.get_thread_pool().apply_async(self.core.connection_pool.request,
                                                ["GET", self.query.url()],
                                                callback=lambda result: self.handle_status(loads(result.data)))
