#! /usr/bin/env python

""" Food Safety Restaurant ERP """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

# Standard Libraries
import os
import sys
import logging
from GUI import settings

settings.get_settings()

logformat = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
datefmt = '%a %b %d %H:%M:%S %Y'
logging.basicConfig(filename="fserp.log", level=settings.level, format=logformat, datefmt=datefmt)
logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())

# PySide
from PySide.QtGui import QApplication, QShortcut, QKeySequence

# Tryton related imports
import FSERP
import trytond
from trytond.config import config, parse_listen
from proteus import config as con

import config_fserp

conf = con.set_trytond('testdbkitchen', user='admin',
                       config_file=os.path.join(os.getcwd(), 'FSERP', 'trytond', 'etc', 'trytond.conf'))

config.update_etc(config_fserp.TRYTON_CONFIG_FILE)


# local module imports 
from GUI.notification import Notification
from admin.authandadmin import Login, Admin  ##call this to check the authenticity of the user
from GUI.gui import Gui


class MainWindow():
    """
       The main application
    """

    def __init__(self):
        logger.info("inside constructor...")
        self.login = Login()
        self.login.exec_()
        self.mainwindow = Gui()

    def setup(self):
        """setup for the main application"""
        self.mainwindow.setup()
        # self.login = Login(self.mainwindow.mainwindow)
        # self.login.exec_()
        self.mainwindow.centralWidget.setAutoFillBackground(True)
        # self.mainwindow.centralWidget.setStyleSheet("background:transparent;")
        self.mainwindow.main_tabWidget.setAutoFillBackground(True)
        # self.mainwindow.inventory_tab_1.setAttribute(Qt.WA_StyledBackground, True)
        # self.set_background_for_eachtab()
        self.notification = Notification(self.mainwindow.mainwindow)
        self.notification.setVisible(False)
        self.mainwindow.actionNotification.toggled.connect(lambda: self.notification.setVisible(
            False) if self.notification.isVisible() else self.notification.setVisible(True))
        self.mainwindow.actionHome.triggered.connect(lambda: self.mainwindow.stackedWidget.setCurrentIndex(1))
        self.set_shortcuts()
        self.mainwindow.shortcut.key_apply_button.clicked.connect(self.get_shortcuts)
        self.mainwindow.shortcut.key_resetdefault_button.clicked.connect(self.set_default)
        # self.localstylesheet = "GUI/staticfiles/styles.qss"
        # self.inlinestylesheet = "GUI/staticfiles/inline.qss"
        # with open(self.inlinestylesheet, 'r') as fh:
        # self.mainwindow.main_tabWidget.setStyleSheet(fh.read())
        # with open(self.localstylesheet, 'r') as fp:
        # self.mainwindow.main_tabWidget.setStyleSheet(fp.read())
        # self.mainwindow.inventory_tab_1.setAutoFillBackground(True)
        # plt = QPalette()
        # plt.setColor(QPalette.Active, QPalette.Background, QColor('#ADEBFF'))
        # plt.setColor(QPalette.Inactive, QPalette.Background, QColor('#ADEBFF'))
        # plt.setColor(QPalette.Disabled, QPalette.Background, QColor('#ADEBFF'))
        # self.mainwindow.inventory_tab_1.setPalette(plt)
        self.mainwindow.actionAdmin.triggered.connect(lambda: self.go_to_admin())
        self.mainwindow.actionSettings.triggered.connect(self.goto_settings)
        logger.info("executed the login dialog now going to add mouseReleaseEvents")
        self.mainwindow.inventory_frame_1.mouseReleaseEvent = lambda event, who=0: self.goto_widget(event, who)
        self.mainwindow.billing_frame_2.mouseReleaseEvent = lambda event, who=1: self.goto_widget(event, who)
        self.mainwindow.employee_frame_3.mouseReleaseEvent = lambda event, who=2: self.goto_widget(event, who)
        self.mainwindow.menu_frame_4.mouseReleaseEvent = lambda event, who=3: self.goto_widget(event, who)
        self.mainwindow.report_frame_5.mouseReleaseEvent = lambda event, who=4: self.goto_widget(event, who)
        self.mainwindow.waste_frame_6.mouseReleaseEvent = lambda event, who=5: self.goto_widget(event, who)
        self.assign_shortcuts()

    def set_default(self):
        """sets the defaults shortcut"""
        for i, j in settings.default_shortcut.items():
            try:
                key = getattr(self.mainwindow.shortcut, i)
                key.setText(j)

            except AttributeError as e:
                print e

    def set_shortcuts(self):
        """sets the shortcut"""
        for i, j in settings.custom_shortcut.items():
            try:
                key = getattr(self.mainwindow.shortcut, i)
                key.setText(j)

            except AttributeError as e:
                print e

    def get_shortcuts(self):
        """get the shortcuts"""
        for i in settings.default_shortcut.keys():
            try:
                key = getattr(self.mainwindow.shortcut, i)
                settings.custom_shortcut[key.objectName()] = key.text()
            except AttributeError as e:
                print e
        settings.set_settings()


    def assign_shortcuts(self):
        """assigns the shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_inventory']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 0))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_billing']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 1))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_menu']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 3))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_employee']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 2))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_report']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 4))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabs_waste']),
                  self.mainwindow.mainwindow, lambda: self.goto_widget('event', 5))

    def verify_login(self):
        """verify the login credentials"""
        if not self.login.valid:
            self.mainwindow.mainwindow.setDisabled(True)
            logger.critical("invalid login access")
            return False
        else:
            return True

    def go_to_admin(self):
        """
        Goes back to the home screen
        :return:none
        """
        logger.info("going to home screen")
        admin = self.mainwindow.stackedWidget.widget(3)
        with admin.authenticate() as state:
            if state:
                self.mainwindow.stackedWidget.setCurrentIndex(3)

    def goto_settings(self):
        """
        Goes back to the home screen
        :return:none
        """
        logger.info("going to home screen")
        self.mainwindow.stackedWidget.setCurrentIndex(0)

    def goto_widget(self, event, who):
        """
        :param who:the tab widget index
        :return:transition to the required widget
        """
        self.mainwindow.stackedWidget.setCurrentIndex(2)
        self.mainwindow.main_tabWidget.setCurrentIndex(who)
        # self.set_background_for_eachtab()
        # self.mainwindow.inventory_tab_1.setAttribute(Qt.WA_StyledBackground,True)

    def resize_event(self, event):
        """handles the resize event to update the posistion"""
        self.notification.updatePosition()


if __name__ == "__main__":
    logger.info("Starting the app...")
    app = QApplication(sys.argv)
    logger.info("created the app...")
    localstylesheet = "GUI/staticfiles/styles.qss"
    with open(localstylesheet, 'r') as fp:
        app.setStyleSheet(fp.read())
    win = MainWindow()
    state = win.verify_login()
    if state:
        win.setup()
        logger.info("created the main window")
        # win.verify_login()
        win.mainwindow.mainwindow.show()
        logger.info("showing the mainwindow")
        app.exec_()
    logger.info("closing the app..")
    sys.exit(0)
