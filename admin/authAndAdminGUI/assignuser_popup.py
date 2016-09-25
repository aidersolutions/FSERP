# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assignuser_popup.ui'
#
# Created: Mon Jun 29 20:09:26 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_adduser(object):
    def setupUi(self, adduser):
        adduser.setObjectName("adduser")
        adduser.resize(270, 92)
        self.verticalLayout = QtGui.QVBoxLayout(adduser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.adduser_combobox = QtGui.QComboBox(adduser)
        self.adduser_combobox.setObjectName("adduser_combobox")
        self.verticalLayout.addWidget(self.adduser_combobox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.adduser_add_button = QtGui.QPushButton(adduser)
        self.adduser_add_button.setObjectName("adduser_add_button")
        self.horizontalLayout.addWidget(self.adduser_add_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(adduser)
        QtCore.QMetaObject.connectSlotsByName(adduser)

    def retranslateUi(self, adduser):
        adduser.setWindowTitle(QtGui.QApplication.translate("adduser", "Assign User", None, QtGui.QApplication.UnicodeUTF8))
        self.adduser_add_button.setText(QtGui.QApplication.translate("adduser", "Add", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    adduser = QtGui.QDialog()
    ui = Ui_adduser()
    ui.setupUi(adduser)
    adduser.show()
    sys.exit(app.exec_())

