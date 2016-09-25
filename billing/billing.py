#! /usr/bin/env python

""" Billing module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from datetime import datetime, timedelta
from cdecimal import Decimal

from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QGridLayout, QTableWidget, QPushButton, QAbstractItemView, QPrintDialog, QDialog, QLabel, QDateEdit, QLineEdit, \
    QMessageBox, QIntValidator, QCompleter, QStringListModel, QTabBar, QShortcut, QKeySequence, QCheckBox, QHBoxLayout, \
    QComboBox
from PySide.QtCore import Qt, QDate, SIGNAL, QCoreApplication, QTimer
from printer.print_execute import PrintNow
from billing_tryton import Search, SearchMenu, SaveBill, Customer, SaveTicket
from inventory.inventory import SupplierAddDialog as CustomerForm
from menu.menu_tryton import WeeklyMenu
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class CustomerSearch(QLineEdit):
    """Class to extend linedit to add customer search feature"""
    def __init__(self, parent=None):
        super(CustomerSearch, self).__init__(parent)
        self.completer = QCompleter()
        self.completer.popup().setStyleSheet("background-color: #4B77BE;")
        self.setCompleter(self.completer)
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setWrapAround(False)
        self.textChanged.connect(self.get_customer)
        self.setAlignment(Qt.AlignCenter)
        self.search = Customer()

    def get_customer(self, text):
        """
        gets the customers from backend
        :param text: the text input
        :return:none
        """
        try:
            if len(text) == 1:
                self.auto_capital()
            if len(text) == 3:
                customers = self.search.search_item(text)
                count = self.model.rowCount()
                self.model.removeRows(0, count)
                self.model.setStringList(customers)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_customer_id(self, code):
        """
        searches a customer corresponding to the id
        :param code:the code of the customer
        :return:none
        """
        try:
            customer = self.search.search_customer_id(code=code)
            if customer:
                self.setText(customer)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def auto_capital(self):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        try:
            text = self.text()
            self.setText(text.title())
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class Billing():
    """Main billing outer tab class"""
    def __init__(self):
        ####
        self.billing_tab_2 = QWidget()
        self.billing_tab_2.setStyleSheet("")
        self.billing_tab_2.setObjectName("billing_tab_2")
        self.horizontalLayout_4 = QHBoxLayout(self.billing_tab_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.billing_detail_tabWidget = QTabWidget(self.billing_tab_2)
        self.billing_detail_tabWidget.setTabsClosable(True)
        self.billing_detail_tabWidget.setObjectName("billing_detail_tabWidget")
        self.add_tabs()
        self.horizontalLayout_4.addWidget(self.billing_detail_tabWidget)
        #### signals and slots && other stuffs
        self.billing_detail_tabWidget.tabCloseRequested.connect(self.close_my_tab)
        tab_1 = self.billing_detail_tabWidget.tabBar()
        closebutton = tab_1.tabButton(0, QTabBar.RightSide)
        closebutton.hide()  # to hide the close button of the first tab
        closebutton = tab_1.tabButton(1, QTabBar.RightSide)
        closebutton.hide()  # to hide the close button of the first tab
        self.billing_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.billing_tab_2.setFocusPolicy(Qt.StrongFocus)
        self.billing_tab_2.focusInEvent = self.change_focus

    def close_my_tab(self, index):
        """
        closes the tab and deletes the object
        :param index: the index of the tab
        :return: none
        """
        try:
            wid = self.billing_detail_tabWidget.widget(index)
            self.billing_detail_tabWidget.removeTab(index)
            del wid
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_tabs(self):
        """
        adds new tab
        :return: none
        """
        try:
            search = SearchBill(self.billing_detail_tabWidget)
            ticket = SearchTicket(self.billing_detail_tabWidget)
            self.billing_detail_tabWidget.addTab(search.billing_main_tab, "&Bills")
            self.billing_detail_tabWidget.addTab(ticket.ticket_main_tab, "&Ticket")
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def change_focus(self, event=None):  # set focus need not run properly
        """
        responds to the changes of the focus
        :param event:focus event
        :return:none
        """
        try:
            wid = self.billing_detail_tabWidget.currentWidget()
            if wid.isVisible():
                wid.setFocus()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class SearchBill():
    """Tab where we can search and find bills"""
    global logger

    def __init__(self, parenttab):
        #######
        logger.info('Inside SearchBill')
        self.parenttab = parenttab
        self.billing_main_tab = QWidget()
        self.billing_main_tab.setObjectName("billing_main_tab")
        self.gridLayout_25 = QGridLayout(self.billing_main_tab)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_15 = QLabel(self.billing_main_tab)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_10.addWidget(self.label_15)
        self.bills_billno_linedit = QLineEdit(self.billing_main_tab)
        self.bills_billno_linedit.setObjectName("bills_billno_linedit")
        self.horizontalLayout_10.addWidget(self.bills_billno_linedit)
        self.label_16 = QLabel(self.billing_main_tab)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_10.addWidget(self.label_16)
        self.bills_fromdate_dateedit = QDateEdit(self.billing_main_tab)
        self.bills_fromdate_dateedit.setCalendarPopup(True)
        self.bills_fromdate_dateedit.setObjectName("bills_fromdate_dateedit")
        self.horizontalLayout_10.addWidget(self.bills_fromdate_dateedit)
        self.label_17 = QLabel(self.billing_main_tab)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_10.addWidget(self.label_17)
        self.bills_todate_dateedit = QDateEdit(self.billing_main_tab)
        self.bills_todate_dateedit.setCalendarPopup(True)
        self.bills_todate_dateedit.setObjectName("bills_todate_dateedit")
        self.horizontalLayout_10.addWidget(self.bills_todate_dateedit)
        self.bills_search_button = QPushButton(self.billing_main_tab)
        self.bills_search_button.setObjectName("bills_search_button")
        self.horizontalLayout_10.addWidget(self.bills_search_button)
        self.gridLayout_25.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)
        self.bills_billlist_table = QTableWidget(self.billing_main_tab)
        self.bills_billlist_table.setObjectName("bills_billlist_table")
        self.bills_billlist_table.setColumnCount(3)
        self.bills_billlist_table.setRowCount(0)
        self.bills_billlist_table.setSortingEnabled(True)
        item = QTableWidgetItem()
        self.bills_billlist_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.bills_billlist_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.bills_billlist_table.setHorizontalHeaderItem(2, item)
        self.bills_billlist_table.horizontalHeader().setCascadingSectionResizes(True)
        self.bills_billlist_table.horizontalHeader().setStretchLastSection(True)
        self.bills_billlist_table.verticalHeader().setVisible(False)
        self.bills_billlist_table.verticalHeader().setCascadingSectionResizes(True)
        self.bills_billlist_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_25.addWidget(self.bills_billlist_table, 1, 0, 1, 1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.bills_newbill_button = QPushButton(self.billing_main_tab)
        self.bills_newbill_button.setObjectName("bills_newbill_button")
        self.horizontalLayout_11.addWidget(self.bills_newbill_button)
        self.bills_ticketbill_button = QPushButton(self.billing_main_tab)
        self.bills_ticketbill_button.setObjectName("bills_ticketbill_button")
        self.horizontalLayout_11.addWidget(self.bills_ticketbill_button)
        self.bills_reset_button = QPushButton(self.billing_main_tab)
        self.bills_reset_button.setObjectName("bills_reset_button")
        self.horizontalLayout_11.addWidget(self.bills_reset_button)
        self.bills_customertab_button = QPushButton(self.billing_main_tab)
        self.bills_customertab_button.setObjectName('bills_customertab_button')
        self.horizontalLayout_11.addWidget(self.bills_customertab_button)
        self.bills_credittab_button = QPushButton(self.billing_main_tab)
        self.bills_credittab_button.setObjectName('bills_credittab_button')
        self.horizontalLayout_11.addWidget(self.bills_credittab_button)
        self.bills_print_button = QPushButton(self.billing_main_tab)
        self.bills_print_button.setObjectName('bills_print_button')
        self.horizontalLayout_11.addWidget(self.bills_print_button)
        self.gridLayout_25.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        #####retranslate
        self.label_15.setText(
            QApplication.translate("MainWindow", "Bill No", None, QApplication.UnicodeUTF8))
        self.bills_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.label_16.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.bills_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.label_17.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.bills_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.bills_billlist_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Bill No", None, QApplication.UnicodeUTF8))
        self.bills_billlist_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.bills_billlist_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Grand Total", None, QApplication.UnicodeUTF8))
        self.bills_newbill_button.setText(
            QApplication.translate("MainWindow", "New Bill", None, QApplication.UnicodeUTF8))
        self.bills_ticketbill_button.setText(
            QApplication.translate("MainWindow", "Bill Tickets", None, QApplication.UnicodeUTF8))
        self.bills_reset_button.setText(
            QApplication.translate("MainWindow", "Reset Search", None, QApplication.UnicodeUTF8))
        self.bills_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.bills_credittab_button.setText(
            QApplication.translate("MainWindow", "Show Credits", None, QApplication.UnicodeUTF8))
        self.bills_customertab_button.setText(
            QApplication.translate("MainWindow", "Show Customers", None, QApplication.UnicodeUTF8))
        self.bills_print_button.setText(
            QApplication.translate("MainWindow", "Print Report", None, QApplication.UnicodeUTF8))
        # self.bills_search_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+Shift+E", None, QApplication.UnicodeUTF8))
        ####signals and slots && other stuffs
        self.billing_main_tab.setFocusPolicy(Qt.StrongFocus)
        self.billing_main_tab.focusInEvent = self.change_focus
        self.bill = Search()
        self.bill_number = None
        # self.bills_newbill_button.clicked = self.add_new_tab
        self.bills_billlist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bills_billlist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bills_billlist_table.setShowGrid(False)
        self.bills_search_button.clicked.connect(self.search_bill)
        self.bills_reset_button.clicked.connect(self.reset_all)
        self.bills_newbill_button.clicked.connect(self.add_new_tab)
        self.bills_billlist_table.itemDoubleClicked.connect(self.find_bill_and_add_tab)
        self.bills_todate_dateedit.setMaximumDate(QDate.currentDate())
        self.bills_todate_dateedit.setDate(QDate.currentDate())
        self.bills_credittab_button.clicked.connect(self.add_credit_tab)
        self.bills_customertab_button.clicked.connect(self.add_cutomer_tab)
        self.bills_ticketbill_button.clicked.connect(self.bill_tickets)
        self.bills_print_button.clicked.connect(self.print_bill)
        today = datetime.today()
        fewdaysback = today - timedelta(days=15)
        self.bills_fromdate_dateedit.setDate(QDate.fromString(fewdaysback.strftime('%d/%m/%Y'), 'dd/MM/yyyy'))
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """
        assigns shortcuts to buttons
        :return:none
        """
        try:
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_newbill']),
                      self.billing_main_tab, self.add_new_tab)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_reset']),
                      self.billing_main_tab, self.reset_all)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_search']),
                      self.billing_main_tab, self.search_bill)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_selectbill']),
                      self.billing_main_tab, self.row_selected)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_showcredit']),
                      self.billing_main_tab, self.add_credit_tab)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingbills_showcustomer']),
                      self.billing_main_tab, self.add_cutomer_tab)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_credit_tab(self):
        """
        adds a new credit tab
        :return:none
        """
        try:
            tab = CreditTab(parent=self, parenttab=self.parenttab)
            count = self.parenttab.addTab(tab.billing_credit_tab, '&Credit Tab')
            self.parenttab.setCurrentIndex(count)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_cutomer_tab(self):
        """
        adds a new customer tab
        :return:none
        """
        try:
            tab = CustomerTab(parent=self, parenttab=self.parenttab)
            count = self.parenttab.addTab(tab.customer_tab, 'Cust&omer Tab')
            self.parenttab.setCurrentIndex(count)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def bill_tickets(self):
        """method to create bills from the tickets"""
        self.bill_number = None
        bill = TicketBill(self)
        bill.exec_()
        if self.bill_number:
            self.add_new_tab(int(self.bill_number))

    def row_selected(self):
        """
        checks the selected row and opens the new tab, equivalent to double click on row
        :return: nope
        """
        try:
            rows = sorted(set(index.row() for index in
                              self.bills_billlist_table.selectedIndexes()))
            if rows:
                self.add_new_tab(int(self.bills_billlist_table.item(rows[0], 0).text()))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def find_bill_and_add_tab(self, item):
        """
        finds the bill number of the row and add it to the tab
        :param item: item clicked
        :return:none
        """
        try:
            model_index = self.bills_billlist_table.indexFromItem(item)
            row = model_index.row()
            bill_no_item = self.bills_billlist_table.item(row, 0)
            self.add_new_tab(int(bill_no_item.text()))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_new_tab(self, *args):
        """
        adds a new tab
        :param args:bill number and other texts
        :return:none
        """
        try:
            logger.info('SearchBill new tab adding initiated')
            tab_name = u"Bill(&%s)" % self.parenttab.count()
            if not args:
                tab = NewTab()
            else:
                tab = NewTab(*args)
                tab_name = u"Bill:&%s" % tab.billnumber
            count = self.parenttab.addTab(tab.billing_tab_1, tab_name)
            self.parenttab.setCurrentIndex(count)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_bill(self):
        """
        :return:search the bills and add them in the bill list table
        """
        try:
            logger.info('SearchBill bill searching initiated')
            self.bills_billlist_table.clearContents()
            bill_no = self.bills_billno_linedit.text()
            from_date = self.bills_fromdate_dateedit.date()
            from_date = from_date.toString('yyyy-MM-dd')
            to_date = self.bills_todate_dateedit.date()
            to_date = to_date.toString('yyyy-MM-dd')
            bill_list = self.bill.search_bills(bill_no=bill_no, from_date=from_date, to_date=to_date)
            self.load_rows(*bill_list)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def reset_all(self):
        """
        :return: resets the the data in the search text
        """
        try:
            self.bills_billno_linedit.clear()
            self.bills_billlist_table.clearContents()
            self.bills_billlist_table.setRowCount(0)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_rows(self, *args):
        """
        :param args: the list of data
        :return:loads the rows with the list of bills
        """
        try:
            if args:
                self.bills_billlist_table.setRowCount(len(args))

            table = self.bills_billlist_table
            for j, i in enumerate(args):
                item = QTableWidgetItem(i['bill_no'])
                table.setItem(j, 0, item)
                item = QTableWidgetItem(i['date'])
                table.setItem(j, 1, item)
                item = QTableWidgetItem(i['total'])
                table.setItem(j, 2, item)
            table.setColumnWidth(0, (table.width() / 3))
            table.setColumnWidth(1, (table.width() / 3))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def change_focus(self, event):
        """
        :return:just had to use this because clicks were not working
        """
        try:
            self.load_rows()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def print_bill(self):
        """
        prints the bill
        """
        logger.info('NewTab bill printing initiated')
        try:
            dialog = QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                p = dialog.printer()
                dataobj = self.get_data()
                if dataobj:
                    printing = PrintNow(p.printerName(), dataobj, 'bill_report')
                    printing.start_print()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_data(self):
        """
        fetches all the data for printing
        :return:list of dictionary
        """
        try:
            table = self.bills_billlist_table
            rows = table.rowCount()
            dataobj = []
            lines = []
            for i in range(rows):
                dictionary = {}
                item = table.cellWidget(i, 0) if table.cellWidget(i, 0) is not None else table.item(i, 0)
                dictionary['bill_no'] = item.text()
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['date'] = item.text()
                if dictionary['date'] == '' and dictionary['bill_no'] == '':
                    continue
                elif dictionary['date'] == '':
                    return False
                item = table.cellWidget(i, 2) if table.cellWidget(i, 2) is not None else table.item(i, 2)
                dictionary['total'] = item.text()
                lines.append(dictionary)
            if not lines:
                return False
            dataobj.append(lines)
            dictionary = {}
            dictionary['total'] = self.get_grand_total(lines=lines)
            from_date = self.bills_fromdate_dateedit.date()
            dictionary['from_date'] = from_date.toString('yyyy-MM-dd')
            to_date = self.bills_todate_dateedit.date()
            dictionary['to_date'] = to_date.toString('yyyy-MM-dd')
            dataobj.append(dictionary)
            return dataobj
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_grand_total(self, lines):
        """get the total of the bills"""
        total = Decimal(0)
        for i in lines:
            total += Decimal(i['total'])
        return total.quantize(Decimal('1.00')).to_eng()


class CreditTab():
    """Tab to maintain creditors"""
    global logger

    def __init__(self, parent, parenttab):
        #######
        logger.info('Inside CreditTab')
        self.parent = parent
        self.super_parent = parenttab
        self.billing_credit_tab = QWidget()
        self.billing_credit_tab.setObjectName("billing_credit_tab")
        self.gridLayout = QGridLayout(self.billing_credit_tab)
        self.gridLayout.setObjectName("gridLayout")
        select_label = QLabel(self.billing_credit_tab)
        self.gridLayout.addWidget(select_label, 0, 0, 1, 1)
        self.billing_search_linedit = CustomerSearch()
        self.billing_search_linedit.setObjectName('billing_search_linedit')
        self.gridLayout.addWidget(self.billing_search_linedit, 0, 1, 1, 1)
        self.billing_credit_table = QTableWidget(self.billing_credit_tab)
        self.billing_credit_table.setObjectName("billing_credit_table")
        self.billing_credit_table.setSortingEnabled(True)
        self.billing_credit_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.billing_credit_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.billing_credit_table.setShowGrid(False)
        self.billing_credit_table.setColumnCount(6)
        self.billing_credit_table.setRowCount(0)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.billing_credit_table.setHorizontalHeaderItem(5, item)
        self.billing_credit_table.horizontalHeader().setCascadingSectionResizes(True)
        self.billing_credit_table.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.billing_credit_table, 1, 0, 1, 4)
        self.billing_pay_button = QPushButton(self.billing_credit_tab)
        self.billing_pay_button.setObjectName('billing_pay_button')
        self.gridLayout.addWidget(self.billing_pay_button, 2, 0, 1, 1)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer_item, 2, 1, 1, 1)
        label = QLabel(self.billing_credit_tab)
        self.gridLayout.addWidget(label, 2, 2, 1, 1)
        self.billing_total_linedit = QLineEdit(self.billing_credit_tab)
        self.billing_total_linedit.setObjectName('billing_total_linedit')
        self.billing_total_linedit.setDisabled(True)
        self.gridLayout.addWidget(self.billing_total_linedit, 2, 3, 1, 1)
        #####retranslate
        select_label.setText(
            QApplication.translate('MainWindow', 'Select Customer', None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select", None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Name", None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Bill Id", None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.billing_credit_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Due", None, QApplication.UnicodeUTF8))
        self.billing_pay_button.setText(
            QApplication.translate('MainWindow', 'Pay', None, QApplication.UnicodeUTF8))
        label.setText(
            QApplication.translate("MainWindow", "Total", None, QApplication.UnicodeUTF8))
        #### signals and slotts &&& other stuffs
        self.bill = Search()
        self.payment_class = SaveBill()
        self.billing_credit_table.horizontalHeader().sectionClicked.connect(self.select_all_checkbox)
        self.call = self.search_bills  # todo find the reason why combo behaves wierd
        self.billing_search_linedit.returnPressed.connect(self.search_bills)
        self.billing_credit_table.itemDoubleClicked.connect(self.find_bill_and_add_tab)
        self.billing_pay_button.clicked.connect(self.pay_bills)

    def select_all_checkbox(self, item):
        """
        selects all checkboxes in the table
        :param item:header item
        :return:none
        """
        try:
            if item == 0:
                row = self.billing_credit_table.rowCount()
                for i in range(row):
                    checkbox = self.billing_credit_table.cellWidget(i, item)
                    if not checkbox.isChecked():
                        checkbox.setCheckState(Qt.Checked)
                    else:
                        checkbox.setCheckState(Qt.Unchecked)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_bills(self):
        """
        searches bills in the backend
        :return:none
        """
        try:
            customer = self.billing_search_linedit.text().split('-')[0]
            if not customer:
                data = self.bill.search_bills(customercode='All')
            else:
                data = self.bill.search_bills(customercode=customer)
            if data:
                self.load_table(*data)
            else:
                self.billing_credit_table.clearContents()
                self.billing_credit_table.setRowCount(0)
            self.sum_total()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def sum_total(self):
        """
        sums all the amounts in the table
        :return: none
        """
        try:
            table = self.billing_credit_table
            row = table.rowCount()
            total = Decimal(0)
            for i in range(row):
                value = table.item(i, 5).text()
                total += Decimal(value)
            self.billing_total_linedit.setText(total.to_eng())
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_table(self, *args):
        """
        loads the data in the table
        :param args: the list of dictionary
        :return:none
        """
        try:
            table = self.billing_credit_table
            if args:
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    chk = QCheckBox()
                    table.setCellWidget(i, 0, chk)
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['name'])
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(j['bill_no'])
                    table.setItem(i, 3, item)
                    item = QTableWidgetItem(j['date'])
                    table.setItem(i, 4, item)
                    item = QTableWidgetItem(j['total'])
                    table.setItem(i, 5, item)
            table.setColumnWidth(0, ((table.width() * 0.4) / 6))
            table.setColumnWidth(1, ((table.width() * 0.5) / 6))
            table.setColumnWidth(2, (table.width() / 6) * 2)
            table.setColumnWidth(3, (table.width() / 6))
            table.setColumnWidth(4, (table.width() / 6))
            table.horizontalHeader().setStretchLastSection(True)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def find_bill_and_add_tab(self, item):
        """
        finds the bill number of the row and add it to the tab
        :param item: item clicked
        :return:none
        """
        try:
            model_index = self.billing_credit_table.indexFromItem(item)
            row = model_index.row()
            bill_no_item = int(self.billing_credit_table.item(row, 3).text())
            self.parent.add_new_tab(bill_no_item)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def pay_bills(self):
        """
        pays the bills of the customer
        :return:None
        """
        try:
            row = self.billing_credit_table.rowCount()
            for i in range(row):
                checkbox = self.billing_credit_table.cellWidget(i, 0)
                if checkbox.isChecked():
                    bill_no_item = int(self.billing_credit_table.item(i, 3).text())
                    result = self.payment_class.pay_bill(bill_no_item)
                    if not result:
                        QMessageBox(QMessageBox(), 'Error!!', 'Payment failed for bill:%d' % bill_no_item,
                            QMessageBox.Ok)
            self.search_bills()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class CustomerTab():
    """Tab to maintain custome details"""
    global logger

    def __init__(self, parent, parenttab):
        #######
        logger.info('Inside Customer')
        self.parent = parent
        self.super_parent = parenttab
        self.customer_tab = QWidget()
        self.customer_tab.setObjectName("customer_tab")
        self.gridLayout = QGridLayout(self.customer_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.customer_table = QTableWidget(self.customer_tab)
        self.customer_table.setObjectName("customer_table")
        self.customer_table.setSortingEnabled(True)
        self.customer_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.customer_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.customer_table.setShowGrid(False)
        self.customer_table.setColumnCount(3)
        self.customer_table.setRowCount(0)
        item = QTableWidgetItem()
        self.customer_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.customer_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.customer_table.setHorizontalHeaderItem(2, item)
        self.customer_table.horizontalHeader().setCascadingSectionResizes(True)
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.customer_table, 0, 0, 1, 4)
        self.customer_add = QPushButton(self.customer_tab)
        self.customer_add.setObjectName('customer_add')
        self.gridLayout.addWidget(self.customer_add, 1, 3, 1, 1)
        # retranslate
        self.customer_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.customer_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Name", None, QApplication.UnicodeUTF8))
        self.customer_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Due", None, QApplication.UnicodeUTF8))
        self.customer_add.setText(
            QApplication.translate('MainWindow', 'Add Customer', None, QApplication.UnicodeUTF8))
        # signals && slots and other stuffs
        self.customer_table.itemDoubleClicked.connect(self.add_customer)
        self.customer_add.clicked.connect(self.add_customer)
        self.customer = Customer()
        self.search_customers()
        self.customer_tab.focusInEvent = self.change_focus

    def search_customers(self):
        """
        searches for customer
        :return:none
        """
        try:
            data = self.customer.search_customers()
            self.load_table(*data)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_table(self, *args):
        """
        loads the table data
        :param args:the list of dictionaries
        :return:none
        """
        try:
            table = self.customer_table
            if args:
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 0, item)
                    item = QTableWidgetItem(j['name'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['total'])
                    table.setItem(i, 2, item)
            table.setColumnWidth(0, (table.width() / 3))
            table.setColumnWidth(1, (table.width() / 3))
            table.horizontalHeader().setStretchLastSection(True)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_customer(self, item=None):
        """
        finds the bill number of the row and add it to the tab
        :param item: item clicked
        :return:none
        """
        try:
            if item:
                model_index = self.customer_table.indexFromItem(item)
                row = model_index.row()
                code = self.customer_table.item(row, 0)
                customer = CustomerAdd(code=code)
            else:
                customer = CustomerAdd()
            customer.exec_()
            self.search_customers()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def change_focus(self, focus=None):
        """
        Focus hack to manage tables
        :return:none
        """
        try:
            self.load_table()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class CustomerAdd(CustomerForm):
    """Add new customer"""
    global logger

    def __init__(self, parent=None, code=None):
        super(CustomerAdd, self).__init__(parent=parent, code=code,
                                          category='Customer')  # this calls the supplier already start here
        self.category = 'Customer'
        self.setWindowTitle('Customer Form')
        self.dialogue.label.setText('Customer Name')


class NewTab():
    """New Bill creation tab"""
    global logger

    def __init__(self, *args):
        logger.info('Inside NewTab')
        self.billing_tab_1 = QWidget()
        self.billing_tab_1.setStyleSheet("")
        self.billing_tab_1.setObjectName("billing_tab_1")
        self.gridLayout_13 = QGridLayout(self.billing_tab_1)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.billing_table = QTableWidget(self.billing_tab_1)
        self.billing_table.setObjectName("billing_table")
        self.billing_table.setColumnCount(5)
        self.billing_table.setRowCount(0)
        item = QTableWidgetItem()
        self.billing_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.billing_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.billing_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.billing_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.billing_table.setHorizontalHeaderItem(4, item)
        self.billing_table.horizontalHeader().setCascadingSectionResizes(True)
        self.billing_table.horizontalHeader().setStretchLastSection(True)
        self.billing_table.verticalHeader().setVisible(True)
        self.billing_table.verticalHeader().setCascadingSectionResizes(True)
        self.billing_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_13.addWidget(self.billing_table, 0, 0, 1, 1)
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.billing_assign_linedit = CustomerSearch(self.billing_tab_1)
        self.billing_assign_linedit.setObjectName('billing_assign_linedit')
        self.billing_assign_linedit.setPlaceholderText('Credit Customer')
        self.gridLayout_12.addWidget(self.billing_assign_linedit, 0, 0, 1, 1)
        self.label_6 = QLabel(self.billing_tab_1)
        self.label_6.setObjectName("label_6")
        self.gridLayout_12.addWidget(self.label_6, 0, 3, 1, 1)
        self.billing_total_linedit = QLineEdit(self.billing_tab_1)
        self.billing_total_linedit.setObjectName("billing_total_linedit")
        self.gridLayout_12.addWidget(self.billing_total_linedit, 0, 4, 1, 1)
        self.billing_tax_label = QLabel(self.billing_tab_1)
        self.billing_tax_label.setObjectName("billing_tax_label")
        self.gridLayout_12.addWidget(self.billing_tax_label, 1, 3, 1, 1)
        self.billing_servicetax_linedit = QLineEdit(self.billing_tab_1)
        self.billing_servicetax_linedit.setObjectName("billing_servicetax_linedit")
        self.gridLayout_12.addWidget(self.billing_servicetax_linedit, 1, 4, 1, 1)
        self.label_9 = QLabel(self.billing_tab_1)
        self.label_9.setObjectName("label_9")
        self.gridLayout_12.addWidget(self.label_9, 2, 3, 1, 1)
        self.billing_roundoff_linedit = QLineEdit(self.billing_tab_1)
        self.billing_roundoff_linedit.setObjectName("billing_roundoff_linedit")
        self.gridLayout_12.addWidget(self.billing_roundoff_linedit, 2, 4, 1, 1)
        self.label_8 = QLabel(self.billing_tab_1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_12.addWidget(self.label_8, 3, 3, 1, 1)
        self.billing_grandtotal_linedit = QLineEdit(self.billing_tab_1)
        self.billing_grandtotal_linedit.setObjectName("billing_grandtotal_linedit")
        self.gridLayout_12.addWidget(self.billing_grandtotal_linedit, 3, 4, 1, 1)
        self.billing_status_label = QLabel(self.billing_tab_1)
        self.billing_status_label.setObjectName("billing_status_label")
        self.gridLayout_12.addWidget(self.billing_status_label, 4, 0, 1, 1)
        spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem18, 4, 1, 1, 1)
        self.billing_paid_button = QPushButton(self.billing_tab_1)
        self.billing_paid_button.setObjectName("billing_paid_button")
        self.gridLayout_12.addWidget(self.billing_paid_button, 4, 2, 1, 1)
        # self.billing_save_button = QPushButton(self.billing_tab_1)
        # self.billing_save_button.setObjectName("billing_save_button")
        # self.gridLayout_12.addWidget(self.billing_save_button, 3, 3, 1, 1)
        self.billing_assign_button = QPushButton(self.billing_tab_1)
        self.billing_assign_button.setObjectName('billing_assign_button')
        self.gridLayout_12.addWidget(self.billing_assign_button, 4, 3, 1, 1)
        self.billing_print_button = QPushButton(self.billing_tab_1)
        self.billing_print_button.setObjectName("billing_print_button")
        self.gridLayout_12.addWidget(self.billing_print_button, 4, 4, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_12, 1, 0, 1, 1)
        # self.billing_detail_tabWidget.addTab(self.billing_tab_1, "")
        # please add the obj.billing_tab_! as a tab in billing_detail_tabWidget
        self.billing_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.billing_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.billing_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Rate", None, QApplication.UnicodeUTF8))
        self.billing_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.billing_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Amount", None, QApplication.UnicodeUTF8))
        self.billing_paid_button.setText(QApplication.translate("MainWindow", "Pay", None, QApplication.UnicodeUTF8))
        self.billing_tax_label.setText(
            QApplication.translate("MainWindow", "Service Tax", None, QApplication.UnicodeUTF8))
        self.billing_assign_button.setText(
            QApplication.translate("MainWindow", "Assign Credit", None, QApplication.UnicodeUTF8))
        self.label_6.setText(QApplication.translate("MainWindow", "Total", None, QApplication.UnicodeUTF8))
        self.label_8.setText(QApplication.translate("MainWindow", "Grand Total", None, QApplication.UnicodeUTF8))
        self.label_9.setText(QApplication.translate("MainWindow", "Round Off", None, QApplication.UnicodeUTF8))
        self.billing_print_button.setText(QApplication.translate("MainWindow", "Print", None, QApplication.UnicodeUTF8))
        self.billing_status_label.setText(
            QApplication.translate("MainWindow", "Status", None, QApplication.UnicodeUTF8))
        # self.billing_save_button.setText(QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        # self.billing_save_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+s", None, QApplication.UnicodeUTF8))
        # self.billing_print_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+p", None, QApplication.UnicodeUTF8))
        # self.billing_detail_tabWidget.setTabText(self.billing_detail_tabWidget.indexOf(self.billing_tab_1), QApplication.translate("MainWindow", "Billing", None, QApplication.UnicodeUTF8))
        ###########################################################################
        self.billtablerow_count = 0
        self.billnumber = None
        self.search = SearchMenu()
        self.bill = Search()
        self.save = SaveBill()
        self.ticket = SaveTicket()
        self.billing_print_button.clicked.connect(self.print_bill)
        # self.billing_save_button.clicked.connect(self.save_bills)
        self.billing_paid_button.clicked.connect(lambda: self.pay_bill(self.billnumber))
        self.billing_assign_button.clicked.connect(self.save_bills)
        self.billing_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.billing_total_linedit.setDisabled(True)
        self.billing_servicetax_linedit.setDisabled(True)
        self.billing_grandtotal_linedit.setDisabled(True)
        self.billing_roundoff_linedit.setDisabled(True)
        self.billing_tab_1.setFocusPolicy(Qt.StrongFocus)  ###this and next line gets the focus event
        self.billing_tab_1.focusInEvent = self.got_focus
        self.editable = True
        ###mainwidnow to access the status bar
        widgets = QApplication.topLevelWidgets()
        self.mainwindow, = [i for i in widgets if type(i).__name__ == 'QMainWindow']
        # self.add_new_row()
        # self.mainwindow.billing_table.cellChanged.connect(self.process_amount)
        ############################################################################
        if args:
            self.editable = False
            self.billnumber = args[0]
            self.load_rows(self.billnumber)
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """
        assigns the shortcut for the buttons
        :return: none
        """
        try:
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_pay']),
                      self.billing_tab_1, lambda: self.pay_bill(self.billnumber))
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_save']),
                      self.billing_tab_1, self.save_bills)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_print']),
                      self.billing_tab_1, self.print_bill)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def assign_credit(self):
        """
        Assigns credit to a customer
        :return:none
        """
        try:
            text = self.billing_assign_linedit.text()
            if not text:
                return False
            customer = text.split('-')
            customercode = customer[0]
            result = self.save.assign_bill(customercode=customercode, billid=self.billnumber)
            if result[0]:
                QMessageBox.information(QMessageBox(), 'Success', result[1], QMessageBox.Ok)
            else:
                QMessageBox.critical(QMessageBox(), 'Error', result[1], QMessageBox.Ok)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_new_row(self, *args):
        """
        Adds a new row to the billing module
        """
        try:
            table = self.billing_table
            if args:
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args[0]))
                for j, i in enumerate(args[0]):
                    item = QTableWidgetItem(i['item_no'])
                    # item.setFlags(item.flags() and not Qt.ItemIsEditable)
                    table.setItem(j, 0, item)
                    item = QTableWidgetItem(i['item'])
                    # item.setFlags(item.flags() and not Qt.ItemIsEditable)
                    table.setItem(j, 1, item)
                    item = QTableWidgetItem(i['rate'])
                    # item.setFlags(item.flags() and not Qt.ItemIsEditable)
                    table.setItem(j, 2, item)
                    item = QTableWidgetItem(i['quantity'])
                    # item.setFlags(item.flags() and not Qt.ItemIsEditable)
                    table.setItem(j, 3, item)
                    item = QTableWidgetItem(i['amount'])
                    # item.setFlags(item.flags() and not Qt.ItemIsEditable)
                    table.setItem(j, 4, item)
                if args[1]:
                    i = args[1]
                    self.billing_total_linedit.setText(i['total'])
                    self.billing_tax_label.setText("Service Tax @" + i['tax'])
                    self.billing_servicetax_linedit.setText(i['tax_amount'])
                    self.billing_roundoff_linedit.setText(i['roundoff'])
                    self.billing_grandtotal_linedit.setText(i['grand'])
                    self.billing_status_label.setText(str(i['state'] + ' id:' + str(self.billnumber)).title())
                    if i['state'] == 'paid':
                        self.billing_status_label.setStyleSheet("QLabel { color : green; }")
                        self.billing_assign_linedit.setDisabled(True)
                    else:
                        self.billing_status_label.setStyleSheet("QLabel { color : #FF0000; }")
                    self.billing_assign_linedit.search_customer_id(i['customer'])
            elif self.editable:
                ######################################
                self.billtablerow_count = self.billing_table.rowCount() + 1
                table.setRowCount(self.billtablerow_count)
                itemfield = QLineEdit()
                completer = QCompleter()
                completer.popup().setStyleSheet("background-color: #4B77BE;")
                itemfield.setCompleter(completer)
                model = QStringListModel()
                completer.setModel(model)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
                completer.setWrapAround(False)
                itemfield.connect(SIGNAL('updatedtext'), self.get_menuitem)
                itemfield.textChanged.connect(
                    lambda: itemfield.emit(SIGNAL("updatedtext"), model, itemfield.text(), itemfield))
                row = table.rowCount()
                itemfield.editingFinished.connect(lambda: self.get_rate(itemfield.text(), row))
                itemfield.setAlignment(Qt.AlignCenter)
                #########################################
                quantityfield = QLineEdit()
                quantityfield.setValidator(QIntValidator(0, 999))
                quantityfield.setAlignment(Qt.AlignRight)
                quantityfield.editingFinished.connect(lambda who=row: self.process_total(who))
                itemcode = QLineEdit()
                itemcode.editingFinished.connect(lambda: self.get_id(itemcode, itemfield))
                table.setCellWidget(self.billtablerow_count - 1, 0, itemcode)
                table.setCellWidget(self.billtablerow_count - 1, 1, itemfield)
                item = QTableWidgetItem()
                item.setFlags(item.flags() and not Qt.ItemIsEditable)
                table.setItem(self.billtablerow_count - 1, 2, item)
                # self.mainwindow.billing_table.setCellWidget(self.billtablerow_count - 1, 1, QLabel())
                # self.mainwindow.billing_table.setCellWidget(self.billtablerow_count - 1, 2, QLabel())
                table.setCellWidget(self.billtablerow_count - 1, 3, quantityfield)
                item = QTableWidgetItem()
                item.setFlags(item.flags() and not Qt.ItemIsEditable)
                table.setItem(self.billtablerow_count - 1, 4, item)
                # self.mainwindow.billing_table.setCellWidget(self.billtablerow_count - 1, 4, QLabel())
                # itemcode.setFocusPolicy(Qt.StrongFocus)
                # itemcode.setFocus()
                # self.set_focus_linedit()
            else:
                pass

            table.setColumnWidth(0, ((table.width() * 3) / 40))
            table.setColumnWidth(1, ((table.width() * 9) / 20))
            table.setColumnWidth(2, ((table.width() * 0.8) / 5))
            table.setColumnWidth(3, ((table.width() * 4) / 40))
            # table.setColumnWidth(4, table.width() / 5)
            self.billing_table.horizontalHeader().setStretchLastSection(True)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def check_available(self, row):
        """method to check if the particular product is available"""
        quantity_line = self.billing_table.cellWidget(row - 1, 3)
        dish_line = self.billing_table.cellWidget(
            row - 1, 1) if self.billing_table.cellWidget(
            row - 1, 1) else self.billing_table.item(row - 1, 1)
        item = self.billing_table.cellWidget(row - 1, 4)
        quantity = int(quantity_line.text()) if quantity_line.text() else 0
        dish = dish_line.text()
        counter = self.ticket.get_availability(dish=dish)
        if counter < quantity:
            msg = QMessageBox.critical(QMessageBox(), 'Warning',
                'The Dish is not Available please check the Inventory and confirm',
                QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Ignore)
            if msg == QMessageBox.Cancel:
                quantity_line.setText('0')
            elif msg == QMessageBox.Ignore:
                confirm = QMessageBox.critical(QMessageBox(), 'Warning',
                    'This will ignore Further Availability message,Are you sure?',
                    QMessageBox.Ok | QMessageBox.Cancel)
                if confirm == QMessageBox.Ok:
                    settings.available_check = False
                    settings.set_settings()
            QTimer.singleShot(0, item.setFocus)
            item.setFocus()

    def auto_capital(self, linedit):
        """
        capitalizes the line in the linedit
        :param linedit: the linedit object to be modified
        :return: none
        """
        try:
            edit = linedit
            text = edit.text()
            edit.setText(text.title())
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_id(self, codefield, itemfield):
        """
        gets the data corresponding to the code
        :param codefield:the code field
        :param itemfield:the item field
        :return:none
        """
        try:
            code = codefield.text()
            item = self.search.search_id(code)
            itemfield.setText(item)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_menuitem(self, *args):
        """
        searches/gets the menu item
        :param args:the list of data
        :return:none
        """
        try:
            if len(args[1]) == 1:
                self.auto_capital(args[2])
            if len(args[1]) == 3:
                menulist = self.search.search_item(item=args[1])
                newmodel = args[0]
                count = newmodel.rowCount()
                newmodel.removeRows(0, count)
                newmodel.setStringList(menulist)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_rate(self, item, where):
        """
        gets the rate of the items
        :param item:the item
        :param where:the row
        :return:none
        """
        try:
            rate, code = self.search.search_rate(item)
            item = QTableWidgetItem(str(rate))
            item.setFlags(item.flags() and not Qt.ItemIsEditable)
            self.billing_table.setItem(where - 1, 2, item)
            codefield = QLineEdit()  # todo had to avoid due to focus issues
            codefield.setText(str(code))
            itemfield = self.billing_table.cellWidget(where - 1, 1)
            codefield.editingFinished.connect(lambda: self.get_id(codefield, itemfield))
            self.billing_table.setCellWidget(where - 1, 0, codefield)
            self.check_and_add_row()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def delete_unwanted_row(self):
        """
        deletes unwanted row
        :return:None
        """
        leav = False
        try:
            while True:
                for i in range(self.billing_table.rowCount()):
                    val = self.billing_table.cellWidget(i, 3).text()
                    if str(val) == '0' or str(val) == '':
                        self.billing_table.removeRow(i)
                        break
                    elif i == self.billing_table.rowCount() - 1:
                        leav = True
                    else:
                        pass
                if leav:
                    break
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def print_bill(self):
        """
        prints the bill
        """
        logger.info('NewTab bill printing initiated')
        try:
            text = self.billing_status_label.text()
            if text == 'Status':
                status = self.save_bills()
                if status:
                    pass
                else:
                    msg = QMessageBox.critical(QMessageBox(), 'Error!!', 'The Bill was not saved', QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        return False
            dialog = QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                p = dialog.printer()
                dataobj = self.get_data()
                if dataobj:
                    printing = PrintNow(p.printerName(), dataobj, 'bill')
                    printing.start_print()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def process_total(self, who=None):
        """
        process the total of the bills
        :param who:the row number
        :return: none
        """
        try:
            if who == None:
                who = self.billing_table.rowCount()
            self.process_amount(who)
            row = self.billing_table.rowCount()
            value = 0
            for i in range(row):
                val = self.billing_table.item(i, 4)
                if val is not None:
                    try:
                        value += int(self.billing_table.item(i, 4).text())
                    except Exception as _:
                        break
            self.billing_total_linedit.setText(str(value))
            tax = self.search.get_tax()
            self.billing_tax_label.setText("Service Tax @" + tax.to_eng())
            self.billing_servicetax_linedit.setText(str(((value * tax) / 100)))
            total = str(value + ((value * tax) / 100))
            round_off_value = Decimal(total) - int(Decimal(total))
            roundoff = str(Decimal(Decimal(1) - round_off_value).quantize(
            Decimal('1.00'))) if round_off_value else str(Decimal(0).quantize(Decimal('1.00')))
            self.billing_roundoff_linedit.setText(roundoff)
            self.billing_grandtotal_linedit.setText(str(Decimal(total) + Decimal(roundoff)))
            if settings.available_check:
                self.check_available(row=who)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def check_and_add_row(self):
        """
        if the last row is empty then dont add a new row
        """
        row = self.billing_table.rowCount()
        lastrow = row - 1
        try:
            val = self.billing_table.cellWidget(lastrow, 0).text()
            if str(val):
                self.add_new_row()
            else:
                pass
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def process_amount(self, row):
        """
        process the amount after quantity is pressed,
        the column number is hardcoded
        """
        try:
            row_position = row - 1
            val1 = self.billing_table.cellWidget(row_position, 3).text()
            val2 = self.billing_table.item(row_position, 2).text()
            multiplier = int(val1 if val1 != '' else 0)
            multiplicant = int(val2)
            if multiplier is not None and multiplicant is not None:
                val = multiplicant * multiplier
                value = QTableWidgetItem(str(val))
                value.setFlags(value.flags() and not Qt.ItemIsEditable)
                self.billing_table.setItem(row_position, 4, value)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def got_focus(self, event):
        """
        gets focus of the tab
        :param event:event function
        :return:adds a new row to align properly
        """
        try:
            count = self.billing_table.rowCount()
            if count == 0:
                self.add_new_row()
                widget = self.billing_table.cellWidget(0, 0)
                QTimer.singleShot(0, widget.setFocus)
            elif not self.editable:  # required to arrange the spacing
                self.add_new_row()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_rows(self, *args):
        """
        load rows with the details of bill with billnumber
        :return:none
        """
        try:
            billlist = self.bill.select_bill(args[0])
            self.add_new_row(*billlist)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def save_bills(self):
        """
        saves the bills and changes its status
        :return:none
        """
        try:
            status = self.mainwindow.statusBar()
            status.setStyleSheet('color:red;')
            status.showMessage('System Info|Please Wait')
            QCoreApplication.processEvents()  # very important to repaint
            dataobj = self.get_data()
            if not self.billnumber:
                if dataobj:
                    data = self.save.save_new_bill(dataobj[0])
                    if data:
                        self.billing_status_label.setText(str(data[1]).title() + " Id:" + data[0])
                        self.billing_status_label.setStyleSheet("QLabel { color : #FF0000; }")
                        self.billnumber = data[0]
                        self.load_rows(self.billnumber)
                        msg = QMessageBox.information(QMessageBox(), 'Success', 'The Bill was saved', QMessageBox.Ok)
                        if msg == QMessageBox.Ok:
                            self.assign_credit()
                            status.clearMessage()
                            return True
            self.assign_credit()
            status.clearMessage()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def pay_bill(self, id):
        """
        :param id: bill number
        :return:status of the bill
        """
        try:
            newid = id
            if not newid:
                self.show_error('Save')
            else:
                status = self.save.pay_bill(newid)
                if status:
                    self.billing_status_label.setText(str(status + " id:" + str(newid)).title())
                    self.billing_status_label.setStyleSheet("QLabel { color : green; }")
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_data(self):
        """
        fetches all the data for printing
        :return:list of dictionary
        """
        try:
            table = self.billing_table
            rows = table.rowCount()
            dataobj = []
            lines = []
            for i in range(rows):
                dictionary = {}
                item = table.cellWidget(i, 0) if table.cellWidget(i, 0) is not None else table.item(i, 0)
                dictionary['id'] = item.text()
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['item'] = item.text()
                if dictionary['item'] == '' and dictionary['id'] == '':
                    continue
                elif dictionary['item'] == '':
                    self.show_error('Item')
                    return False
                item = table.cellWidget(i, 2) if table.cellWidget(i, 2) is not None else table.item(i, 2)
                dictionary['rate'] = item.text()
                item = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
                dictionary['quantity'] = item.text()
                if dictionary['quantity'] == '':
                    self.show_error('Quantity')
                    return False
                if dictionary['quantity'] == '0':
                    continue
                item = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
                dictionary['amount'] = item.text()
                lines.append(dictionary)
            if lines == []:
                self.show_error('Data')
                return False
            lines = self.aggregate_dishes(lines)
            dataobj.append(lines)
            dictionary = {}
            dictionary['status'] = self.billing_status_label.text().split()[0]
            dictionary['total'] = self.billing_total_linedit.text()
            dictionary['tax'] = self.billing_tax_label.text()
            dictionary['tax_amount'] = self.billing_servicetax_linedit.text()
            dictionary['roundoff'] = self.billing_roundoff_linedit.text()
            dictionary['grand'] = self.billing_grandtotal_linedit.text()
            if self.billnumber:
                dictionary['bill_number'] = self.billnumber
            dataobj.append(dictionary)
            return dataobj
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def aggregate_dishes(self, data):
        """
        adds the quantity of the repeated dishes
        :param data:list of dictionary
        :return:list of dictionary
        """
        try:
            data = data
            quantitydict = {}  # quantitydict['id']=(item,rate,quantity,amount)
            for i in data:
                if quantitydict.get(i['id']):
                    qd = quantitydict[i['id']]
                    item = qd[0]
                    rate = qd[1]
                    quantity = int(qd[2])
                    amount = qd[3]
                    quantitydict[i['id']] = (
                        item, rate + i['rate'], quantity + int(i['quantity']), amount + i['amount'])
                else:
                    quantitydict[i['id']] = (i['item'], i['rate'], i['quantity'], i['amount'])
            line = []
            for i, j in quantitydict.iteritems():
                dummydict = {}
                dummydict['id'] = i
                dummydict['item'] = j[0]
                dummydict['rate'] = j[1]
                dummydict['quantity'] = str(j[2])
                dummydict['amount'] = j[3]
                line.append(dummydict)
            return line
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def show_error(self, text):
        """
        :return: pops up an error
        """
        try:
            QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class SearchTicket():
    """Searches the ticket and get details"""
    global logger

    def __init__(self, parenttab):
        #######
        logger.info('Inside SearchTicket')
        self.parenttab = parenttab
        self.ticket_main_tab = QWidget()
        self.ticket_main_tab.setObjectName("ticket_main_tab")
        self.gridLayout_25 = QGridLayout(self.ticket_main_tab)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_15 = QLabel(self.ticket_main_tab)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_10.addWidget(self.label_15)
        self.tickets_ticketno_linedit = QLineEdit(self.ticket_main_tab)
        self.tickets_ticketno_linedit.setObjectName("tickets_ticketno_linedit")
        self.horizontalLayout_10.addWidget(self.tickets_ticketno_linedit)
        self.label_16 = QLabel(self.ticket_main_tab)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_10.addWidget(self.label_16)
        self.tickets_fromdate_dateedit = QDateEdit(self.ticket_main_tab)
        self.tickets_fromdate_dateedit.setCalendarPopup(True)
        self.tickets_fromdate_dateedit.setObjectName("tickets_fromdate_dateedit")
        self.horizontalLayout_10.addWidget(self.tickets_fromdate_dateedit)
        self.label_17 = QLabel(self.ticket_main_tab)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_10.addWidget(self.label_17)
        self.tickets_todate_dateedit = QDateEdit(self.ticket_main_tab)
        self.tickets_todate_dateedit.setCalendarPopup(True)
        self.tickets_todate_dateedit.setObjectName("tickets_todate_dateedit")
        self.horizontalLayout_10.addWidget(self.tickets_todate_dateedit)
        self.tickets_search_button = QPushButton(self.ticket_main_tab)
        self.tickets_search_button.setObjectName("tickets_search_button")
        self.horizontalLayout_10.addWidget(self.tickets_search_button)
        self.gridLayout_25.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)
        self.tickets_table = QTableWidget(self.ticket_main_tab)
        self.tickets_table.setObjectName("tickets_table")
        self.tickets_table.setColumnCount(3)
        self.tickets_table.setRowCount(0)
        self.tickets_table.setSortingEnabled(True)
        item = QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tickets_table.setHorizontalHeaderItem(2, item)
        self.tickets_table.horizontalHeader().setCascadingSectionResizes(True)
        self.tickets_table.horizontalHeader().setStretchLastSection(True)
        self.tickets_table.verticalHeader().setVisible(False)
        self.tickets_table.verticalHeader().setCascadingSectionResizes(True)
        self.tickets_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_25.addWidget(self.tickets_table, 1, 0, 1, 1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.tickets_newticket_button = QPushButton(self.ticket_main_tab)
        self.tickets_newticket_button.setObjectName("tickets_newticket_button")
        self.horizontalLayout_11.addWidget(self.tickets_newticket_button)
        spacerItem14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem14)
        self.tickets_reset_button = QPushButton(self.ticket_main_tab)
        self.tickets_reset_button.setObjectName("tickets_reset_button")
        self.horizontalLayout_11.addWidget(self.tickets_reset_button)
        self.gridLayout_25.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        #####retranslate
        self.label_15.setText(
            QApplication.translate("MainWindow", "Bill No", None, QApplication.UnicodeUTF8))
        self.tickets_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.label_16.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.tickets_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.label_17.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.tickets_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.tickets_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Ticket Number", None, QApplication.UnicodeUTF8))
        self.tickets_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.tickets_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Table Number", None, QApplication.UnicodeUTF8))
        self.tickets_newticket_button.setText(
            QApplication.translate("MainWindow", "New Ticket", None, QApplication.UnicodeUTF8))
        self.tickets_reset_button.setText(
            QApplication.translate("MainWindow", "Reset Search", None, QApplication.UnicodeUTF8))
        self.tickets_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        # self.tickets_search_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+Shift+E", None, QApplication.UnicodeUTF8))
        ####signals and slots && other stuffs
        self.ticket_main_tab.setFocusPolicy(Qt.StrongFocus)
        self.ticket_main_tab.focusInEvent = self.change_focus
        self.ticket_search = Search()
        # self.tickets_newticket_button.clicked = self.add_new_tab
        self.tickets_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tickets_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tickets_table.setShowGrid(False)
        self.tickets_search_button.clicked.connect(self.search_bill)
        self.tickets_reset_button.clicked.connect(self.reset_all)
        self.tickets_newticket_button.clicked.connect(self.add_new_tab)
        self.tickets_table.itemDoubleClicked.connect(self.find_ticket_and_add_tab)
        self.tickets_todate_dateedit.setMaximumDate(QDate.currentDate())
        self.tickets_todate_dateedit.setDate(QDate.currentDate())
        today = datetime.today()
        fewdaysback = today - timedelta(days=15)
        self.tickets_fromdate_dateedit.setDate(QDate.fromString(fewdaysback.strftime('%d/%m/%Y'), 'dd/MM/yyyy'))
        # self.assign_shortcuts()

    def assign_shortcuts(self):
        """
        assigns shortcuts to buttons
        :return:none
        """
        try:
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingtickets_newbill']),
                      self.ticket_main_tab, self.add_new_tab)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingtickets_reset']),
                      self.ticket_main_tab, self.reset_all)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingtickets_search']),
                      self.ticket_main_tab, self.search_bill)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingtickets_selectbill']),
                      self.ticket_main_tab, self.row_selected)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def row_selected(self):
        """
        checks the selected row and opens the new tab, equivalent to double click on row
        :return: nope
        """
        try:
            rows = sorted(set(index.row() for index in
                              self.tickets_table.selectedIndexes()))
            if rows:
                self.add_new_tab(int(self.tickets_table.item(rows[0], 0).text()))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def find_ticket_and_add_tab(self, item):
        """
        finds the bill number of the row and add it to the tab
        :param item: item clicked
        :return:none
        """
        try:
            model_index = self.tickets_table.indexFromItem(item)
            row = model_index.row()
            bill_no_item = self.tickets_table.item(row, 0)
            self.add_new_tab(int(bill_no_item.text()))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_new_tab(self, *args):
        """
        adds a new tab
        :param args:bill number and other texts
        :return:none
        """
        try:
            logger.info('SearchTicket new tab adding initiated')
            tab_name = u"Ticket(&%s)" % self.parenttab.count()
            if not args:
                tab = TicketTab()
            else:
                tab = TicketTab(*args)
                tab_name = u"Ticket:&%s" % tab.billnumber
            count = self.parenttab.addTab(tab.ticket_tab_1, tab_name)
            self.parenttab.setCurrentIndex(count)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_bill(self):
        """
        :return:search the tickets and add them in the bill list table
        """
        try:
            logger.info('SearchTicket ticket searching initiated')
            self.tickets_table.clearContents()
            ticket_number = self.tickets_ticketno_linedit.text()
            from_date = self.tickets_fromdate_dateedit.date()
            from_date = from_date.toString('yyyy-MM-dd')
            to_date = self.tickets_todate_dateedit.date()
            to_date = to_date.toString('yyyy-MM-dd')
            bill_list = self.ticket_search.search_tickets(ticket_no=ticket_number, from_date=from_date, to_date=to_date)
            self.load_rows(*bill_list)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def reset_all(self):
        """
        :return: resets the the data in the search text
        """
        try:
            self.tickets_ticketno_linedit.clear()
            self.tickets_table.clearContents()
            self.tickets_table.setRowCount(0)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_rows(self, *args):
        """
        :param args: the list of data
        :return:loads the rows with the list of tickets
        """
        try:
            if args:
                self.tickets_table.setRowCount(len(args))

            table = self.tickets_table
            for j, i in enumerate(args):
                item = QTableWidgetItem(i['ticket_no'])
                table.setItem(j, 0, item)
                item = QTableWidgetItem(i['date'])
                table.setItem(j, 1, item)
                item = QTableWidgetItem(i['table_no'])
                table.setItem(j, 2, item)
            table.setColumnWidth(0, (table.width() / 3))
            table.setColumnWidth(1, (table.width() / 3))
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def change_focus(self, event):
        """
        :return:just had to use this because clicks were not working
        """
        try:
            self.load_rows()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class TicketTab():
    """Tab to create new Ticket"""
    global logger

    def __init__(self, *args):
        logger.info('Inside TicketTab')
        self.ticket_tab_1 = QWidget()
        self.ticket_tab_1.setStyleSheet("")
        self.ticket_tab_1.setObjectName("ticket_tab_1")
        self.gridLayout_13 = QGridLayout(self.ticket_tab_1)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.ticket_table = QTableWidget(self.ticket_tab_1)
        self.ticket_table.setObjectName("ticket_table")
        self.ticket_table.setColumnCount(4)
        self.ticket_table.setRowCount(0)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(3, item)
        self.ticket_table.horizontalHeader().setCascadingSectionResizes(True)
        self.ticket_table.horizontalHeader().setStretchLastSection(True)
        self.ticket_table.verticalHeader().setVisible(True)
        self.ticket_table.verticalHeader().setCascadingSectionResizes(True)
        self.ticket_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_13.addWidget(self.ticket_table, 0, 0, 1, 1)
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.ticket_invoice_label = QLabel(self.ticket_tab_1)
        self.ticket_invoice_label.setObjectName('ticket_invoice_label')
        self.gridLayout_12.addWidget(self.ticket_invoice_label, 0, 0, 1, 1)
        self.ticket_invoiceline = QLineEdit(self.ticket_tab_1)
        self.ticket_invoiceline.setObjectName('ticket_invoiceline')
        self.gridLayout_12.addWidget(self.ticket_invoiceline, 0, 1, 1, 1)
        # self.billing_assign_linedit = CustomerSearch(self.ticket_tab_1)
        # self.billing_assign_linedit.setObjectName('billing_assign_linedit')
        # self.billing_assign_linedit.setPlaceholderText('Credit Customer')
        # self.gridLayout_12.addWidget(self.billing_assign_linedit, 0, 0, 1, 1)
        # spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.gridLayout_12.addItem(spacerItem18, 0, 2, 1, 1)
        self.table_label = QLabel(self.ticket_tab_1)
        self.table_label.setObjectName('table_label')
        self.gridLayout_12.addWidget(self.table_label, 0, 2, 1, 1)
        self.table_numberline = QLineEdit(self.ticket_tab_1)
        self.table_numberline.setText("0")
        self.table_numberline.setObjectName('table_numberline')
        self.gridLayout_12.addWidget(self.table_numberline, 0, 3, 1, 1)
        # self.label_6 = QLabel(self.ticket_tab_1)
        # self.label_6.setObjectName("label_6")
        # self.gridLayout_12.addWidget(self.label_6, 0, 3, 1, 1)
        # self.billing_total_linedit = QLineEdit(self.ticket_tab_1)
        # self.billing_total_linedit.setObjectName("billing_total_linedit")
        # self.gridLayout_12.addWidget(self.billing_total_linedit, 0, 4, 1, 1)
        self.ticket_status_label = QLabel(self.ticket_tab_1)
        self.ticket_status_label.setObjectName("ticket_status_label")
        self.gridLayout_12.addWidget(self.ticket_status_label, 1, 0, 1, 1)
        self.ticket_cancelbutton = QPushButton(self.ticket_tab_1)
        self.ticket_cancelbutton.setObjectName('ticket_cancelbutton')
        self.gridLayout_12.addWidget(self.ticket_cancelbutton, 1, 2, 1, 1)
        self.ticket_savebutton = QPushButton(self.ticket_tab_1)
        self.ticket_savebutton.setObjectName('ticket_savebutton')
        self.gridLayout_12.addWidget(self.ticket_savebutton, 1, 1, 1, 1)
        self.ticket_printbutton = QPushButton(self.ticket_tab_1)
        self.ticket_printbutton.setObjectName('ticket_printbutton')
        self.gridLayout_12.addWidget(self.ticket_printbutton, 1, 3, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_12, 1, 0, 1, 1)
        # self.billing_tax_label = QLabel(self.ticket_tab_1)
        # self.billing_tax_label.setObjectName("billing_tax_label")
        # self.gridLayout_12.addWidget(self.billing_tax_label, 1, 3, 1, 1)
        # self.billing_servicetax_linedit = QLineEdit(self.ticket_tab_1)
        # self.billing_servicetax_linedit.setObjectName("billing_servicetax_linedit")
        # self.gridLayout_12.addWidget(self.billing_servicetax_linedit, 1, 4, 1, 1)
        # self.label_8 = QLabel(self.ticket_tab_1)
        # self.label_8.setObjectName("label_8")
        # self.gridLayout_12.addWidget(self.label_8, 2, 3, 1, 1)
        # self.billing_grandtotal_linedit = QLineEdit(self.ticket_tab_1)
        # self.billing_grandtotal_linedit.setObjectName("billing_grandtotal_linedit")
        # self.gridLayout_12.addWidget(self.billing_grandtotal_linedit, 2, 4, 1, 1)
        # self.billing_status_label = QLabel(self.ticket_tab_1)
        # self.billing_status_label.setObjectName("billing_status_label")
        # self.gridLayout_12.addWidget(self.billing_status_label, 3, 0, 1, 1)
        # spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.gridLayout_12.addItem(spacerItem18, 3, 1, 1, 1)
        # self.billing_paid_button = QPushButton(self.ticket_tab_1)
        # self.billing_paid_button.setObjectName("billing_paid_button")
        # self.gridLayout_12.addWidget(self.billing_paid_button, 3, 2, 1, 1)
        # self.billing_save_button = QPushButton(self.ticket_tab_1)
        # self.billing_save_button.setObjectName("billing_save_button")
        # self.gridLayout_12.addWidget(self.billing_save_button, 3, 3, 1, 1)
        # self.billing_assign_button = QPushButton(self.ticket_tab_1)
        # self.billing_assign_button.setObjectName('billing_assign_button')
        # self.gridLayout_12.addWidget(self.billing_assign_button, 3, 3, 1, 1)
        # self.billing_print_button = QPushButton(self.ticket_tab_1)
        # self.billing_print_button.setObjectName("billing_print_button")
        # self.gridLayout_12.addWidget(self.billing_print_button, 3, 4, 1, 1)

        # self.billing_detail_tabWidget.addTab(self.ticket_tab_1, "")
        # please add the obj.billing_tab_! as a tab in billing_detail_tabWidget
        self.ticket_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.ticket_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.ticket_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.ticket_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Status", None, QApplication.UnicodeUTF8))
        self.ticket_invoice_label.setText(
            QApplication.translate("MainWindow", "Invoice Number", None, QApplication.UnicodeUTF8))
        self.table_label.setText(QApplication.translate("MainWindow", "Table Number", None, QApplication.UnicodeUTF8))
        self.ticket_cancelbutton.setText(QApplication.translate("MainWindow", "Cancel", None, QApplication.UnicodeUTF8))
        self.ticket_savebutton.setText(QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        self.ticket_printbutton.setText(QApplication.translate("MainWindow", "Print", None, QApplication.UnicodeUTF8))
        self.ticket_status_label.setText(QApplication.translate("MainWindow", "Status", None, QApplication.UnicodeUTF8))
        # self.billing_save_button.setText(QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        # self.billing_save_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+s", None, QApplication.UnicodeUTF8))
        # self.billing_print_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+p", None, QApplication.UnicodeUTF8))
        # self.billing_detail_tabWidget.setTabText(self.billing_detail_tabWidget.indexOf(self.ticket_tab_1), QApplication.translate("MainWindow", "Billing", None, QApplication.UnicodeUTF8))
        ###########################################################################
        self.billtablerow_count = 0
        self.billnumber = None
        self.search = SearchMenu()
        self.bill = Search()
        self.save = SaveTicket()
        self.ticket_printbutton.clicked.connect(self.print_bill)
        # self.billing_save_button.clicked.connect(self.save_bills)
        self.ticket_cancelbutton.clicked.connect(lambda: self.cancel_bill(self.billnumber))
        self.ticket_savebutton.clicked.connect(self.save_bills)
        self.ticket_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ticket_invoiceline.setDisabled(True)
        self.ticket_tab_1.setFocusPolicy(Qt.StrongFocus)  ###this and next line gets the focus event
        self.ticket_tab_1.focusInEvent = self.got_focus
        self.editable = True
        ###mainwidnow to access the status bar
        widgets = QApplication.topLevelWidgets()
        self.mainwindow, = [i for i in widgets if type(i).__name__ == 'QMainWindow']
        # self.add_new_row()
        # self.mainwindow.ticket_table.cellChanged.connect(self.process_amount)
        ############################################################################
        if args:
            self.editable = False
            self.billnumber = args[0]
            self.load_rows(self.billnumber)
            # self.assign_shortcuts()

    def assign_shortcuts(self):
        """
        assigns the shortcut for the buttons
        :return: none
        """
        try:
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_pay']),
                      self.ticket_tab_1, lambda: self.cancel_bill(self.billnumber))
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_save']),
                      self.ticket_tab_1, self.save_bills)
            QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_billingedit_print']),
                      self.ticket_tab_1, self.print_bill)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def add_new_row(self, *args):
        """
        Adds a new row to the billing module
        """
        try:
            table = self.ticket_table
            if args:
                if args[0]:
                    table.clearContents()
                    table.setRowCount(0)
                    table.setRowCount(len(args[0]))
                    for j, i in enumerate(args[0]):
                        item = QTableWidgetItem(i['item_no'])
                        table.setItem(j, 0, item)
                        item = QTableWidgetItem(i['item'])
                        table.setItem(j, 1, item)
                        quantityfield = QLineEdit()
                        row = table.rowCount()
                        quantityfield.editingFinished.connect(
                            lambda row=row: self.check_available(row=row))
                        quantityfield.setText(str(i['quantity']))
                        table.setCellWidget(j, 2, quantityfield)
                        statecombo = QComboBox()
                        self.fill_item_list(statecombo, i['state'])
                        table.setCellWidget(j, 3, statecombo)
                if args[1]:
                    self.ticket_invoiceline.setText(str(args[1]['invoice']))
                    self.ticket_status_label.setText('{0} Id:{1}'.format(args[1]['state'].title(), self.billnumber))
                    if args[1]['state'] == 'done':
                        self.ticket_status_label.setStyleSheet("QLabel { color : green; }")
                    else:
                        self.ticket_status_label.setStyleSheet("QLabel { color : #FF0000; }")
                    self.table_numberline.setText(str(args[1]['table_no']))
            elif self.editable:
                ######################################
                self.billtablerow_count = self.ticket_table.rowCount() + 1
                table.setRowCount(self.billtablerow_count)
                itemfield = QLineEdit()
                completer = QCompleter()
                completer.popup().setStyleSheet("background-color: #4B77BE;")
                itemfield.setCompleter(completer)
                model = QStringListModel()
                completer.setModel(model)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
                completer.setWrapAround(False)
                itemfield.connect(SIGNAL('updatedtext'), self.get_menuitem)
                itemfield.textChanged.connect(
                    lambda: itemfield.emit(SIGNAL("updatedtext"), model, itemfield.text(), itemfield))
                itemfield.setAlignment(Qt.AlignCenter)
                row = table.rowCount()
                itemfield.editingFinished.connect(lambda row=row: self.search_dish(row))
                statecombo = QComboBox()
                self.fill_item_list(statecombo)
                #########################################
                itemcode = QLineEdit()
                itemcode.editingFinished.connect(lambda: self.get_id(itemcode, itemfield))
                table.setCellWidget(self.billtablerow_count - 1, 0, itemcode)
                table.setCellWidget(self.billtablerow_count - 1, 1, itemfield)
                quantityfield = QLineEdit()
                quantityfield.editingFinished.connect(
                    lambda row=row: self.check_available(row=row))
                table.setCellWidget(self.billtablerow_count - 1, 2, quantityfield)
                table.setCellWidget(self.billtablerow_count - 1, 3, statecombo)
            else:
                pass

            table.setColumnWidth(0, (table.width() / 7))
            table.setColumnWidth(1, (table.width() / 2))
            table.horizontalHeader().setStretchLastSection(True)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def auto_capital(self, linedit):
        """
        capitalizes the line in the linedit
        :param linedit: the linedit object to be modified
        :return: none
        """
        try:
            edit = linedit
            text = edit.text()
            edit.setText(text.title())
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_id(self, codefield, itemfield):
        """
        gets the data corresponding to the code
        :param codefield:the code field
        :param itemfield:the item field
        :return:none
        """
        try:
            code = codefield.text()
            item = self.search.search_id(code)
            itemfield.setText(item)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_dish(self, row):
        """Searches dish"""
        line = self.ticket_table.cellWidget(row - 1, 0)
        item = self.ticket_table.cellWidget(row - 1, 1).text()
        code = self.search.search_dish(item)
        line.setText(code) if code else ''
        self.check_and_add_row()

    def get_menuitem(self, *args):
        """
        searches/gets the menu item
        :param args:the list of data
        :return:none
        """
        try:
            if len(args[1]) == 1:
                self.auto_capital(args[2])
            if len(args[1]) == 3:
                menulist = self.search.search_item(item=args[1])
                newmodel = args[0]
                count = newmodel.rowCount()
                newmodel.removeRows(0, count)
                newmodel.setStringList(menulist)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def fill_item_list(self, combo, state=None):
        """fills the item list with states"""
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        itemfield.addItems(['Processing', 'Cancel', 'Rejected'])
        if state:
            if state == 'done':
                itemfield.addItem(state.title())
            index = itemfield.findText(state.title())
            itemfield.setCurrentIndex(index)

    def check_available(self, row):
        """check if the product is available"""
        if settings.available_check:
            quantity_line = self.ticket_table.cellWidget(row - 1, 2)
            dish_line = self.ticket_table.cellWidget(
                row - 1, 1) if self.ticket_table.cellWidget(
                row - 1, 1) else self.ticket_table.item(row - 1, 1)
            combo = self.ticket_table.cellWidget(row - 1, 3)
            quantity = int(quantity_line.text()) if quantity_line.text() else 0
            dish = dish_line.text()
            counter = self.save.get_availability(dish=dish)
            if counter < quantity:
                msg = QMessageBox.critical(QMessageBox(), 'Warning',
                    'The Dish is not Available please check the Inventory and confirm',
                    QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Ignore)
                if msg == QMessageBox.Cancel:
                    quantity_line.setText('0')
                elif msg == QMessageBox.Ignore:
                    confirm = QMessageBox.critical(QMessageBox(), 'Warning',
                        'This will ignore Further Availability message,Are you sure?',
                        QMessageBox.Ok | QMessageBox.Cancel)
                    if confirm == QMessageBox.Ok:
                        settings.available_check = False
                        settings.set_settings()
                QTimer.singleShot(0, combo.setFocus)
                combo.setFocus()

    def delete_unwanted_row(self):
        """
        deletes unwanted row
        :return:None
        """
        leav = False
        try:
            while True:
                for i in range(self.ticket_table.rowCount()):
                    val = self.ticket_table.cellWidget(i, 3).text()
                    if str(val) == '0' or str(val) == '':
                        self.ticket_table.removeRow(i)
                        break
                    elif i == self.ticket_table.rowCount() - 1:
                        leav = True
                    else:
                        pass
                if leav:
                    break
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def print_bill(self):
        """
        prints the bill
        """
        logger.info('NewTab bill printing initiated')
        try:
            text = self.ticket_status_label.text()
            if text == 'Status':
                status = self.save_bills()
                if status:
                    pass
                else:
                    msg = QMessageBox.critical(QMessageBox(parent=self.ticket_tab_1), 'Error!!',
                                               'The Ticket was not saved', QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        return False
            dialog = QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                p = dialog.printer()
                data = self.get_data()
                meta = {'table_no': self.table_numberline.text(), 'ticket_no': self.billnumber}
                dataobj = [data, meta]
                if dataobj:
                    printing = PrintNow(p.printerName(), dataobj, 'ticket')
                    printing.start_print()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def check_and_add_row(self):
        """
        if the last row is empty then dont add a new row
        """
        row = self.ticket_table.rowCount()
        lastrow = row - 1
        try:
            val = self.ticket_table.cellWidget(lastrow, 0).text()
            if str(val):
                self.add_new_row()
            else:
                pass
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def got_focus(self, event):
        """
        gets focus of the tab
        :param event:event function
        :return:adds a new row to align properly
        """
        try:
            count = self.ticket_table.rowCount()
            if count == 0:
                self.add_new_row()
                widget = self.ticket_table.cellWidget(0, 0)
                QTimer.singleShot(0, widget.setFocus)
            elif not self.editable:  # required to arrange the spacing
                self.add_new_row()
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_rows(self, *args):
        """
        load rows with the details of bill with billnumber
        :return:none
        """
        try:
            billlist = self.bill.select_ticket(args[0])
            self.add_new_row(*billlist)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def save_bills(self):
        """
        saves the bills and changes its status
        :return:none
        """
        try:
            status = self.mainwindow.statusBar()
            status.setStyleSheet('color:red;')
            status.showMessage('System Info|Please Wait')
            QCoreApplication.processEvents()  # very important to repaint
            dataobj = self.get_data()
            if dataobj:
                table_number = self.table_numberline.text()
                if not table_number:
                    self.show_error('Table number')
                    return False
                if not self.billnumber:
                    data = self.save.save_ticket(dataobj, table_number=table_number)
                else:
                    data = self.save.save_ticket(dataobj, ticket_number=self.billnumber, table_number=table_number)
                if data[0]:
                    self.ticket_status_label.setText('{0} Id:{1}'.format(data[1].title(), data[0]))
                    self.ticket_invoiceline.setText(str(data[2]))
                    self.ticket_status_label.setStyleSheet("QLabel { color : #FF0000; }")
                    self.billnumber = data[0]
                    self.load_rows(self.billnumber)
                    QMessageBox.information(QMessageBox(),
                        'Success', 'The Ticket was saved', QMessageBox.Ok)
                else:
                    QMessageBox.critical(QMessageBox(),
                        'Failed', data[1], QMessageBox.Ok)
            status.clearMessage()
            return True
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def cancel_bill(self, newid):
        """
        cancels the bills
        :param id: bill number
        :return:status of the bill
        """
        try:
            if not newid:
                self.show_error('Save')
            else:
                status = self.save.cancel_ticket(newid)
                if status[0]:
                    self.ticket_status_label.setText('{0} Id:{1}'.format(status[0].title(), newid))
                    self.ticket_status_label.setStyleSheet("QLabel { color : red; }")
                    QMessageBox.information(QMessageBox(),
                        'Cancel', status[1], QMessageBox.Ok)
                    self.load_rows(newid)
                else:
                    QMessageBox.critical(QMessageBox(),
                        'Cancel', status[1], QMessageBox.Ok)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_data(self):
        """
        fetches all the data for printing
        :return:list of dictionary
        """
        try:
            table = self.ticket_table
            rows = table.rowCount()
            lines = []
            for i in range(rows):
                dictionary = {}
                item = table.cellWidget(i, 0) if table.cellWidget(i, 0) is not None else table.item(i, 0)
                dictionary['id'] = item.text()
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['item'] = item.text()
                if dictionary['item'] == '' and dictionary['id'] == '':
                    continue
                elif dictionary['item'] == '':
                    self.show_error('Item')
                    return False
                item = table.cellWidget(i, 2) if table.cellWidget(i, 2) is not None else table.item(i, 2)
                dictionary['quantity'] = item.text()
                if dictionary['quantity'] == '':
                    self.show_error('Quantity')
                    return False
                if dictionary['quantity'] == '0':
                    continue
                state = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
                dictionary['state'] = state.currentText().lower()
                lines.append(dictionary)
            if lines == []:
                self.show_error('Data')
                return False
            lines = self.aggregate_dishes(lines)
            return lines
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def aggregate_dishes(self, data):
        """
        adds the quantity of the repeated dishes
        :param data:list of dictionary
        :return:list of dictionary
        """
        try:
            data = data
            quantitydict = {}  # quantitydict['id']=(item,quantity,state)
            for i in data:
                if quantitydict.get(i['id']):
                    qd = quantitydict[i['id']]
                    item = qd[0]
                    quantity = int(qd[1])
                    quantitydict[i['id']] = (item, quantity + int(i['quantity']), i['state'])
                else:
                    quantitydict[i['id']] = (i['item'], i['quantity'], i['state'])
            line = []
            for i, j in quantitydict.iteritems():
                dummydict = {}
                dummydict['id'] = i
                dummydict['item'] = j[0]
                dummydict['quantity'] = str(j[1])
                dummydict['state'] = j[2]
                line.append(dummydict)
            return line
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def show_error(self, text):
        """
        :return: pops up an error
        """
        try:
            QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class TicketBill(QDialog):
    """Dialog to create bills out of tickets"""
    global logger

    def __init__(self, parenttab):
        QDialog.__init__(self)
        logger.info('Inside TicketBill')
        self.setWindowTitle("Add Tickets")
        self.parent = parenttab
        self.gridLayout_13 = QGridLayout(self)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.ticket_table = QTableWidget(self)
        self.ticket_table.setObjectName("ticket_table")
        self.ticket_table.setColumnCount(3)
        self.ticket_table.setRowCount(0)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(2, item)
        self.ticket_table.horizontalHeader().setCascadingSectionResizes(True)
        self.ticket_table.horizontalHeader().setStretchLastSection(True)
        self.ticket_table.verticalHeader().setVisible(True)
        self.ticket_table.verticalHeader().setCascadingSectionResizes(True)
        self.ticket_table.verticalHeader().setStretchLastSection(False)
        self.ticket_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ticket_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.gridLayout_13.addWidget(self.ticket_table, 0, 0, 1, 1)
        self.horizontal = QHBoxLayout()
        spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal.addItem(spacerItem18)
        self.create_bill_button = QPushButton(self)
        self.create_bill_button.setAutoDefault(False)
        self.horizontal.addWidget(self.create_bill_button)
        self.gridLayout_13.addLayout(self.horizontal, 1, 0, 1, 1)

        self.ticket_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Table", None, QApplication.UnicodeUTF8))
        self.ticket_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Ticket", None, QApplication.UnicodeUTF8))
        self.ticket_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "State", None, QApplication.UnicodeUTF8))
        self.create_bill_button.setText(
            QApplication.translate("MainWindow", "Create Bill", None, QApplication.UnicodeUTF8))
        ###########################################################################
        self.billtablerow_count = 0
        self.billnumber = None
        self.search = SearchMenu()
        self.bill = Search()
        self.save = SaveTicket()
        self.create_bill_button.clicked.connect(self.save_bills)
        self.setFocusPolicy(Qt.StrongFocus)  ###this and next line gets the focus event
        self.focusInEvent = self.got_focus
        self.editable = True
        ###mainwidnow to access the status bar
        widgets = QApplication.topLevelWidgets()
        self.mainwindow, = [i for i in widgets if type(i).__name__ == 'QMainWindow']
        # self.add_new_row()
        # self.mainwindow.ticket_table.cellChanged.connect(self.process_amount)
        ############################################################################

    def add_new_row(self, new=True):
        """
        Adds a new row to the billing module
        """
        try:
            table = self.ticket_table
            if new:
                ######################################
                ticket = QLineEdit()
                row = table.rowCount()
                table.setRowCount(row + 1)
                ticket.editingFinished.connect(lambda row=row: self.search_table(row))
                table.setCellWidget(row, 1, ticket)

            table.setColumnWidth(0, (table.width() / 3))
            table.setColumnWidth(1, (table.width() / 3))
            table.horizontalHeader().setStretchLastSection(True)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_table(self, row):
        """get the table number of the ticket"""
        ticket = self.ticket_table.cellWidget(row, 1)
        ticket_number = ticket.text()
        data = self.save.get_details(ticket_number=ticket_number)
        if data:
            table_no = QTableWidgetItem(str(data[0]))
            self.ticket_table.setItem(row, 0, table_no)
            state = QTableWidgetItem(data[1].title())
            self.ticket_table.setItem(row, 2, state)
        else:  # clean
            item = QTableWidgetItem()
            self.ticket_table.setItem(row, 0, item)
            self.ticket_table.setItem(row, 2, item)
        self.check_and_add_row()

    def delete_unwanted_row(self):
        """
        deletes unwanted row
        :return:None
        """
        leav = False
        try:
            while True:
                for i in range(self.ticket_table.rowCount()):
                    val = self.ticket_table.cellWidget(i, 3).text()
                    if str(val) == '0' or str(val) == '':
                        self.ticket_table.removeRow(i)
                        break
                    elif i == self.ticket_table.rowCount() - 1:
                        leav = True
                    else:
                        pass
                if leav:
                    break
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def check_and_add_row(self):
        """
        if the last row is empty then dont add a new row
        """
        row = self.ticket_table.rowCount()
        lastrow = row - 1
        try:
            val = self.ticket_table.item(lastrow, 0).text()
            if str(val):
                self.add_new_row()
            else:
                pass
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def got_focus(self, event):
        """
        gets focus of the tab
        :param event:event function
        :return:adds a new row to align properly
        """
        try:
            count = self.ticket_table.rowCount()
            if count < 2:
                self.add_new_row()
                self.add_new_row()
                widget = self.ticket_table.cellWidget(0, 1)
                QTimer.singleShot(0, widget.setFocus)
            else:
                self.add_new_row(new=False)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def save_bills(self):
        """
        saves the bills and changes its status
        :return:none
        """
        try:
            status = self.mainwindow.statusBar()
            status.setStyleSheet('color:red;')
            status.showMessage('System Info|Please Wait')
            QCoreApplication.processEvents()  # very important to repaint
            dataobj = self.get_data()
            if dataobj:
                data = self.save.save_invoice(dataobj)
                if data[0]:
                    self.parent.bill_number = data[1]
                    QMessageBox.information(QMessageBox(),
                        'Success', 'The Bill was saved', QMessageBox.Ok)
                    self.close()
                else:
                    QMessageBox.critical(QMessageBox(),
                        'Failed', data[1], QMessageBox.Ok)

            status.clearMessage()
            return True
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_data(self):
        """
        fetches all the data for printing
        :return:list of dictionary
        """
        try:
            table = self.ticket_table
            rows = table.rowCount()
            lines = []
            for i in range(rows):
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                item_ = item.text()
                if not item_:
                    continue
                table_no = table.item(i, 0).text()
                if not table_no:
                    continue
                state = table.item(i, 2).text()
                if not state or state == 'Cancel':
                    self.show_error('non cancelled tickets')
                    return False
                lines.append(item_)
            if not lines:
                self.show_error('Data')
                return False
            lines = self.rearrange_lies(lines)
            return lines
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def rearrange_lies(self, inpt):
        """rearranges lines"""
        output = []
        for i in inpt:
            if i not in output:
                output.append(i)
        return output

    def show_error(self, text):
        """
        :return: pops up an error
        """
        try:
            QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return False
