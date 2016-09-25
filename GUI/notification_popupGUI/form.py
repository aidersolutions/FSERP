# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Fri Jul 24 19:24:51 2015
# by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(328, 552)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtGui.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 308, 532))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.notificationTop = QtGui.QVBoxLayout()
        self.notificationTop.setObjectName("notificationTop")
        self.verticalLayout.addLayout(self.notificationTop)
        self.line = QtGui.QFrame(self.scrollAreaWidgetContents_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label2 = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.label2.setObjectName("label2")
        self.verticalLayout.addWidget(self.label2)
        self.notificationBottom = QtGui.QVBoxLayout()
        self.notificationBottom.setObjectName("notificationBottom")
        self.verticalLayout.addLayout(self.notificationBottom)
        spacerItem = QtGui.QSpacerItem(20, 486, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form",
                                                        "<html><head/><body><p align=\"center\">"
                                                        "<span style=\" font-weight:600;\">"
                                                        "New Messages</span></p></body></html>",
                                                        None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Form",
                                                         "<html><head/><body><p align=\"center\">"
                                                         "<span style=\" font-weight:600;\">"
                                                         "To Do List</span></p></body></html>",
                                                         None, QtGui.QApplication.UnicodeUTF8))

    def part_two(self):  # layout does not work properly if inserted before
        self.show_all = QtGui.QPushButton(self.scrollAreaWidgetContents_2)
        self.verticalLayout.insertWidget(1, self.show_all)
        self.show_all.setText(QtGui.QApplication.translate(
            "Form", "Show All Notification", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

