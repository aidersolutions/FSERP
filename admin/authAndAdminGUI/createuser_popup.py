# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createuser_popup.ui'
#
# Created: Tue Jun 30 10:27:43 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_newuser(object):
    def setupUi(self, newuser):
        newuser.setObjectName("newuser")
        newuser.resize(242, 160)
        self.formLayout = QtGui.QFormLayout(newuser)
        self.formLayout.setObjectName("formLayout")
        self.label_16 = QtGui.QLabel(newuser)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_16)
        self.newuser_name_linedit = QtGui.QLineEdit(newuser)
        self.newuser_name_linedit.setReadOnly(False)
        self.newuser_name_linedit.setObjectName("newuser_name_linedit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.newuser_name_linedit)
        self.label_12 = QtGui.QLabel(newuser)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_12)
        self.newuser_username_linedit = QtGui.QLineEdit(newuser)
        self.newuser_username_linedit.setObjectName("newuser_username_linedit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.newuser_username_linedit)
        self.label_13 = QtGui.QLabel(newuser)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_13)
        self.newuser_password_linedit = QtGui.QLineEdit(newuser)
        self.newuser_password_linedit.setEchoMode(QtGui.QLineEdit.Password)
        self.newuser_password_linedit.setObjectName("newuser_password_linedit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.newuser_password_linedit)
        self.newuser_save_button = QtGui.QPushButton(newuser)
        self.newuser_save_button.setObjectName("newuser_save_button")
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.newuser_save_button)

        self.retranslateUi(newuser)
        QtCore.QMetaObject.connectSlotsByName(newuser)

    def retranslateUi(self, newuser):
        newuser.setWindowTitle(QtGui.QApplication.translate("newuser", "Create User", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("newuser", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("newuser", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("newuser", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.newuser_save_button.setText(QtGui.QApplication.translate("newuser", "Save", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    newuser = QtGui.QDialog()
    ui = Ui_newuser()
    ui.setupUi(newuser)
    newuser.show()
    sys.exit(app.exec_())

