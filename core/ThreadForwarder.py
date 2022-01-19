from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Invokable(object):
    """
    Wrap a function in a type that can be passed
    via Qt signal/slot functionality
    """
    function = None

    def __init__(self, function):
        """
        Create invokable with provided function

        :param function: Function to wrap
        """
        self.function = function


class ThreadForwarder(QObject):
    """
    Utility class to ensure a particular function
    is executed on the GUI thread, generally for
    anything which is updating a view
    """
    signal = pyqtSignal(Invokable)

    def __init__(self, parent=None):
        """
        Constructor which takes a parent

        :param parent: Parent object
        """
        # Initialise super
        super().__init__(parent)

        # Connect signal to handler
        self.signal.connect(self.execute)

    def forward(self, function):
        """
        Execute a function a GUI thread by emitting
        it as a signal to the built-in handler

        :param function: Function to execute on GUI
        """
        self.signal.emit(Invokable(function))

    @pyqtSlot(Invokable)
    def execute(self, invokable):
        """
        Executes a provided functor

        :param invokable: Function to run
        """
        invokable.function()
