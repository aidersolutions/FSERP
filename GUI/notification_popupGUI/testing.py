# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testing.ui'
#
# Created: Fri Mar 20 19:41:16 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(529, 240)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.listView = QtGui.QListView(Dialog)
        self.listView.setObjectName("listView")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.listView)
        self.listView_2 = QtGui.QListView(Dialog)
        self.listView_2.setObjectName("listView_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.listView_2)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.pushButton_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

