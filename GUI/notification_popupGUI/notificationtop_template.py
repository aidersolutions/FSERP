# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notificationtop_template.ui'
#
# Created: Mon Mar 23 15:28:23 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_notificationtop_template(object):
    def setupUi(self, notificationtop_template):
        notificationtop_template.setObjectName("notificationtop_template")
        notificationtop_template.resize(287, 108)
        font = QtGui.QFont()
        font.setPointSize(10)
        notificationtop_template.setFont(font)
        self.gridLayout_2 = QtGui.QGridLayout(notificationtop_template)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.notificationtop_done_button = QtGui.QPushButton(notificationtop_template)
        self.notificationtop_done_button.setObjectName("notificationtop_done_button")
        self.horizontalLayout.addWidget(self.notificationtop_done_button)
        self.notificationtop_todo_button = QtGui.QPushButton(notificationtop_template)
        self.notificationtop_todo_button.setObjectName("notificationtop_todo_button")
        self.horizontalLayout.addWidget(self.notificationtop_todo_button)
        self.notificationtop_later_button = QtGui.QPushButton(notificationtop_template)
        self.notificationtop_later_button.setStyleSheet("")
        self.notificationtop_later_button.setObjectName("notificationtop_later_button")
        self.horizontalLayout.addWidget(self.notificationtop_later_button)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(notificationtop_template)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.notificationtop_image_frame = QtGui.QFrame(notificationtop_template)
        self.notificationtop_image_frame.setStyleSheet("border-image:url(:/images/region.png);")
        self.notificationtop_image_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.notificationtop_image_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.notificationtop_image_frame.setObjectName("notificationtop_image_frame")
        self.gridLayout.addWidget(self.notificationtop_image_frame, 0, 0, 2, 1)
        self.notificationtop_message_label = QtGui.QLabel(notificationtop_template)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.notificationtop_message_label.setFont(font)
        self.notificationtop_message_label.setWordWrap(False)
        self.notificationtop_message_label.setObjectName("notificationtop_message_label")
        self.gridLayout.addWidget(self.notificationtop_message_label, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(notificationtop_template)
        QtCore.QMetaObject.connectSlotsByName(notificationtop_template)

    def retranslateUi(self, notificationtop_template):
        notificationtop_template.setWindowTitle(QtGui.QApplication.translate("notificationtop_template", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationtop_done_button.setText(QtGui.QApplication.translate("notificationtop_template", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationtop_todo_button.setText(QtGui.QApplication.translate("notificationtop_template", "To Do", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationtop_later_button.setText(QtGui.QApplication.translate("notificationtop_template", "Later", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("notificationtop_template", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Regional Officer</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationtop_message_label.setText(QtGui.QApplication.translate("notificationtop_template", "text", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
