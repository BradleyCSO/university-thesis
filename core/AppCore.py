from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from urllib3 import HTTPSConnectionPool
from core.ApplicationDataStore import ApplicationDataStore
from core.singleton import singleton
from core.ThreadForwarder import ThreadForwarder
from core.KeyStore import KeyStore


@singleton
class AppCore(object):
    """
    Core object which contains application
    runtime information used for various things
    """
    threadPool = None
    forwarder = ThreadForwarder()
    data_store = ApplicationDataStore()
    key_store = KeyStore()
    qt_application = None
    launcher = None
    stock_time_series_window = None
    stock_time_series_analysis_window = None
    currency_window = None
    dollar_index_window = None
    connection_pool = HTTPSConnectionPool("www.alphavantage.co:443", maxsize=8)

    def reset_used_keys(self):
        """
        For any key which hasn't been used in 24 hours, reset
        the used count
        """
        self.key_store.lock.acquire()
        # Previous date 00:00
        now = datetime.utcnow()
        old = now - timedelta(hours=now.hour,
                              minutes=now.minute,
                              seconds=now.second,
                              microseconds=now.microsecond,
                              days=1)

        # Fetch all records older than this
        self.key_store.cursor.execute('SELECT * FROM api_key_store WHERE last_accessed < ' + str(old.timestamp()))
        data = self.key_store.cursor.fetchall()

        # Finalised key records to re-insert
        insert_keys = []

        for record in data:
            # Update each record to reset the
            # used index to 0
            temp = list(record)
            temp[2] = 0
            insert_keys.append(tuple(temp))

        # Insert updated records
        self.key_store.cursor.executemany('REPLACE INTO api_key_store VALUES (?,?,?)', insert_keys)
        self.key_store.lock.release()

    def add_api_keys(self, keys):
        """
        Add API keys to the application DB

        :param keys: Key list
        """
        self.key_store.lock.acquire()
        # Tuples to insert
        insert_keys = []
        for key in keys:
            insert_keys.append((key[0], 0.0, 0))

        # Bulk insert
        self.key_store.cursor.executemany('INSERT OR IGNORE INTO api_key_store VALUES (?,?,?)', insert_keys)

        # Commit
        self.key_store.connection.commit()
        self.key_store.lock.release()

    def get_api_key(self) -> str:
        """
        Returns a random API key from selection
        as not to exhaust the usages of a single
        key

        :return: Random key
        """
        self.key_store.lock.acquire()

        # Get least recent accessed key which hasn't
        # already been used 500 times (unlikely)
        self.key_store.cursor.execute('SELECT * FROM api_key_store WHERE used < 500 ORDER BY last_accessed LIMIT 1')
        key = self.key_store.cursor.fetchone()

        # Update time/usage properties
        new_time = datetime.utcnow().timestamp()
        new_used = key[2] + 1

        # New insert key
        insert_key = (key[0], new_time, new_used)

        # Replace record for key
        self.key_store.cursor.execute('REPLACE INTO api_key_store VALUES (?,?,?)', insert_key)
        self.key_store.connection.commit()
        self.key_store.lock.release()

        # Return actual key
        return key[0]

    def get_thread_pool(self) -> ThreadPool:
        """
        Returns the thread pool instance

        :return: Thread pool
        """
        return self.threadPool

    def get_forwarder(self) -> ThreadForwarder:
        """
        Returns the thread forwarder instance

        :return: Thread forwarder
        """
        return self.forwarder

    def get_data_store(self) -> ApplicationDataStore:
        """
        Returns the historic store instance

        :return: Thread forwarder
        """
        return self.data_store
