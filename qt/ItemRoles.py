from PyQt5.QtCore import Qt


class ItemRoles:
    """
    Ordinal to contain data which can be stored
    within QStandardItems and be accessed at a
    later point in time
    """
    SERIES_DATA_ROLE = Qt.UserRole + 1000
    MODE_WIDGET_ROLE = Qt.UserRole + 1001
