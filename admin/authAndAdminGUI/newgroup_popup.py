# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgroup_popup.ui'
#
# Created: Mon Jun 29 15:28:53 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_newgroup(object):
    def setupUi(self, newgroup):
        newgroup.setObjectName("newgroup")
        newgroup.resize(265, 100)
        self.verticalLayout = QtGui.QVBoxLayout(newgroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(newgroup)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.newgroup_name_linedit = QtGui.QLineEdit(newgroup)
        self.newgroup_name_linedit.setObjectName("newgroup_name_linedit")
        self.horizontalLayout.addWidget(self.newgroup_name_linedit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.newgroup_create_button = QtGui.QPushButton(newgroup)
        self.newgroup_create_button.setObjectName("newgroup_create_button")
        self.horizontalLayout_2.addWidget(self.newgroup_create_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(newgroup)
        QtCore.QMetaObject.connectSlotsByName(newgroup)

    def retranslateUi(self, newgroup):
        newgroup.setWindowTitle(QtGui.QApplication.translate("newgroup", "New Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("newgroup", "Name of the Group", None, QtGui.QApplication.UnicodeUTF8))
        self.newgroup_create_button.setText(QtGui.QApplication.translate("newgroup", "Create", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    newgroup = QtGui.QDialog()
    ui = Ui_newgroup()
    ui.setupUi(newgroup)
    newgroup.show()
    sys.exit(app.exec_())

