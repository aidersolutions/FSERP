# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'department_add_popup.ui'
#
# Created: Mon Jun  8 12:25:52 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_department_popup(object):
    def setupUi(self, department_popup):
        department_popup.setObjectName("department_popup")
        department_popup.resize(368, 127)
        self.gridLayout_2 = QtGui.QGridLayout(department_popup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtGui.QLabel(department_popup)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.department_add_id_lineedit = QtGui.QLineEdit(department_popup)
        self.department_add_id_lineedit.setObjectName("department_add_id_lineedit")
        self.gridLayout.addWidget(self.department_add_id_lineedit, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(department_popup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.department_add_name_lineedit = QtGui.QLineEdit(department_popup)
        self.department_add_name_lineedit.setObjectName("department_add_name_lineedit")
        self.gridLayout.addWidget(self.department_add_name_lineedit, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.department_add_delete_button = QtGui.QPushButton(department_popup)
        self.department_add_delete_button.setObjectName("department_add_delete_button")
        self.horizontalLayout_2.addWidget(self.department_add_delete_button)
        self.department_add_save_button = QtGui.QPushButton(department_popup)
        self.department_add_save_button.setObjectName("department_add_save_button")
        self.horizontalLayout_2.addWidget(self.department_add_save_button)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(department_popup)
        QtCore.QMetaObject.connectSlotsByName(department_popup)
        department_popup.setTabOrder(self.department_add_id_lineedit, self.department_add_name_lineedit)
        department_popup.setTabOrder(self.department_add_name_lineedit, self.department_add_save_button)
        department_popup.setTabOrder(self.department_add_save_button, self.department_add_delete_button)

    def retranslateUi(self, department_popup):
        department_popup.setWindowTitle(QtGui.QApplication.translate("department_popup", "Department", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("department_popup", "Department ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("department_popup", "Department Name", None, QtGui.QApplication.UnicodeUTF8))
        self.department_add_delete_button.setText(QtGui.QApplication.translate("department_popup", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.department_add_save_button.setText(QtGui.QApplication.translate("department_popup", "Save", None, QtGui.QApplication.UnicodeUTF8))

