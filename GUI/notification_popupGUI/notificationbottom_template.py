# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notificationbottom_template.ui'
#
# Created: Fri Jul 24 19:44:01 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_notificationbottom_template(object):
    def setupUi(self, notificationbottom_template):
        notificationbottom_template.setObjectName("notificationbottom_template")
        notificationbottom_template.resize(284, 112)
        self.horizontalLayout = QtGui.QHBoxLayout(notificationbottom_template)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.todo_checkbox = QtGui.QCheckBox(notificationbottom_template)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.todo_checkbox.setFont(font)
        self.todo_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.todo_checkbox.setStyleSheet("QCheckBox::indicator{\n"
"width:40px;\n"
"height:40px;\n"
"subcontrol-position: top left;\n"
"}")
        self.todo_checkbox.setText("")
        self.todo_checkbox.setObjectName("todo_checkbox")
        self.verticalLayout.addWidget(self.todo_checkbox)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.todo_label = QtGui.QLabel(notificationbottom_template)
        self.todo_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.todo_label.setObjectName("todo_label")
        self.horizontalLayout.addWidget(self.todo_label)
        spacerItem2 = QtGui.QSpacerItem(136, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)

        self.retranslateUi(notificationbottom_template)
        QtCore.QMetaObject.connectSlotsByName(notificationbottom_template)

    def retranslateUi(self, notificationbottom_template):
        notificationbottom_template.setWindowTitle(QtGui.QApplication.translate("notificationbottom_template", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.todo_label.setText(QtGui.QApplication.translate("notificationbottom_template", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    notificationbottom_template = QtGui.QWidget()
    ui = Ui_notificationbottom_template()
    ui.setupUi(notificationbottom_template)
    notificationbottom_template.show()
    sys.exit(app.exec_())

