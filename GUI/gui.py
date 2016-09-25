#! /usr/bin/env python

""" Main Gui file """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

import resources_rc
from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QSpacerItem, QSizePolicy, \
    QGridLayout, QLabel, QStyle, QStyleFactory, QStylePainter, QStyleOptionTabV3, QColor, QPalette, QMainWindow, \
    QStackedWidget, QFrame, QVBoxLayout, QMenuBar, QToolBar, QIcon, QAction, QPixmap, QStatusBar, QProgressDialog, \
    QScrollArea

from PySide.QtCore import Qt, QObject, QEvent, QSize, QRect, QMetaObject
from shortcutsettings.shortcut import NewShortcut
from admin.authandadmin import Admin
from GUI.notification import NotificationTab
import logging
import settings

logger = logging.getLogger(__name__)


class EventHandlerForTabBar(QObject):
    """set custom color for each tab in the ui"""
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Paint:
            obj.setStyle(QStyleFactory.create('Windows'))
            p = QStylePainter(obj)
            tab = QStyleOptionTabV3()
            # selected = obj.currentIndex()
            for idx in range(obj.count()):
                obj.initStyleOption(tab, idx)
                if idx == 0:
                    bg_color = QColor('#ADEBFF')
                    fg_color = QColor('black')
                elif idx == 1:
                    bg_color = QColor('#6CBED2')
                    fg_color = QColor('black')
                elif idx == 2:
                    bg_color = QColor('#0099CC')
                    fg_color = QColor('black')
                elif idx == 3:
                    bg_color = QColor('#297ACC')
                    fg_color = QColor('black')
                elif idx == 4:
                    bg_color = QColor('#006BB2')
                    fg_color = QColor('black')
                elif idx == 5:
                    bg_color = QColor('#003D7A')
                    fg_color = QColor('black')
                tab.palette.setColor(QPalette.Window, bg_color)
                tab.palette.setColor(QPalette.WindowText, fg_color)
                p.drawControl(QStyle.CE_TabBarTab, tab)
            return True
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)


class Gui():
    """main gui class"""
    def __init__(self):
        self.mainwindow = QMainWindow()
        settings.get_settings()
        self.access = tuple(settings.access.items())
        self.progress = QProgressDialog("Setting up modules...", "cancel", 0, 7, self.mainwindow)
        self.progress.setWindowTitle(
            QApplication.translate("MainWindow", str(settings.company), None, QApplication.UnicodeUTF8))

    def setup(self):
        """initializes the uio of the erp client"""
        self.progress.setFixedWidth(1000)
        self.progress.setCancelButton(None)
        # self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setValue(1)
        self.mainwindow.setObjectName("MainWindow")
        self.mainwindow.resize(832, 668)
        self.mainwindow.setStyleSheet("QToolBar{\n"
                                      "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
                                      "stop:0 rgba(0,0,0),stop:1 rgb(162, 162, 162, 162));\n"
                                      "border: 0px;\n"
                                      "}\n"
                                      "QToolBar > QWidget{\n"
                                      "color:white;\n"
                                      "}\n"
                                      "QToolBar > QWidget:hover {\n"
                                      "background:transparent;\n"
                                      " }\n"
                                      "QToolBar > QWidget:checked {\n"
                                      "background:transparent;\n"
                                      " }\n"
                                      "#MainWindow{\n"
                                      "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
                                      "stop:0 rgba(0,0,0),stop:1 rgb(162, 162, 162, 162));\n"
                                      "border: 0px;\n"
                                      "}\n"
                                      "")
        self.centralWidget = QWidget(self.mainwindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QStackedWidget(self.centralWidget)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.shortcut = NewShortcut()
        scroll = QScrollArea()
        scroll.setWidget(self.shortcut.shortcut_setting)
        self.stackedWidget.addWidget(self.shortcut.shortcut_setting)
        self.home_page = QWidget()
        self.home_page.setObjectName("home_page")
        self.gridLayout = QGridLayout(self.home_page)
        self.gridLayout.setObjectName("gridLayout")
        self.billing_frame_2 = QFrame(self.home_page)
        self.billing_frame_2.setStyleSheet("background-image:url(:/images/billing_frame.png);\n"
                                           "background-repeat: no-repeat;\n"
                                           "background-position: center;\n"
                                           "background-color:#6CBED2;")
        self.billing_frame_2.setFrameShape(QFrame.StyledPanel)
        self.billing_frame_2.setFrameShadow(QFrame.Raised)
        self.billing_frame_2.setObjectName("billing_frame_2")
        self.verticalLayout_4 = QVBoxLayout(self.billing_frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QSpacerItem(20, 217, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.label_10 = QLabel(self.billing_frame_2)
        self.label_10.setStyleSheet("background:transparent;")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.gridLayout.addWidget(self.billing_frame_2, 0, 1, 1, 1)
        self.employee_frame_3 = QFrame(self.home_page)
        self.employee_frame_3.setStyleSheet("background-image:url(:/images/employee_frame.png);\n"
                                            "background-repeat: no-repeat;\n"
                                            "background-position: center;\n"
                                            "background-color:#0099CC;")
        self.employee_frame_3.setFrameShape(QFrame.StyledPanel)
        self.employee_frame_3.setFrameShadow(QFrame.Raised)
        self.employee_frame_3.setObjectName("employee_frame_3")
        self.verticalLayout_5 = QVBoxLayout(self.employee_frame_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem1 = QSpacerItem(20, 217, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.label_11 = QLabel(self.employee_frame_3)
        self.label_11.setStyleSheet("background:transparent;")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.gridLayout.addWidget(self.employee_frame_3, 0, 2, 1, 1)
        self.menu_frame_4 = QFrame(self.home_page)
        self.menu_frame_4.setStyleSheet("background-image:url(:/images/menu_frame.png);\n"
                                        "background-repeat: no-repeat;\n"
                                        "background-position: center;\n"
                                        "background-color:#297ACC;")
        self.menu_frame_4.setFrameShape(QFrame.StyledPanel)
        self.menu_frame_4.setFrameShadow(QFrame.Raised)
        self.menu_frame_4.setObjectName("menu_frame_4")
        self.verticalLayout_3 = QVBoxLayout(self.menu_frame_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QSpacerItem(20, 216, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.label_12 = QLabel(self.menu_frame_4)
        self.label_12.setStyleSheet("background:transparent;")
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.gridLayout.addWidget(self.menu_frame_4, 1, 0, 1, 1)
        self.report_frame_5 = QFrame(self.home_page)
        self.report_frame_5.setStyleSheet("background-image:url(:/images/report_frame.png);\n"
                                          "background-repeat: no-repeat;\n"
                                          "background-position: center;\n"
                                          "background-color:#006BB2;")
        self.report_frame_5.setFrameShape(QFrame.StyledPanel)
        self.report_frame_5.setFrameShadow(QFrame.Raised)
        self.report_frame_5.setObjectName("report_frame_5")
        self.verticalLayout_6 = QVBoxLayout(self.report_frame_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem3 = QSpacerItem(20, 216, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.label_13 = QLabel(self.report_frame_5)
        self.label_13.setStyleSheet("background:transparent;")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_6.addWidget(self.label_13)
        self.gridLayout.addWidget(self.report_frame_5, 1, 1, 1, 1)
        self.waste_frame_6 = QFrame(self.home_page)
        self.waste_frame_6.setStyleSheet("background-image:url(:/images/waste_frame.png);\n"
                                         "background-repeat: no-repeat;\n"
                                         "background-position: center;\n"
                                         "background-color:#003D7A;")
        self.waste_frame_6.setFrameShape(QFrame.StyledPanel)
        self.waste_frame_6.setFrameShadow(QFrame.Raised)
        self.waste_frame_6.setObjectName("waste_frame_6")
        self.verticalLayout_7 = QVBoxLayout(self.waste_frame_6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem4 = QSpacerItem(20, 216, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem4)
        self.label_14 = QLabel(self.waste_frame_6)
        self.label_14.setStyleSheet("background:transparent;")
        self.label_14.setObjectName("label_14")
        self.verticalLayout_7.addWidget(self.label_14)
        self.gridLayout.addWidget(self.waste_frame_6, 1, 2, 1, 1)
        self.inventory_frame_1 = QFrame(self.home_page)
        self.inventory_frame_1.setStyleSheet("background-image:url(:/images/inventory_frame.png);\n"
                                             "background-repeat: no-repeat;\n"
                                             "background-position: center;\n"
                                             "background-color:#ADEBFF;")
        self.inventory_frame_1.setFrameShape(QFrame.StyledPanel)
        self.inventory_frame_1.setFrameShadow(QFrame.Raised)
        self.inventory_frame_1.setObjectName("inventory_frame_1")
        self.verticalLayout_2 = QVBoxLayout(self.inventory_frame_1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem5 = QSpacerItem(20, 217, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.label_9 = QLabel(self.inventory_frame_1)
        self.label_9.setStyleSheet("background:transparent;")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.gridLayout.addWidget(self.inventory_frame_1, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.home_page)
        self.detail_page = QWidget()
        self.detail_page.setObjectName("detail_page")
        self.horizontalLayout_2 = QHBoxLayout(self.detail_page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_tabWidget = QTabWidget(self.detail_page)
        self.main_tabWidget.setAutoFillBackground(False)
        self.main_tabWidget.setStyleSheet("")
        self.main_tabWidget.setTabPosition(QTabWidget.West)
        self.main_tabWidget.setIconSize(QSize(60, 60))
        self.main_tabWidget.setElideMode(Qt.ElideNone)
        self.main_tabWidget.setObjectName("main_tabWidget")
        ##initializes the tabs
        self.add_tabs()
        self.main_tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.main_tabWidget.focusInEvent = self.change_focus
        self.main_tabWidget.currentChanged.connect(self.change_focus)
        self.stackedWidget.currentChanged.connect(self.change_focus)
        ######
        self.horizontalLayout_2.addWidget(self.main_tabWidget)
        self.stackedWidget.addWidget(self.detail_page)
        if ('Admin', True) in self.access:
            self.stackedWidget.addWidget(Admin(self.mainwindow))
        notification = NotificationTab()
        tab = notification.notificationTab_tab_4
        tab.custom_class_object = notification  # class_object is used to access the api through the
        self.stackedWidget.addWidget(tab)
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.mainwindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(self.mainwindow)
        self.menuBar.setGeometry(QRect(0, 0, 832, 29))
        self.menuBar.setObjectName("menuBar")
        self.mainwindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(self.mainwindow)
        self.mainToolBar.setLayoutDirection(Qt.RightToLeft)
        self.mainToolBar.setStyleSheet("")
        self.mainToolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainwindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(self.mainwindow)
        self.statusBar.setObjectName("statusBar")
        self.mainwindow.setStatusBar(self.statusBar)
        self.toolBar = QToolBar(self.mainwindow)
        self.toolBar.setLayoutDirection(Qt.RightToLeft)
        self.toolBar.setStyleSheet("")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        self.mainwindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.actionNotification = QAction(self.mainwindow)
        self.actionNotification.setCheckable(True)
        self.actionNotification.setChecked(False)
        self.actionNotification.setEnabled(True)
        icon6 = QIcon()
        icon6.addPixmap(QPixmap(":/images/notification.png"), QIcon.Normal, QIcon.Off)
        self.actionNotification.setIcon(icon6)
        self.actionNotification.setAutoRepeat(True)
        self.actionNotification.setVisible(True)
        self.actionNotification.setIconVisibleInMenu(False)
        self.actionNotification.setObjectName("actionNotification")
        self.actionNotification
        self.actionAdmin = QAction(self.mainwindow)
        # self.actionAdmin.setCheckable(True)
        icon7 = QIcon()
        icon7.addPixmap(QPixmap(":/images/admin.png"), QIcon.Normal, QIcon.Off)
        self.actionAdmin.setIcon(icon7)
        self.actionAdmin.setObjectName("actionAdmin")
        self.actionRefresh = QAction(self.mainwindow)
        icon8 = QIcon()
        icon8.addPixmap(QPixmap(":/images/refresh.png"), QIcon.Normal, QIcon.Off)
        self.actionRefresh.setIcon(icon8)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionHome = QAction(self.mainwindow)
        # self.actionHome.setCheckable(True)
        icon9 = QIcon()
        icon9.addPixmap(QPixmap(":/images/home.png"), QIcon.Normal, QIcon.Off)
        self.actionHome.setIcon(icon9)
        self.actionHome.setObjectName("actionHome")
        self.actionSettings = QAction(self.mainwindow)
        icon10 = QIcon()
        icon10.addPixmap(QPixmap(":/images/settings.png"), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon10)
        self.actionSettings.setObjectName("actionRefresh")
        self.toolBar.addAction(self.actionNotification)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdmin)
        if ('Admin', True) in self.access:
            self.toolBar.addSeparator()
        else:
            self.actionAdmin.setVisible(False)
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        ##retranslates
        self.mainwindow.setWindowTitle(
            QApplication.translate("MainWindow", settings.company, None, QApplication.UnicodeUTF8))
        self.label_10.setText(QApplication.translate
                              ("MainWindow", "<html><head/><body><p align=\"center\">BILLING</p></body></html>", None,
                               QApplication.UnicodeUTF8))
        self.label_11.setText(QApplication.translate
                              ("MainWindow", "<html><head/><body><p align=\"center\">EMPLOYEE</p></body></html>", None,
                               QApplication.UnicodeUTF8))
        self.label_12.setText(QApplication.translate
                              ("MainWindow", "<html><head/><body><p align=\"center\">MENU</p></body></html>", None,
                               QApplication.UnicodeUTF8))
        self.label_13.setText(QApplication.translate
                              ("MainWindow", "<html><head/><body><p align=\"center\">REPORT</p></body></html>", None,
                               QApplication.UnicodeUTF8))
        self.label_14.setText(QApplication.translate
                              ("MainWindow", "<html><head/><body><p align=\"center\">WASTE</p></body></html>", None,
                               QApplication.UnicodeUTF8))
        self.label_9.setText(QApplication.translate
                             ("MainWindow", "<html><head/><body><p align=\"center\">INVENTORY</p></body></html>", None,
                              QApplication.UnicodeUTF8))
        self.inventory_frame_1.setToolTip(
            QApplication.translate("MainWindow", "Go to the Inventory Tab", None, QApplication.UnicodeUTF8))
        self.billing_frame_2.setToolTip(
            QApplication.translate("MainWindow", "Go to the Billing Tab", None, QApplication.UnicodeUTF8))
        self.employee_frame_3.setToolTip(
            QApplication.translate("MainWindow", "Go to the Employee Tab", None, QApplication.UnicodeUTF8))
        self.menu_frame_4.setToolTip(
            QApplication.translate("MainWindow", "Go to the Menu Tab", None, QApplication.UnicodeUTF8))
        self.report_frame_5.setToolTip(
            QApplication.translate("MainWindow", "Go to the Report Tab", None, QApplication.UnicodeUTF8))
        self.waste_frame_6.setToolTip(
            QApplication.translate("MainWindow", "Go to the Waste Tab", None, QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(
            QApplication.translate("MainWindow", "toolBar", None, QApplication.UnicodeUTF8))
        self.actionNotification.setText("&&Notification")
        # QApplication.translate("MainWindow", "&Notification", None, QApplication.UnicodeUTF8))
        self.actionNotification.setToolTip(
            QApplication.translate("MainWindow", "Click to see new notifications", None,
                                   QApplication.UnicodeUTF8))
        # self.actionNotification.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+Shift+N", None, QApplication.UnicodeUTF8))
        self.actionAdmin.setText('&&Admin')
        # QApplication.translate("MainWindow", "Admin", None, QApplication.UnicodeUTF8))
        self.actionAdmin.setToolTip(QApplication.translate("MainWindow", "Click to go to admin interface", None,
                                                           QApplication.UnicodeUTF8))
        # self.actionAdmin.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+Shift+A", None, QApplication.UnicodeUTF8))
        self.actionRefresh.setText("&&Refresh")
        # QApplication.translate("MainWindow", "Refresh", None, QApplication.UnicodeUTF8))
        self.actionRefresh.setToolTip(
            QApplication.translate("MainWindow", "refreshes the data from the server", None,
                                   QApplication.UnicodeUTF8))
        # self.actionRefresh.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+Shift+R", None, QApplication.UnicodeUTF8))
        self.actionHome.setText('&&Home')
        # QApplication.translate("MainWindow", "Home", None, QApplication.UnicodeUTF8))
        self.actionHome.setToolTip(
            QApplication.translate("MainWindow", "Go back to the home screen", None,
                                   QApplication.UnicodeUTF8))
        self.actionSettings.setText('&&Settings')
        # QApplication.translate("MainWindow", "Settings", None, QApplication.UnicodeUTF8))
        self.actionSettings.setToolTip(
            QApplication.translate("MainWindow", "Go to the settings panel", None,
                                   QApplication.UnicodeUTF8))
        # self.actionHome.setShortcut(
        #     QApplication.translate("MainWindow", "Ctrl+Shift+H", None, QApplication.UnicodeUTF8))
        self.stackedWidget.setCurrentIndex(1)
        self.main_tabWidget.setCurrentIndex(0)

        self.ob = self.main_tabWidget.tabBar()
        # self.add_tool_tip(self.ob) todo avoided due to segmentation fault error, left for future fixes
        self.tb = EventHandlerForTabBar()
        self.ob.installEventFilter(self.tb)

        QMetaObject.connectSlotsByName(self.mainwindow)

    def add_tabs(self):
        """
        adds new tabs
        """
        global logger
        if ('Inventory', True) in self.access:
            logger.info('initiating Inventory')
            icon = QIcon()
            icon.addPixmap(QPixmap(":/images/inventory.png"), QIcon.Normal, QIcon.Off)
            from inventory.inventory import Inventory

            inventory = Inventory()
            # inventory.inventory_tab_1.setToolTip("Inventory Section")
            self.main_tabWidget.addTab(inventory.inventory_tab_1, icon, "")
            inventory.inventory_detail_tabWidget.setCurrentIndex(0)
        else:
            self.inventory_frame_1.setVisible(False)
        self.progress.setLabelText('Inventory Done....')
        self.progress.setValue(2)

        if ('Billing', True) in self.access:
            logger.info('initiating Billing')
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/images/billing.png"), QIcon.Normal, QIcon.Off)
            from billing.billing import Billing

            bill = Billing()
            # bill.billing_tab_2.setToolTip("Billing Section")
            self.main_tabWidget.addTab(bill.billing_tab_2, icon1, "")
            bill.billing_detail_tabWidget.setCurrentIndex(0)
        else:
            self.billing_frame_2.setVisible(False)
        self.progress.setLabelText('Billing Done...')
        self.progress.setValue(3)

        if ('Employee', True) in self.access:
            logger.info('initiating Employee')
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/images/employee.png"), QIcon.Normal, QIcon.Off)
            from employee.employee import Employee

            employee = Employee()
            # employee.employee_tab_3.setToolTip("Employee Section")
            self.main_tabWidget.addTab(employee.employee_tab_3, icon2, "")
            employee.employee_detail_tabWidget.setCurrentIndex(0)
        else:
            self.employee_frame_3.setVisible(False)
        self.progress.setLabelText('Employee Done...')
        self.progress.setValue(4)

        if ('Menu', True) in self.access:
            logger.info('initiating Menu')
            icon3 = QIcon()
            icon3.addPixmap(QPixmap(":/images/menu.png"), QIcon.Normal, QIcon.Off)
            from menu.menu import Menu

            menu = Menu()
            # menu.menu_tab_4.setToolTip("Menu Section")
            self.main_tabWidget.addTab(menu.menu_tab_4, icon3, "")
            menu.menu_detail_tabWidget.setCurrentIndex(0)
        else:
            self.menu_frame_4.setVisible(False)
        self.progress.setLabelText('Menu Done....')
        self.progress.setValue(5)

        if ('Report', True) in self.access:
            logger.info('initiating Report')
            icon4 = QIcon()
            icon4.addPixmap(QPixmap(":/images/report.png"), QIcon.Normal, QIcon.Off)
            from report.report import Report

            report = Report()
            # report.report_tab_5.setToolTip("Report Section")
            self.main_tabWidget.addTab(report.report_tab_5, icon4, "")
            report.report_detail_tabWidget.setCurrentIndex(0)
        else:
            self.report_frame_5.setVisible(False)
        self.progress.setLabelText('Report Done....')
        self.progress.setValue(6)

        if ('Waste', True) in self.access:
            logger.info('initiating Waste')
            icon5 = QIcon()
            icon5.addPixmap(QPixmap(":/images/waste.png"), QIcon.Normal, QIcon.Off)
            from waste.waste import Waste

            waste = Waste()
            # waste.waste_tab_6.setToolTip("Waste Section")
            self.main_tabWidget.addTab(waste.waste_tab_6, icon5, "")
            waste.waste_detail_tabWidget.setCurrentIndex(0)
        else:
            self.waste_frame_6.setVisible(False)
        self.progress.setLabelText('Waste Done....')
        self.progress.setValue(7)

    def change_focus(self, event=None):
        """
        focus method to set focus to a tab to initialize the corresponding events of the tab
        """
        wid = self.main_tabWidget.currentWidget()
        if wid:
            if wid.isVisible():
                # print wid.objectName()
                # print '1y'
                wid.setFocus()

    def add_tool_tip(self, ob):  # todo not working causing segmentation fault, avoided calling this function
        """
        method to add tool tip to the tabs
        :param ob: Tab bar
        """
        obj = ob
        count = obj.count()
        hardcode = {0: 'Inventory Section', 1: "Billing Section", 2: "Employee Section", 3: "Menu Section",
                    4: "Report Section", 5: "Waste Section"}
        for i in range(count):
            obj.setTabToolTip(i, hardcode[i])
