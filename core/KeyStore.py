import sqlite3
from threading import Lock


class KeyStore:
    """
    On-disk key store to track API usage through time
    to ensure only valid keys are selected
    """
    connection = None
    cursor = None
    lock = Lock()

    def __init__(self):
        # Create an in-memory DB
        self.connection = sqlite3.connect("keys.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Setup the table
        table = open('sql/initialise_key.sql').read()

        # Create the table
        self.cursor.executescript(table)
        self.connection.commit()

    def __del__(self):
        # Drop connection to DB
        self.cursor.close()
        self.connection.close()
