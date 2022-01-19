# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CurrencyDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CurrencyDisplay(object):
    def setupUi(self, CurrencyDisplay):
        CurrencyDisplay.setObjectName("CurrencyDisplay")
        CurrencyDisplay.resize(1206, 849)
        self.primaryLayout = QtWidgets.QGridLayout(CurrencyDisplay)
        self.primaryLayout.setObjectName("primaryLayout")
        self.selectionWidget = QtWidgets.QWidget(CurrencyDisplay)
        self.selectionWidget.setObjectName("selectionWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.selectionWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.fromCurrencyView = QtWidgets.QListView(self.selectionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fromCurrencyView.sizePolicy().hasHeightForWidth())
        self.fromCurrencyView.setSizePolicy(sizePolicy)
        self.fromCurrencyView.setObjectName("fromCurrencyView")
        self.gridLayout.addWidget(self.fromCurrencyView, 1, 0, 1, 1)
        self.toCurrencyView = QtWidgets.QListView(self.selectionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toCurrencyView.sizePolicy().hasHeightForWidth())
        self.toCurrencyView.setSizePolicy(sizePolicy)
        self.toCurrencyView.setObjectName("toCurrencyView")
        self.gridLayout.addWidget(self.toCurrencyView, 1, 1, 1, 1)
        self.fromLabel = QtWidgets.QLabel(self.selectionWidget)
        self.fromLabel.setObjectName("fromLabel")
        self.gridLayout.addWidget(self.fromLabel, 0, 0, 1, 1)
        self.toLabel = QtWidgets.QLabel(self.selectionWidget)
        self.toLabel.setObjectName("toLabel")
        self.gridLayout.addWidget(self.toLabel, 0, 1, 1, 1)
        self.primaryLayout.addWidget(self.selectionWidget, 2, 0, 1, 1)
        self.infoWidget = QtWidgets.QWidget(CurrencyDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.infoWidget.setObjectName("infoWidget")
        self.infoLayout = QtWidgets.QGridLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setHorizontalSpacing(2)
        self.infoLayout.setVerticalSpacing(6)
        self.infoLayout.setObjectName("infoLayout")
        self.chartDisplay = QChartView(self.infoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartDisplay.sizePolicy().hasHeightForWidth())
        self.chartDisplay.setSizePolicy(sizePolicy)
        self.chartDisplay.setObjectName("chartDisplay")
        self.infoLayout.addWidget(self.chartDisplay, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentRateLabel = QtWidgets.QLabel(self.infoWidget)
        self.currentRateLabel.setObjectName("currentRateLabel")
        self.horizontalLayout.addWidget(self.currentRateLabel)
        self.currentRateArea = QtWidgets.QLineEdit(self.infoWidget)
        self.currentRateArea.setReadOnly(True)
        self.currentRateArea.setObjectName("currentRateArea")
        self.horizontalLayout.addWidget(self.currentRateArea)
        self.infoLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.primaryLayout.addWidget(self.infoWidget, 3, 0, 1, 1)
        self.viewWidget = QtWidgets.QWidget(CurrencyDisplay)
        self.viewWidget.setObjectName("viewWidget")
        self.viewLayout = QtWidgets.QHBoxLayout(self.viewWidget)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setObjectName("viewLayout")
        self.button15m = QtWidgets.QPushButton(self.viewWidget)
        self.button15m.setObjectName("button15m")
        self.viewLayout.addWidget(self.button15m)
        self.button1h = QtWidgets.QPushButton(self.viewWidget)
        self.button1h.setObjectName("button1h")
        self.viewLayout.addWidget(self.button1h)
        self.button24h = QtWidgets.QPushButton(self.viewWidget)
        self.button24h.setObjectName("button24h")
        self.viewLayout.addWidget(self.button24h)
        self.button7d = QtWidgets.QPushButton(self.viewWidget)
        self.button7d.setObjectName("button7d")
        self.viewLayout.addWidget(self.button7d)
        self.button30d = QtWidgets.QPushButton(self.viewWidget)
        self.button30d.setObjectName("button30d")
        self.viewLayout.addWidget(self.button30d)
        self.primaryLayout.addWidget(self.viewWidget, 4, 0, 1, 1)

        self.retranslateUi(CurrencyDisplay)
        QtCore.QMetaObject.connectSlotsByName(CurrencyDisplay)

    def retranslateUi(self, CurrencyDisplay):
        _translate = QtCore.QCoreApplication.translate
        CurrencyDisplay.setWindowTitle(_translate("CurrencyDisplay", "Market Analysis - Currency"))
        self.fromLabel.setText(_translate("CurrencyDisplay", "From currency:"))
        self.toLabel.setText(_translate("CurrencyDisplay", "To currency:"))
        self.currentRateLabel.setText(_translate("CurrencyDisplay", "Current change rate:"))
        self.button15m.setText(_translate("CurrencyDisplay", "15 minute"))
        self.button1h.setText(_translate("CurrencyDisplay", "60 minute"))
        self.button24h.setText(_translate("CurrencyDisplay", "24 hour"))
        self.button7d.setText(_translate("CurrencyDisplay", "7 day"))
        self.button30d.setText(_translate("CurrencyDisplay", "30 day"))
from PyQt5.QtChart import QChartView