# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnalysisWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnalysisWidget(object):
    def setupUi(self, AnalysisWidget):
        AnalysisWidget.setObjectName("AnalysisWidget")
        AnalysisWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(AnalysisWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(AnalysisWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.linearTestTab = QtWidgets.QWidget()
        self.linearTestTab.setObjectName("linearTestTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.linearTestTab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.linearTestTab, "")
        self.linearRegTab = QtWidgets.QWidget()
        self.linearRegTab.setObjectName("linearRegTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.linearRegTab)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget.addTab(self.linearRegTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(AnalysisWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AnalysisWidget)

    def retranslateUi(self, AnalysisWidget):
        _translate = QtCore.QCoreApplication.translate
        AnalysisWidget.setWindowTitle(_translate("AnalysisWidget", "Stock Analysis Project - Analysis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linearTestTab), _translate("AnalysisWidget", "Linear regression test"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linearRegTab), _translate("AnalysisWidget", "Linear regression analysis"))
