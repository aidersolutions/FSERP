# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addroles_popup.ui'
#
# Created: Mon Jun 29 15:29:06 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addroles(object):
    def setupUi(self, addroles):
        addroles.setObjectName("addroles")
        addroles.resize(269, 93)
        self.verticalLayout = QtGui.QVBoxLayout(addroles)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addroles_combobox = QtGui.QComboBox(addroles)
        self.addroles_combobox.setObjectName("addroles_combobox")
        self.verticalLayout.addWidget(self.addroles_combobox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addroles_add_button = QtGui.QPushButton(addroles)
        self.addroles_add_button.setObjectName("addroles_add_button")
        self.horizontalLayout.addWidget(self.addroles_add_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(addroles)
        QtCore.QMetaObject.connectSlotsByName(addroles)

    def retranslateUi(self, addroles):
        addroles.setWindowTitle(QtGui.QApplication.translate("addroles", "Add Roles", None, QtGui.QApplication.UnicodeUTF8))
        self.addroles_add_button.setText(QtGui.QApplication.translate("addroles", "Add", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    addroles = QtGui.QDialog()
    ui = Ui_addroles()
    ui.setupUi(addroles)
    addroles.show()
    sys.exit(app.exec_())

