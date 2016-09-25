# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designation_add_popup.ui'
#
# Created: Mon Jun  8 12:26:56 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_new_designation(object):
    def setupUi(self, new_designation):
        new_designation.setObjectName("new_designation")
        new_designation.resize(370, 131)
        self.gridLayout_2 = QtGui.QGridLayout(new_designation)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(new_designation)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.designation_add_code_lineedit = QtGui.QLineEdit(new_designation)
        self.designation_add_code_lineedit.setObjectName("designation_add_code_lineedit")
        self.gridLayout.addWidget(self.designation_add_code_lineedit, 0, 1, 1, 1)
        self.label = QtGui.QLabel(new_designation)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.designation_add_name_lineedit = QtGui.QLineEdit(new_designation)
        self.designation_add_name_lineedit.setObjectName("designation_add_name_lineedit")
        self.gridLayout.addWidget(self.designation_add_name_lineedit, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.designation_add_delete_button = QtGui.QPushButton(new_designation)
        self.designation_add_delete_button.setObjectName("designation_add_delete_button")
        self.horizontalLayout.addWidget(self.designation_add_delete_button)
        self.designation_add_save_button = QtGui.QPushButton(new_designation)
        self.designation_add_save_button.setObjectName("designation_add_save_button")
        self.horizontalLayout.addWidget(self.designation_add_save_button)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(new_designation)
        QtCore.QMetaObject.connectSlotsByName(new_designation)
        new_designation.setTabOrder(self.designation_add_code_lineedit, self.designation_add_name_lineedit)
        new_designation.setTabOrder(self.designation_add_name_lineedit, self.designation_add_save_button)
        new_designation.setTabOrder(self.designation_add_save_button, self.designation_add_delete_button)

    def retranslateUi(self, new_designation):
        new_designation.setWindowTitle(QtGui.QApplication.translate("new_designation", "Designation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("new_designation", "Designation Code", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("new_designation", "Designation Name", None, QtGui.QApplication.UnicodeUTF8))
        self.designation_add_delete_button.setText(QtGui.QApplication.translate("new_designation", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.designation_add_save_button.setText(QtGui.QApplication.translate("new_designation", "Save", None, QtGui.QApplication.UnicodeUTF8))

