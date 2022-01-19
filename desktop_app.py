from qdarkstyle import load_stylesheet
from csv import reader
from logging import basicConfig, DEBUG
from multiprocessing.pool import ThreadPool
from PyQt5.QtWidgets import QApplication
from sys import argv

from core import AppCore
from widget import Launcher


# Create Qt application
qt_application = QApplication(argv)
qt_application.setStyleSheet(load_stylesheet(qt_api='pyqt5'))

# Setup application logging
basicConfig(level=DEBUG)

# Create core interface
application_core = AppCore()

# Supply default set of API keys
keys = open("keys.txt")
keys = reader(keys, delimiter='\n')
application_core.reset_used_keys()
application_core.add_api_keys(keys)

# Create thread pool
application_core.threadPool = ThreadPool(8)
application_core.qt_application = qt_application

# Create and display launcher
application_core.launcher = Launcher()
application_core.launcher.setup_application_widgets()
application_core.launcher.show()

# Start application event loop
qt_application.exec_()

# Ensure all threads have terminated
application_core.threadPool.terminate()
application_core.threadPool.join()
