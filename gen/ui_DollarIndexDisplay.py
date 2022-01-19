# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DollarIndexDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DollarIndexDisplay(object):
    def setupUi(self, DollarIndexDisplay):
        DollarIndexDisplay.setObjectName("DollarIndexDisplay")
        DollarIndexDisplay.resize(1159, 512)
        self.gridLayout = QtWidgets.QGridLayout(DollarIndexDisplay)
        self.gridLayout.setObjectName("gridLayout")
        self.chartView = QChartView(DollarIndexDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartView.sizePolicy().hasHeightForWidth())
        self.chartView.setSizePolicy(sizePolicy)
        self.chartView.setObjectName("chartView")
        self.gridLayout.addWidget(self.chartView, 1, 0, 1, 1)
        self.horizontalWidget = QtWidgets.QWidget(DollarIndexDisplay)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentLabel = QtWidgets.QLabel(self.horizontalWidget)
        self.currentLabel.setObjectName("currentLabel")
        self.horizontalLayout.addWidget(self.currentLabel)
        self.currentText = QtWidgets.QLineEdit(self.horizontalWidget)
        self.currentText.setReadOnly(True)
        self.currentText.setObjectName("currentText")
        self.horizontalLayout.addWidget(self.currentText)
        self.gridLayout.addWidget(self.horizontalWidget, 0, 0, 1, 1)
        self.buttonWidget = QtWidgets.QWidget(DollarIndexDisplay)
        self.buttonWidget.setObjectName("buttonWidget")
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(2)
        self.buttonLayout.setObjectName("buttonLayout")
        self.button7d = QtWidgets.QPushButton(self.buttonWidget)
        self.button7d.setObjectName("button7d")
        self.buttonLayout.addWidget(self.button7d)
        self.button30d = QtWidgets.QPushButton(self.buttonWidget)
        self.button30d.setObjectName("button30d")
        self.buttonLayout.addWidget(self.button30d)
        self.button1y = QtWidgets.QPushButton(self.buttonWidget)
        self.button1y.setObjectName("button1y")
        self.buttonLayout.addWidget(self.button1y)
        self.button5y = QtWidgets.QPushButton(self.buttonWidget)
        self.button5y.setObjectName("button5y")
        self.buttonLayout.addWidget(self.button5y)
        self.gridLayout.addWidget(self.buttonWidget, 2, 0, 1, 1)

        self.retranslateUi(DollarIndexDisplay)
        QtCore.QMetaObject.connectSlotsByName(DollarIndexDisplay)

    def retranslateUi(self, DollarIndexDisplay):
        _translate = QtCore.QCoreApplication.translate
        DollarIndexDisplay.setWindowTitle(_translate("DollarIndexDisplay", "Market Analysis - US Dollar Index"))
        self.currentLabel.setText(_translate("DollarIndexDisplay", "Current US Dollar Index (USDX):"))
        self.button7d.setText(_translate("DollarIndexDisplay", "7 day"))
        self.button30d.setText(_translate("DollarIndexDisplay", "30 day"))
        self.button1y.setText(_translate("DollarIndexDisplay", "1 year"))
        self.button5y.setText(_translate("DollarIndexDisplay", "5 year"))
from PyQt5.QtChart import QChartView
