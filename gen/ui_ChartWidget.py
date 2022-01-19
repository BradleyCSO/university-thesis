# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChartWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChartWidget(object):
    def setupUi(self, ChartWidget):
        ChartWidget.setObjectName("ChartWidget")
        ChartWidget.resize(1081, 775)
        self.gridLayout = QtWidgets.QGridLayout(ChartWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.chartView = QChartView(ChartWidget)
        self.chartView.setObjectName("chartView")
        self.gridLayout.addWidget(self.chartView, 0, 0, 1, 1)

        self.retranslateUi(ChartWidget)
        QtCore.QMetaObject.connectSlotsByName(ChartWidget)

    def retranslateUi(self, ChartWidget):
        _translate = QtCore.QCoreApplication.translate
        ChartWidget.setWindowTitle(_translate("ChartWidget", "Form"))
from PyQt5.QtChart import QChartView
