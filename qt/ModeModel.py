from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from qt.ItemRoles import ItemRoles


class ModeModel(QStandardItemModel):

    def __init__(self, parent=None):
        """
        Construct model with supplied parent

        :param parent: Parent object
        """
        super().__init__(parent)

    def add_mode(self, name, tooltip, widget):
        """
        Add a mode to the launcher

        :param name: Name (for display)
        :param tooltip: Tooltip (for display)
        :param widget: Widget (shown on click)
        """
        # Generate standard item which is larger
        # than the default item and is aligned to
        # the centre of the view
        mode = QStandardItem()
        mode.setText(name)
        mode.setSizeHint(QSize(40, 60))
        mode.setTextAlignment(Qt.AlignCenter)
        mode.setEditable(False)

        # Add tooltip
        mode.setToolTip(tooltip)

        # Set handler
        mode.setData(widget, ItemRoles.MODE_WIDGET_ROLE)

        # Add to model
        self.appendRow(mode)
