# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadingWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingWidget(object):
    def setupUi(self, LoadingWidget):
        LoadingWidget.setObjectName("LoadingWidget")
        LoadingWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(LoadingWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.loadingLabel = QtWidgets.QLabel(LoadingWidget)
        self.loadingLabel.setText("")
        self.loadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadingLabel.setObjectName("loadingLabel")
        self.gridLayout.addWidget(self.loadingLabel, 0, 0, 1, 1)

        self.retranslateUi(LoadingWidget)
        QtCore.QMetaObject.connectSlotsByName(LoadingWidget)

    def retranslateUi(self, LoadingWidget):
        _translate = QtCore.QCoreApplication.translate
        LoadingWidget.setWindowTitle(_translate("LoadingWidget", "Loading..."))
