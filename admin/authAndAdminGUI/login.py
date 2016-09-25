# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Tue May 12 20:11:44 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(287, 171)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.loginpopup_error_label = QtGui.QLabel(Dialog)
        self.loginpopup_error_label.setStyleSheet("color:red;")
        self.loginpopup_error_label.setText("")
        self.loginpopup_error_label.setObjectName("loginpopup_error_label")
        self.verticalLayout.addWidget(self.loginpopup_error_label)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.loginpopup_usename_linedit = QtGui.QLineEdit(Dialog)
        self.loginpopup_usename_linedit.setObjectName("loginpopup_usename_linedit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.loginpopup_usename_linedit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.loginpopup_password_linedit = QtGui.QLineEdit(Dialog)
        self.loginpopup_password_linedit.setEchoMode(QtGui.QLineEdit.Password)
        self.loginpopup_password_linedit.setObjectName("loginpopup_password_linedit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.loginpopup_password_linedit)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginpopup_reset_button = QtGui.QPushButton(Dialog)
        self.loginpopup_reset_button.setObjectName("loginpopup_reset_button")
        self.horizontalLayout.addWidget(self.loginpopup_reset_button)
        self.loginpopup_login_button = QtGui.QPushButton(Dialog)
        self.loginpopup_login_button.setObjectName("loginpopup_login_button")
        self.horizontalLayout.addWidget(self.loginpopup_login_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.loginpopup_usename_linedit, self.loginpopup_password_linedit)
        Dialog.setTabOrder(self.loginpopup_password_linedit, self.loginpopup_login_button)
        Dialog.setTabOrder(self.loginpopup_login_button, self.loginpopup_reset_button)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.loginpopup_reset_button.setText(QtGui.QApplication.translate("Dialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.loginpopup_login_button.setText(QtGui.QApplication.translate("Dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

