from csv import reader
from datetime import datetime
from os import path

from core import ApplicationDataStore


def request_file():
    """
    Ask user to specify a file location containing
    yahoo finance USDX data

    :return: Path
    """
    req = input("Select USDX data file:")
    return req


def validate(text):
    """
    Returns true if the text value is not null

    :param text: Text to verify
    :return: True if not null
    """
    return text != "null"


# Create and initialise data store
data_store = ApplicationDataStore()

# List of items to insert to store
items = []

# Get file
loc = request_file()

# Process file
if path.exists(loc):
    # Open file and get buffer
    with open(loc, "r") as csv:
        # CSV parser
        rd = reader(csv)

        # Skip header
        next(rd)

        # Parse data
        for row in rd:
            # Filter for rows with null values
            nrow = list(filter(validate, row))

            # Ensure no values are null before adding to insert list
            if len(nrow) == len(row):
                # Convert timestamp
                dt = datetime.strptime(row[0], "%Y-%m-%d")

                # Build tuple for insert
                items.append((dt.timestamp(),
                              float(row[1]),
                              float(row[2]),
                              float(row[3]),
                              float(row[4]),
                              float(row[5])))

# Execute bulk insert
data_store.cursor.executemany("INSERT OR IGNORE INTO dollar_index VALUES (?,?,?,?,?,?)", items)
data_store.connection.commit()
