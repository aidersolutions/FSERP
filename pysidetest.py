# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Mar  9 19:16:08 2015
# by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget_2 = QtGui.QStackedWidget(self.centralWidget)
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.page_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tabWidget = QtGui.QTabWidget(self.page_3)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QtCore.QSize(724, 257))
        self.tabWidget.setAccessibleDescription("")
        self.tabWidget.setStyleSheet("#tabWidget QTabBar::tab:hover{\n"
                                     "background-color:rgb(35, 15, 255);\n"
                                     "border-bottom-left-radius:15px;\n"
                                     "width:50px;\n"
                                     "height:50px;\n"
                                     "}\n"
                                     "QWidget{\n"
                                     "background-color:rgb(170,0,0);\n"
                                     "}\n"
                                     "#tabWidget_2 QTabBar::tab:hover{\n"
                                     "background-color:white;\n"
                                     "border-bottom-left-radius:0;\n"
                                     "border-top-left-radius:15;\n"
                                     "width:50px;\n"
                                     "height:50px;\n"
                                     "}\n"
                                     "")
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        self.tabWidget_2.setStyleSheet("")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget = QtGui.QListWidget(self.tab_3)
        self.listWidget.setStyleSheet("background-color:yellow;")
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_3.addWidget(self.listWidget)
        self.pushButton = QtGui.QPushButton(self.tab_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.horizontalLayout_2.addWidget(self.tabWidget_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_4.addWidget(self.tabWidget)
        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.pushButton_2 = QtGui.QPushButton(self.page_4)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 110, 95, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.stackedWidget_2.addWidget(self.page_4)
        self.horizontalLayout.addWidget(self.stackedWidget_2)
        self.listWidget_2 = QtGui.QListWidget(self.centralWidget)
        self.listWidget_2.setSelectionRectVisible(False)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout.addWidget(self.listWidget_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 760, 29))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtGui.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action_New = QtGui.QAction(MainWindow)
        self.action_New.setObjectName("action_New")
        self.actionNotification = QtGui.QAction(MainWindow)
        self.actionNotification.setObjectName("actionNotification")
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.actionNotification)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.mainToolBar.addAction(self.actionNotification)

        self.retranslateUi(MainWindow)
        self.stackedWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(
            QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3),
                                    QtGui.QApplication.translate("MainWindow", "Tab 1", None,
                                                                 QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4),
                                    QtGui.QApplication.translate("MainWindow", "Tab 2", None,
                                                                 QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  QtGui.QApplication.translate("MainWindow", "Tab 1", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QtGui.QApplication.translate("MainWindow", "Tab 2", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(
            QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(
            QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setText(
            QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNotification.setText(
            QtGui.QApplication.translate("MainWindow", "notification", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

