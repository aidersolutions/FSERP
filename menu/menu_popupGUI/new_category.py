# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_category.ui'
#
# Created: Sat May 23 14:28:38 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_new_category(object):
    def setupUi(self, new_category):
        new_category.setObjectName("new_category")
        new_category.resize(249, 113)
        self.verticalLayout = QtGui.QVBoxLayout(new_category)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtGui.QLabel(new_category)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.categorydialogue_newcategory_linedit = QtGui.QLineEdit(new_category)
        self.categorydialogue_newcategory_linedit.setObjectName("categorydialogue_newcategory_linedit")
        self.horizontalLayout_2.addWidget(self.categorydialogue_newcategory_linedit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.categorydialogue_addcategory_button = QtGui.QPushButton(new_category)
        self.categorydialogue_addcategory_button.setObjectName("categorydialogue_addcategory_button")
        self.horizontalLayout.addWidget(self.categorydialogue_addcategory_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(new_category)
        QtCore.QMetaObject.connectSlotsByName(new_category)

    def retranslateUi(self, new_category):
        new_category.setWindowTitle(QtGui.QApplication.translate("new_category", "New Category", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("new_category", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.categorydialogue_addcategory_button.setText(QtGui.QApplication.translate("new_category", "Add Category", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    new_category = QtGui.QDialog()
    ui = Ui_new_category()
    ui.setupUi(new_category)
    new_category.show()
    sys.exit(app.exec_())

