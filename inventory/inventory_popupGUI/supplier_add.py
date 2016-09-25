# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'supplier_add.ui'
#
# Created: Thu Jun 11 18:30:59 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Supplier_Add(object):
    def setupUi(self, Supplier_Add):
        Supplier_Add.setObjectName("Supplier_Add")
        Supplier_Add.resize(334, 238)
        self.verticalLayout = QtGui.QVBoxLayout(Supplier_Add)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Supplier_Add)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.supplieradd_name_linedit = QtGui.QLineEdit(Supplier_Add)
        self.supplieradd_name_linedit.setObjectName("supplieradd_name_linedit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.supplieradd_name_linedit)
        self.label_2 = QtGui.QLabel(Supplier_Add)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.supplieradd_street_linedit = QtGui.QLineEdit(Supplier_Add)
        self.supplieradd_street_linedit.setObjectName("supplieradd_street_linedit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.supplieradd_street_linedit)
        self.label_8 = QtGui.QLabel(Supplier_Add)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.supplieradd_city_linedit = QtGui.QLineEdit(Supplier_Add)
        self.supplieradd_city_linedit.setObjectName("supplieradd_city_linedit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.supplieradd_city_linedit)
        self.label_9 = QtGui.QLabel(Supplier_Add)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_9)
        self.supplieradd_pin_linedit = QtGui.QLineEdit(Supplier_Add)
        self.supplieradd_pin_linedit.setObjectName("supplieradd_pin_linedit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.supplieradd_pin_linedit)
        self.label_4 = QtGui.QLabel(Supplier_Add)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.supplieradd_code_linedit = QtGui.QLineEdit(Supplier_Add)
        self.supplieradd_code_linedit.setObjectName("supplieradd_code_linedit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.supplieradd_code_linedit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.supplieradd_delete_button = QtGui.QPushButton(Supplier_Add)
        self.supplieradd_delete_button.setObjectName("supplieradd_delete_button")
        self.horizontalLayout.addWidget(self.supplieradd_delete_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.supplieradd_save_button = QtGui.QPushButton(Supplier_Add)
        self.supplieradd_save_button.setObjectName("supplieradd_save_button")
        self.horizontalLayout.addWidget(self.supplieradd_save_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Supplier_Add)
        QtCore.QMetaObject.connectSlotsByName(Supplier_Add)
        Supplier_Add.setTabOrder(self.supplieradd_code_linedit, self.supplieradd_name_linedit)
        Supplier_Add.setTabOrder(self.supplieradd_name_linedit, self.supplieradd_street_linedit)
        Supplier_Add.setTabOrder(self.supplieradd_street_linedit, self.supplieradd_city_linedit)
        Supplier_Add.setTabOrder(self.supplieradd_city_linedit, self.supplieradd_pin_linedit)
        Supplier_Add.setTabOrder(self.supplieradd_pin_linedit, self.supplieradd_save_button)
        Supplier_Add.setTabOrder(self.supplieradd_save_button, self.supplieradd_delete_button)

    def retranslateUi(self, Supplier_Add):
        Supplier_Add.setWindowTitle(QtGui.QApplication.translate("Supplier_Add", "Supplier Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Supplier_Add", "Supplier Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Supplier_Add", "Street & Lane", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Supplier_Add", "City", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Supplier_Add", "Pin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Supplier_Add", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.supplieradd_delete_button.setText(QtGui.QApplication.translate("Supplier_Add", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.supplieradd_save_button.setText(QtGui.QApplication.translate("Supplier_Add", "Save", None, QtGui.QApplication.UnicodeUTF8))

