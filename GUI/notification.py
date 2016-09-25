#! /usr/bin/env python

""" Notification Module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from notification_popupGUI.form import Ui_Form
from PySide.QtGui import QWidget, QGridLayout, QHBoxLayout, QLabel, QDateEdit, QComboBox, QTableWidget, QPushButton, \
    QTableWidgetItem, QSizePolicy, QSpacerItem, QApplication, QAbstractItemView, QKeySequence, QCheckBox, \
    QDoubleValidator, QMessageBox, QPrintDialog, QDialog, QLineEdit, QShortcut, QTextEdit, QHeaderView, QVBoxLayout
from PySide.QtCore import QDate, Qt, Signal
from notification_popupGUI.notificationtop_template import Ui_notificationtop_template
from notification_popupGUI.notificationbottom_template import Ui_notificationbottom_template
from datetime import datetime, timedelta
from GUI.notification_tryton import Messaging
from collections import defaultdict
import json
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class Notification(QWidget):
    """the notification panel class"""
    def __init__(self, parent=None):
        super(Notification, self).__init__(parent)
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.paddingLeft = 0
        self.paddingBottom = 25
        # op=QGraphicsOpacityEffect(self)
        # op.setOpacity(1.00)
        # self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)
        self.topnotification_object_count = 0
        self.bottomnotification_object_count = 0
        self.new_topnotification_object = {}
        self.new_bottomnotification_object = {}
        self.add_new_topnotification()
        widgets = QApplication.topLevelWidgets()
        mainwindow, = [i for i in widgets if type(i).__name__ == 'QMainWindow']
        windows = {type(i).__name__: i for i in mainwindow.centralWidget().children()}
        self.stack = windows['QStackedWidget']
        self.form.part_two()
        self.form.show_all.clicked.connect(self.goto_notifications)
        # self.add_new_topnotification()
        # self.setStyleSheet("background-color:#ADEBFF;")

    def setParent(self, parent):
        """method to set parent widget of the notofication ui widget"""
        self.updatePosition()
        return super(Notification, self).setParent(parent)

    def updatePosition(self):
        """method to update the postion of the notification panel in resize cases"""
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()

        if not parentRect:
            return
        x = parentRect.width() - self.width() - self.paddingLeft
        y = parentRect.height() - self.height() - self.paddingBottom
        self.setGeometry(x, y, self.width(), parentRect.height() - 62)

    def resizeEvent(self, event):
        """method override to handle resize cases to update the position"""
        super(Notification, self).resizeEvent(event)
        self.updatePosition()

    def showEvent(self, event):
        """method overide to capture show event to update the position of the panel"""
        self.updatePosition()
        return super(Notification, self).showEvent(event)

    def add_new_topnotification(self):
        """addds the top notification section, where new notification arrives"""
        try:
            data = json.loads(open('message_json.json', 'r').read())
            for i in data['messages']:
                self.topnotification_object_count += 1
                ob = NotificationTemplate(self)
                self.new_topnotification_object[i['message id']] = ob
                ob.new_notification(i)
                # ob.toptemplate.notificationtop_done_button.clicked.connect(
                # lambda who=self.topnotification_object_count: self.remove_topnotification(who))
                # ob.toptemplate.notificationtop_todo_button.clicked.connect(
                # lambda who=self.topnotification_object_count: self.new_bottomchecknotification(who))
                # ob.toptemplate.notificationtop_later_button.clicked.connect(
                # lambda who=self.topnotification_object_count: self.notify_later(who))
                ob.custom_signal.connect(self.notify_later)
                self.form.notificationTop.addWidget(ob)
        except (OSError, IOError):
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def remove_topnotification(self, id):
        """ removes top notification on a subseuent acction"""
        self.new_topnotification_object[id].hide()
        del self.new_topnotification_object[id]
        self.topnotification_object_count -= 1

    def new_bottomchecknotification(self, id):
        """adds a new notification in the bottom based on the action of the top notification"""
        self.bottomnotification_object_count += 1
        ob = NotificationBottomTemplate(self)
        self.new_bottomnotification_object[self.bottomnotification_object_count] = ob
        top = self.new_topnotification_object[id]
        ob.new_notification(top.toptemplate.notificationtop_message_label.text())
        ob.bottomtemplate.todo_checkbox.stateChanged.connect(self.remove_bottomnotification)
        self.form.notificationBottom.addWidget(ob)
        self.remove_topnotification(id)

    def remove_bottomnotification(self, arg):
        """ removes the  boittom notification based on the subsequent action"""
        val = int
        for i, j in self.new_bottomnotification_object.iteritems():
            if j.bottomtemplate.todo_checkbox.checkState() == arg:
                val = i
        self.new_bottomnotification_object[val].setVisible(False)
        del self.new_bottomnotification_object[val]

    def notify_later(self, id):
        """method to set the notification to notify later section"""
        widget = self.stack.widget(4)
        self.stack.setCurrentIndex(4)
        widget.custom_class_object.load_single_message(id)
        self.remove_topnotification(id)
        self.setVisible(False)

    def goto_notifications(self):
        """method to open the notification details in the notification tabs"""
        self.stack.setCurrentIndex(4)
        self.setVisible(False)


class NotificationTopTemplate(QWidget): #unused, use NotificationTemplate
    """generl template class to create a new top notification"""
    def __init__(self, parent=None):
        super(NotificationTopTemplate, self).__init__(parent)
        self.toptemplate = Ui_notificationtop_template()
        self.toptemplate.setupUi(self)
        self.setStyleSheet('QWidget:hover {color:blue}')
        # self.setAutoFillBackground(True)

    # def enterEvent(self, event):
    # self.setStyleSheet('background-color:#ADEBFF;')
    # super(NotificationTopTemplate, self).enterEvent(event)
    #
    # def leaveEvent(self, event):
    # self.setStyleSheet('background-color:white;')
    # super(NotificationTopTemplate, self).leaveEvent(event)

    def new_notification(self, text):
        """creates a new notification"""
        s = ''
        s += 'From:{}\n'.format(text['from'][0])
        s += 'Designation:{}\n'.format(text['from'][1])
        s += 'Date:{}\n'.format(text['sent'])
        body = text['body'].replace('\n', '')
        for i, j in enumerate(body):
            if i % 31 == 0:
                s += '\n'
            s += j
        text = s
        self.toptemplate.notificationtop_message_label.setText(str(text))
        # self.toptemplate.notificationtop_image_frame.setAutoFillBackground(True)


class NotificationBottomTemplate(QWidget):
    """generl template class to create a new top notification"""
    def __init__(self, parent=None):
        super(NotificationBottomTemplate, self).__init__(parent)
        self.bottomtemplate = Ui_notificationbottom_template()
        self.bottomtemplate.setupUi(self)
        # self.setAutoFillBackground(True)

    def new_notification(self, text):
        """creates a new notification"""
        s = ''
        for i, j in enumerate(text):
            if i % 31 == 0:
                s += '\n'
            s += j
        text = s
        self.bottomtemplate.todo_label.setText(str(text))
        # self.toptemplate.notificationtop_image_frame.setAutoFillBackground(True)


class NotificationTab():
    """ui class for new notification tab"""
    global logger

    def __init__(self):
        #####
        logger.info('Inside PurchaseSchedule')
        self.notificationTab_tab_4 = QWidget()
        self.notificationTab_tab_4.setObjectName("notificationTab_tab_4")
        self.gridLayout_19 = QGridLayout(self.notificationTab_tab_4)
        self.gridLayout_19.setObjectName("gridLayout_19")
        ##
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_label = QLabel(self.notificationTab_tab_4)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout.addWidget(self.title_label)
        self.gridLayout_19.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        ##
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.id_label = QLabel(self.notificationTab_tab_4)
        self.id_label.setObjectName("id_label")
        self.horizontalLayout_6.addWidget(self.id_label)
        self.id_line = QLineEdit(self.notificationTab_tab_4)
        self.id_line.setObjectName("id_line")
        self.horizontalLayout_6.addWidget(self.id_line)
        self.notification_schedule_fromdate_label = QLabel(self.notificationTab_tab_4)
        self.notification_schedule_fromdate_label.setObjectName("notification_schedule_fromdate_label")
        self.horizontalLayout_6.addWidget(self.notification_schedule_fromdate_label)
        self.notification_schedule_fromdate_dateedit = QDateEdit(self.notificationTab_tab_4)
        self.notification_schedule_fromdate_dateedit.setMaximumDate(QDate.currentDate())
        self.notification_schedule_fromdate_dateedit.setDate(QDate.currentDate())
        self.notification_schedule_fromdate_dateedit.setCalendarPopup(True)
        self.notification_schedule_fromdate_dateedit.setObjectName("notification_schedule_fromdate_dateedit")
        self.horizontalLayout_6.addWidget(self.notification_schedule_fromdate_dateedit)
        self.notification_schedule_todate_label = QLabel(self.notificationTab_tab_4)
        self.notification_schedule_todate_label.setObjectName("notification_schedule_todate_label")
        self.horizontalLayout_6.addWidget(self.notification_schedule_todate_label)
        self.notification_schedule_todate_dateedit = QDateEdit(self.notificationTab_tab_4)
        self.notification_schedule_todate_dateedit.setMaximumDate(QDate.currentDate())
        self.notification_schedule_todate_dateedit.setDate(QDate.currentDate())
        self.notification_schedule_todate_dateedit.setCalendarPopup(True)
        self.notification_schedule_todate_dateedit.setObjectName("notification_schedule_todate_dateedit")
        self.horizontalLayout_6.addWidget(self.notification_schedule_todate_dateedit)
        self.type_label = QLabel(self.notificationTab_tab_4)
        self.type_label.setObjectName("type_label")
        self.horizontalLayout_6.addWidget(self.type_label)
        self.notification_states = QComboBox(self.notificationTab_tab_4)
        self.notification_states.setObjectName("notification_states")
        self.horizontalLayout_6.addWidget(self.notification_states)
        self.batch_label = QLabel(self.notificationTab_tab_4)
        self.batch_label.setObjectName("batch_label")
        self.horizontalLayout_6.addWidget(self.batch_label)
        self.notification_results = QComboBox(self.notificationTab_tab_4)
        self.notification_results.setObjectName("notification_results")
        self.horizontalLayout_6.addWidget(self.notification_results)
        self.gridLayout_19.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.notification_schedule_table = QTableWidget(self.notificationTab_tab_4)
        self.notification_schedule_table.setObjectName("notification_schedule_table")
        self.notification_schedule_table.setColumnCount(5)
        self.notification_schedule_table.setRowCount(0)
        self.notification_schedule_table.setWordWrap(True)
        item = QTableWidgetItem()
        self.notification_schedule_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.notification_schedule_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.notification_schedule_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.notification_schedule_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.notification_schedule_table.setHorizontalHeaderItem(4, item)
        self.notification_schedule_table.horizontalHeader().setCascadingSectionResizes(True)
        self.notification_schedule_table.horizontalHeader().setStretchLastSection(True)
        self.notification_schedule_table.verticalHeader().setVisible(False)
        self.notification_schedule_table.verticalHeader().setCascadingSectionResizes(True)
        self.notification_schedule_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_8.addWidget(self.notification_schedule_table, 0, 0, 1, 5)
        self.notification_search_button = QPushButton(self.notificationTab_tab_4)
        self.notification_search_button.setObjectName("notification_search_button")
        self.gridLayout_8.addWidget(self.notification_search_button, 1, 0, 1, 1)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem10, 1, 2, 1, 1)
        self.notification_reset_button = QPushButton(self.notificationTab_tab_4)
        self.notification_reset_button.setObjectName("notification_reset_button")
        self.gridLayout_8.addWidget(self.notification_reset_button, 1, 3, 1, 1)
        self.notification_load_more_button = QPushButton(self.notificationTab_tab_4)
        self.notification_load_more_button.setObjectName("notification_load_more_button")
        self.gridLayout_8.addWidget(self.notification_load_more_button, 1, 4, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_8, 2, 0, 1, 1)
        ###retranslate
        self.title_label.setText(
            QApplication.translate("MainWindow", "<html><head/><body><p align=\"center\">"
                                                 "<span style=\" font-weight:600;font-size:20px\">"
                                                 "<u>All Notifications</u></span></p></body></html>",
                                   None, QApplication.UnicodeUTF8))
        self.id_label.setText(QApplication.translate("MainWindow",
                                                     "Message Id", None, QApplication.UnicodeUTF8))
        self.notification_schedule_fromdate_label.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.notification_schedule_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.notification_schedule_todate_label.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.notification_schedule_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.type_label.setText(
            QApplication.translate("MainWindow", "Type", None, QApplication.UnicodeUTF8))
        self.batch_label.setText(
            QApplication.translate("MainWindow", "Number of Notifications", None, QApplication.UnicodeUTF8))
        self.notification_schedule_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Message Id", None, QApplication.UnicodeUTF8))
        self.notification_schedule_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.notification_schedule_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "From", None, QApplication.UnicodeUTF8))
        self.notification_schedule_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Message", None, QApplication.UnicodeUTF8))
        self.notification_schedule_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "State", None, QApplication.UnicodeUTF8))
        self.notification_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.notification_reset_button.setText(
            QApplication.translate("MainWindow", "Reset All", None, QApplication.UnicodeUTF8))
        self.notification_load_more_button.setText(
            QApplication.translate("MainWindow", "Load More", None, QApplication.UnicodeUTF8))
        ##signals and slotts && other stuffs
        self.scheduletable_count = 0
        self.addtable_count = 0
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.notification_schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.batch_number = None
        self.notification_results.addItems([str(i) for i in range(1, 50, 5)])
        self.notification_states.addItems(['All', 'New', 'To Do', 'Done'])
        self.message = Messaging()
        self.notification_load_more_button.clicked.connect(self.load_more)
        self.notification_search_button.clicked.connect(self.search_messages)
        self.notification_reset_button.clicked.connect(self.reset_all)
        self.notificationTab_tab_4.setFocusPolicy(Qt.StrongFocus)
        self.notificationTab_tab_4.focusInEvent = self.load_rows
        # self.assign_shortcuts()

        # def assign_shortcuts(self):
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_search']),
        # self.notificationTab_tab_4, self.search_messages)
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_additem']),
        # self.notificationTab_tab_4, self.add_new_blank_rows)
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_print']),
        # self.notificationTab_tab_4, self.commit_and_print)
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_today']),
        # self.notificationTab_tab_4, lambda: self.load_messages('today'))
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_tommorow']),
        # self.notificationTab_tab_4, lambda: self.load_messages('tomorrow'))
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_thismonth']),
        # self.notificationTab_tab_4, lambda: self.load_messages('month'))
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_thisweek']),
        # self.notificationTab_tab_4, lambda: self.load_messages('week'))
        # QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorynotification_clear']),
        # self.notificationTab_tab_4, self.clear_table)

    def add_messages(self, *args):
        """
        Populates the Schedules when we load the tab
        """
        table = self.notification_schedule_table
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    item = QTableWidgetItem(j['msg_id'])
                    table.setItem(i, 0, item)
                    item = QTableWidgetItem(j['date'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(
                        'Name:{}\nDesignation:{}\nAddress:{}'.format(j['name'], j['designation'], j['address']))
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem('Message Type:{}\nMessage:{}'.format(j['msg_type'].title(), j['msg_body']))
                    table.setItem(i, 3, item)
                    states = QComboBox()
                    self.populate_states(states, j['msg_state'].title())
                    states.currentIndexChanged.connect(lambda index, row=i: self.changed_state(row, index))
                    table.setCellWidget(i, 4, states)
            elif args[0] == 'new':
                initial = table.rowCount()
                row = table.rowCount() + len(args[1])
                table.setRowCount(row)
                forward_range = range(initial, row)
                for i, j in zip(forward_range, args[1]):
                    item = QTableWidgetItem(j['msg_id'])
                    table.setItem(i, 0, item)
                    item = QTableWidgetItem(j['date'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(
                        'Name:{}\nDesignation:{}\nAddress:{}'.format(j['name'], j['designation'], j['address']))
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(
                        'Message Type:{}\nMessage:{}'.format(j['msg_type'].title(), j['msg_body']))
                    table.setItem(i, 3, item)
                    states = QComboBox()
                    self.populate_states(states, j['msg_state'].title())
                    states.currentIndexChanged.connect(lambda index, row=i: self.changed_state(row, index))
                    table.setCellWidget(i, 4, states)
        table.setColumnWidth(0, (table.width() * 0.5) / 5)
        table.setColumnWidth(1, (table.width() * 0.5) / 5)
        table.setColumnWidth(2, table.width() / 5)
        table.setColumnWidth(3, (table.width() * 2) / 5)
        self.notification_schedule_table.resizeRowsToContents()

    def populate_states(self, combo, state):
        """
        fills the supplier list for each item line
        :param combo: the combo box of suppliers
        :return:none
        """
        combo.setStyleSheet("QAbstractItemView{"
                            "background: #4B77BE;"
                            "}")
        combo.addItems(['New', 'To Do', 'Done'])
        index = combo.findText(state)
        combo.setCurrentIndex(index)

    def changed_state(self, row, index):
        """
        fill the item combo box
        :param combo: the combobox object
        :return: none
        """
        table = self.notification_schedule_table
        data = {}
        data['message_id'] = table.item(row, 0).text()
        data['msg_state'] = table.cellWidget(row, 4).currentText()
        msg = QMessageBox.information(QMessageBox(), 'Alert!!', 'Do you want to change the status of the Message??',
            QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            report = self.message.update_message(data)
            if report:
                _ = QMessageBox.information(QMessageBox(), 'Success!!', 'The Message was updated',
                    QMessageBox.Yes | QMessageBox.No)
            else:
                _ = QMessageBox.critical(QMessageBox(), 'Error!!', 'The Message was not updated',
                    QMessageBox.Yes | QMessageBox.No)

    def search_messages(self):
        """
        Searches for messages when search button is pressed
        """
        logger.info('Notifications searching messages initiated')
        from_date = self.notification_schedule_fromdate_dateedit.text()
        to_date = self.notification_schedule_todate_dateedit.text()
        limit = self.notification_results.currentText()
        msg_id = self.id_line.text()
        msg_state = self.notification_states.currentText()
        dataobj = self.message.load_message(limit=limit, from_date=from_date, to_date=to_date, msg_id=msg_id,
                                            msg_state=msg_state)
        if dataobj:
            self.add_messages(*dataobj)
        else:
            self.notification_schedule_table.clearContents()
            self.notification_schedule_table.setRowCount(0)

    def load_more(self):
        """
        Searches for messages when search button is pressed
        """
        logger.info('Notifications searching messages initiated')
        from_date = self.notification_schedule_fromdate_dateedit.text()
        to_date = self.notification_schedule_todate_dateedit.text()
        limit = self.notification_results.currentText()
        msg_id = self.id_line.text()
        msg_state = self.notification_states.currentText()
        offset = self.notification_schedule_table.rowCount()
        dataobj = self.message.load_message(limit=limit, from_date=from_date, to_date=to_date, msg_id=msg_id,
                                            msg_state=msg_state, offset=offset)
        if dataobj:
            self.add_messages('new', dataobj)
        else:
            self.notification_schedule_table.clearContents()
            self.notification_schedule_table.setRowCount(0)

    def load_single_message(self, msg_id):  # api
        """method to load a single message"""
        self.reset_all()
        dataobj = self.message.load_message(msg_id=msg_id)
        if dataobj:
            self.add_messages('new', dataobj)
            self.id_line.setText(str(msg_id))
        else:
            self.notification_schedule_table.clearContents()
            self.notification_schedule_table.setRowCount(0)

    def load_rows(self, event):
        """
        :return:loads the rows
        """
        self.add_messages()

    def reset_all(self):
        """
        :return: resets the the data in the search text
        """
        try:
            self.id_line.clear()
            self.notification_schedule_table.clearContents()
            self.notification_schedule_table.setRowCount(0)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class NotificationTemplate(QWidget):
    """new implementation for top notification"""
    custom_signal = Signal(int)

    def __init__(self, parent=None):
        super(NotificationTemplate, self).__init__(parent)
        self.setObjectName('notification_template')
        self.msg_id = ''
        self.horizontal = QVBoxLayout(self)
        self.body = QLabel(self)
        self.body.mouseReleaseEvent = self.mouseReleaseEvent
        self.horizontal.addWidget(self.body)
        self.setStyleSheet('QWidget:hover {'
                           'background-color:#4285f4;color:white;}')

    def mouseReleaseEvent(self, event):
        # super(NotificationTemplate, self).mouseReleaseEvent(event)
        self.custom_signal.emit(self.msg_id)

    def new_notification(self, text):
        """creates a new notification"""
        self.msg_id = text['message id']
        s = ''
        s += "<p><span style=\"font-size:14pt; font-weight:600;\">Designation:{}</span></p>".format(text['from'][1])
        s += '<p>'
        s += 'From:{}<br/>'.format(text['from'][0])
        s += 'Date:{}<br/>'.format(text['sent'])
        body = 'Message:'
        body += text['body'].replace('\n', '')
        for i, j in enumerate(body):
            if i and i % 39 == 0:
                s += '<br/>'
            s += j
        s += '</p>'
        value = s
        self.body.setText(str(value))
