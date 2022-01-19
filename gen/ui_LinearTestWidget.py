# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LinearTestWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LinearTestWidget(object):
    def setupUi(self, LinearTestWidget):
        LinearTestWidget.setObjectName("LinearTestWidget")
        LinearTestWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(LinearTestWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.configLayout = QtWidgets.QGridLayout()
        self.configLayout.setHorizontalSpacing(0)
        self.configLayout.setVerticalSpacing(2)
        self.configLayout.setObjectName("configLayout")
        self.dayValue = QtWidgets.QLineEdit(LinearTestWidget)
        self.dayValue.setObjectName("dayValue")
        self.configLayout.addWidget(self.dayValue, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(LinearTestWidget)
        self.label_3.setObjectName("label_3")
        self.configLayout.addWidget(self.label_3, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.configLayout.addItem(spacerItem, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.configLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.testValue = QtWidgets.QSpinBox(LinearTestWidget)
        self.testValue.setMinimum(1)
        self.testValue.setProperty("value", 20)
        self.testValue.setObjectName("testValue")
        self.configLayout.addWidget(self.testValue, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(LinearTestWidget)
        self.label_5.setObjectName("label_5")
        self.configLayout.addWidget(self.label_5, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.configLayout.addItem(spacerItem2, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.configLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.maxValue = QtWidgets.QLineEdit(LinearTestWidget)
        self.maxValue.setObjectName("maxValue")
        self.configLayout.addWidget(self.maxValue, 1, 2, 1, 1)
        self.minValue = QtWidgets.QLineEdit(LinearTestWidget)
        self.minValue.setObjectName("minValue")
        self.configLayout.addWidget(self.minValue, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(LinearTestWidget)
        self.label_2.setObjectName("label_2")
        self.configLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(LinearTestWidget)
        self.label.setObjectName("label")
        self.configLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.configLayout, 0, 0, 1, 1)
        self.chartWidget = QtWidgets.QWidget(LinearTestWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartWidget.sizePolicy().hasHeightForWidth())
        self.chartWidget.setSizePolicy(sizePolicy)
        self.chartWidget.setObjectName("chartWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.chartWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout.addWidget(self.chartWidget, 1, 0, 1, 1)

        self.retranslateUi(LinearTestWidget)
        QtCore.QMetaObject.connectSlotsByName(LinearTestWidget)

    def retranslateUi(self, LinearTestWidget):
        _translate = QtCore.QCoreApplication.translate
        LinearTestWidget.setWindowTitle(_translate("LinearTestWidget", "Form"))
        self.dayValue.setPlaceholderText(_translate("LinearTestWidget", "All"))
        self.label_3.setText(_translate("LinearTestWidget", "Load history (days)"))
        self.testValue.setSuffix(_translate("LinearTestWidget", "%"))
        self.label_5.setText(_translate("LinearTestWidget", "Test split"))
        self.maxValue.setPlaceholderText(_translate("LinearTestWidget", "Any"))
        self.minValue.setPlaceholderText(_translate("LinearTestWidget", "Any"))
        self.label_2.setText(_translate("LinearTestWidget", "Maximum load value"))
        self.label.setText(_translate("LinearTestWidget", "Minimum load value"))
