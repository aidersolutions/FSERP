# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu_for_each_week.ui'
#
# Created: Thu May 21 21:32:02 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_menu_this_day(object):
    def setupUi(self, menu_this_day):
        menu_this_day.setObjectName("menu_this_day")
        menu_this_day.resize(249, 153)
        self.gridLayout = QtGui.QGridLayout(menu_this_day)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(menu_this_day)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.menuperday_code_label = QtGui.QLabel(menu_this_day)
        self.menuperday_code_label.setObjectName("menuperday_code_label")
        self.horizontalLayout.addWidget(self.menuperday_code_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_4 = QtGui.QLabel(menu_this_day)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.menuperday_name_label = QtGui.QLabel(menu_this_day)
        self.menuperday_name_label.setObjectName("menuperday_name_label")
        self.horizontalLayout_3.addWidget(self.menuperday_name_label)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 4)
        self.line = QtGui.QFrame(menu_this_day)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 4)
        self.label_2 = QtGui.QLabel(menu_this_day)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.menuperday_quantity_linedit = QtGui.QLineEdit(menu_this_day)
        self.menuperday_quantity_linedit.setObjectName("menuperday_quantity_linedit")
        self.gridLayout.addWidget(self.menuperday_quantity_linedit, 3, 2, 1, 2)
        self.menuperday_delete_button = QtGui.QPushButton(menu_this_day)
        self.menuperday_delete_button.setObjectName("menuperday_delete_button")
        self.gridLayout.addWidget(self.menuperday_delete_button, 4, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 2)
        self.menuperday_save_button = QtGui.QPushButton(menu_this_day)
        self.menuperday_save_button.setObjectName("menuperday_save_button")
        self.gridLayout.addWidget(self.menuperday_save_button, 4, 3, 1, 1)

        self.retranslateUi(menu_this_day)
        QtCore.QMetaObject.connectSlotsByName(menu_this_day)
        menu_this_day.setTabOrder(self.menuperday_quantity_linedit, self.menuperday_save_button)
        menu_this_day.setTabOrder(self.menuperday_save_button, self.menuperday_delete_button)

    def retranslateUi(self, menu_this_day):
        menu_this_day.setWindowTitle(QtGui.QApplication.translate("menu_this_day", "Menu This Day", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("menu_this_day", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.menuperday_code_label.setText(QtGui.QApplication.translate("menu_this_day", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("menu_this_day", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.menuperday_name_label.setText(QtGui.QApplication.translate("menu_this_day", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("menu_this_day", "Quantity Sold", None, QtGui.QApplication.UnicodeUTF8))
        self.menuperday_delete_button.setText(QtGui.QApplication.translate("menu_this_day", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.menuperday_save_button.setText(QtGui.QApplication.translate("menu_this_day", "Save", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    menu_this_day = QtGui.QDialog()
    ui = Ui_menu_this_day()
    ui.setupUi(menu_this_day)
    menu_this_day.show()
    sys.exit(app.exec_())

