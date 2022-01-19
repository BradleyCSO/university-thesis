from os import path
from PyQt5.uic import compileUi


def compile_ui(ui_file):
    """
    Simple function which can compile a UI file into
    a python file and applies the appropriate prefix

    :param ui_file: File target
    """
    py_file = "ui_" + path.splitext(ui_file)[0] + ".py"
    fp = open(py_file, "w")
    compileUi(ui_file, fp, from_imports=True)
    fp.close()


# Add UI files as required here
ui_list = ['AnalysisWidget.ui',
           'CurrencyDisplay.ui',
           'Launcher.ui',
           'LoadingWidget.ui',
           'StockTimeSeriesDisplay.ui',
           'DollarIndexDisplay.ui',
           'ChartWidget.ui',
           'LinearTestWidget.ui']

for ui in ui_list:
    # Build specified ui
    compile_ui(ui)
