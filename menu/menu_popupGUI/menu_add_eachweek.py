# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu_add_eachweek.ui'
#
# Created: Mon Jun 15 17:21:47 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_add_menu_eachweek(object):
    def setupUi(self, add_menu_eachweek):
        add_menu_eachweek.setObjectName("add_menu_eachweek")
        add_menu_eachweek.resize(648, 260)
        self.gridLayout = QtGui.QGridLayout(add_menu_eachweek)
        self.gridLayout.setObjectName("gridLayout")
        self.add_eachweek_table = QtGui.QTableWidget(add_menu_eachweek)
        self.add_eachweek_table.setObjectName("add_eachweek_table")
        self.add_eachweek_table.setColumnCount(6)
        self.add_eachweek_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.add_eachweek_table.setHorizontalHeaderItem(5, item)
        self.add_eachweek_table.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.add_eachweek_table, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(379, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.add_eachweek_add_button = QtGui.QPushButton(add_menu_eachweek)
        self.add_eachweek_add_button.setObjectName("add_eachweek_add_button")
        self.gridLayout.addWidget(self.add_eachweek_add_button, 1, 1, 1, 1)

        self.retranslateUi(add_menu_eachweek)
        QtCore.QMetaObject.connectSlotsByName(add_menu_eachweek)

    def retranslateUi(self, add_menu_eachweek):
        add_menu_eachweek.setWindowTitle(QtGui.QApplication.translate("add_menu_eachweek", "Add Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("add_menu_eachweek", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("add_menu_eachweek", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("add_menu_eachweek", "Dish", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("add_menu_eachweek", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("add_menu_eachweek", "Rate", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_table.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("add_menu_eachweek", "Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.add_eachweek_add_button.setText(QtGui.QApplication.translate("add_menu_eachweek", "Add Dishes", None, QtGui.QApplication.UnicodeUTF8))

