# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Launcher.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Launcher(object):
    def setupUi(self, Launcher):
        Launcher.setObjectName("Launcher")
        Launcher.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Launcher)
        self.gridLayout.setObjectName("gridLayout")
        self.modeView = QtWidgets.QListView(Launcher)
        self.modeView.setObjectName("modeView")
        self.gridLayout.addWidget(self.modeView, 0, 0, 1, 1)

        self.retranslateUi(Launcher)
        QtCore.QMetaObject.connectSlotsByName(Launcher)

    def retranslateUi(self, Launcher):
        _translate = QtCore.QCoreApplication.translate
        Launcher.setWindowTitle(_translate("Launcher", "Market Analysis - Launcher"))
