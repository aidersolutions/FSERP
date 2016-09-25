# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_item_newsupplier.ui'
#
# Created: Thu May 28 19:58:54 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_new_supplier(object):
    def setupUi(self, new_supplier):
        new_supplier.setObjectName("new_supplier")
        new_supplier.resize(347, 122)
        self.verticalLayout = QtGui.QVBoxLayout(new_supplier)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(new_supplier)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(new_supplier)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.newsupplier_code_label = QtGui.QLabel(new_supplier)
        self.newsupplier_code_label.setObjectName("newsupplier_code_label")
        self.horizontalLayout.addWidget(self.newsupplier_code_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(new_supplier)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.newsupplier_name_combobox = QtGui.QComboBox(new_supplier)
        self.newsupplier_name_combobox.setObjectName("newsupplier_name_combobox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.newsupplier_name_combobox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.newsupplier_add_button = QtGui.QPushButton(new_supplier)
        self.newsupplier_add_button.setObjectName("newsupplier_add_button")
        self.horizontalLayout_2.addWidget(self.newsupplier_add_button)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(new_supplier)
        QtCore.QMetaObject.connectSlotsByName(new_supplier)

    def retranslateUi(self, new_supplier):
        new_supplier.setWindowTitle(QtGui.QApplication.translate("new_supplier", "New Supplier", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("new_supplier", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.newsupplier_code_label.setText(QtGui.QApplication.translate("new_supplier", "No User Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("new_supplier", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.newsupplier_add_button.setText(QtGui.QApplication.translate("new_supplier", "Add", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    new_supplier = QtGui.QDialog()
    ui = Ui_new_supplier()
    ui.setupUi(new_supplier)
    new_supplier.show()
    sys.exit(app.exec_())

