#! /usr/bin/env python

""" Inventory Module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from decimal import Decimal
from collections import defaultdict
from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QGridLayout, QTableWidget, QPushButton, QAbstractItemView, QPrintDialog, QDialog, QLabel, QDateEdit, QLineEdit, \
    QMessageBox, QCheckBox, QDoubleValidator, QComboBox, QDateTimeEdit, QIntValidator, QShortcut, QKeySequence

from PySide.QtCore import Qt, QDate

from printer.print_execute import PrintNow
from inventory_popupGUI.supplier_add import Ui_Supplier_Add
from inventory_popupGUI.new_item import Ui_new_item
from inventory_popupGUI.new_category import Ui_new_category
from inventory_popupGUI.new_item_newsupplier import Ui_new_supplier
from inventory_tryton import BusinessParty, ItemProduct, CategoryOfProduct, SchedulePurchase, AddStockInventory, \
    StockInventory, ReleaseDiscard, KitechenInventory
from datetime import datetime, timedelta
import logging
from GUI import settings

logger = logging.getLogger(__name__)


class Inventory():
    """Inventory main container """
    def __init__(self):
        ####
        self.inventory_tab_1 = QWidget()
        self.inventory_tab_1.setAutoFillBackground(False)
        self.inventory_tab_1.setStyleSheet("")
        self.inventory_tab_1.setObjectName("inventory_tab_1")
        self.horizontalLayout_3 = QHBoxLayout(self.inventory_tab_1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.inventory_detail_tabWidget = QTabWidget(self.inventory_tab_1)
        self.inventory_detail_tabWidget.setObjectName("inventory_detail_tabWidget")
        self.inventory_detail_tabWidget.setCurrentIndex(0)
        self.add_tabs()
        self.horizontalLayout_3.addWidget(self.inventory_detail_tabWidget)
        ##### signals and slotts && other stuffs
        self.inventory_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.inventory_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.inventory_tab_1.focusInEvent = self.change_focus

    def add_tabs(self):
        """
        adds the new tabs
        """
        stock = Stock()
        store = KitchenStore()
        adds = AddStock()
        release = Release()
        purchaseSchedule = PurchaseSchedule()
        supplier = Supplier()
        item = Item()
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_stock']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(0))
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_add']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(1))
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_release']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(2))
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_purchase']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(3))
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_supplier']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(4))
        QShortcut(QKeySequence(settings.custom_shortcut['inventorytab_item']),
                  self.inventory_detail_tabWidget, lambda: self.change_index(5))
        self.inventory_detail_tabWidget.addTab(stock.stock_tab_1, "Stock")
        self.inventory_detail_tabWidget.addTab(store.stock_tab_1, "Kitchen Store")
        self.inventory_detail_tabWidget.addTab(adds.add_tab_2, "Add")
        self.inventory_detail_tabWidget.addTab(release.release_tab_3, "Release")
        self.inventory_detail_tabWidget.addTab(purchaseSchedule.purchaseSchedule_tab_4, "Purchase Schedule")
        self.inventory_detail_tabWidget.addTab(supplier.supplier_tab_5, "Supplier")
        self.inventory_detail_tabWidget.addTab(item.itemdetail_tab_6, "Item")

    def change_focus(self, event=None):
        """
        to handle the change in focus event
        """
        wid = self.inventory_detail_tabWidget.currentWidget()
        if wid.isVisible():
            wid.setFocus()

    def change_index(self, index):
        """changes the index of the tab"""
        self.inventory_detail_tabWidget.setCurrentIndex(index)


class Stock():
    """Stock Managment tab"""
    global logger

    def __init__(self):
        #####
        logger.info('Inside Stock')
        self.stock_tab_1 = QWidget()
        self.stock_tab_1.setObjectName("stock_tab_1")
        self.gridLayout_3 = QGridLayout(self.stock_tab_1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stock_table = QTableWidget(self.stock_tab_1)
        self.stock_table.setWordWrap(False)
        self.stock_table.setSortingEnabled(True)
        self.stock_table.setObjectName("stock_table")
        self.stock_table.setColumnCount(7)
        self.stock_table.setRowCount(0)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.stock_table.setHorizontalHeaderItem(6, item)
        self.stock_table.horizontalHeader().setStretchLastSection(True)
        self.stock_table.verticalHeader().setCascadingSectionResizes(True)
        self.stock_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.stock_table, 0, 0, 1, 3)
        self.stock_refresh_button = QPushButton(self.stock_tab_1)
        self.stock_refresh_button.setObjectName("stock_refresh_button")
        self.gridLayout_3.addWidget(self.stock_refresh_button, 1, 0, 1, 1)
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 1, 1, 1, 1)
        self.stock_print_button = QPushButton(self.stock_tab_1)
        self.stock_print_button.setObjectName("stock_print_button")
        self.gridLayout_3.addWidget(self.stock_print_button, 1, 2, 1, 1)
        ##retranslate
        self.stock_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Batch No", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Supplier", None, QApplication.UnicodeUTF8))
        self.stock_table.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Ex. Date", None, QApplication.UnicodeUTF8))
        self.stock_refresh_button.setText(
            QApplication.translate("MainWindow", "Refresh", None, QApplication.UnicodeUTF8))
        self.stock_print_button.setText(QApplication.translate("MainWindow", "Print", None, QApplication.UnicodeUTF8))
        ##signals and slots & other functions
        self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stock_print_button.clicked.connect(self.print_pdf)
        self.stock_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.stock_tab_1.focusInEvent = self.got_focus
        self.stockinventory = StockInventory()
        self.stock_refresh_button.clicked.connect(self.load_rows)
        self.datalist = None
        self.load_rows()
        self.assign_shortcuts()
        # self.add_row_in_stock_table()  # for automatic updating the stock table

    def assign_shortcuts(self):
        """assigns a shortcut"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorystock_refresh']),
                  self.stock_tab_1, self.load_rows)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorystock_print']),
                  self.stock_tab_1, self.print_pdf)

    def add_row_in_stock_table(self, *args):
        """new row entry"""
        # the below lines are for inserting dummy data!!
        table = self.stock_table
        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for n, i in enumerate(args):
                item = QTableWidgetItem(i['code'])
                table.setItem(n, 0, item)
                item = QTableWidgetItem(i['item'])
                table.setItem(n, 1, item)
                item = QTableWidgetItem(i['category'])
                table.setItem(n, 2, item)
                item = QTableWidgetItem(i['quantity'])
                table.setItem(n, 3, item)
                item = QTableWidgetItem(i['batch_number'])
                table.setItem(n, 4, item)
                item = QTableWidgetItem(i['supplier'])
                table.setItem(n, 5, item)
                item = QTableWidgetItem(i['expiry_date'])
                table.setItem(n, 6, item)
        table.setColumnWidth(0, ((table.width() * 0.5) / 7))
        table.setColumnWidth(1, (table.width() / 7))
        table.setColumnWidth(2, ((table.width() * 2) / 7))
        table.setColumnWidth(3, ((table.width() * 0.5) / 7))
        table.setColumnWidth(4, (table.width() / 7))
        table.setColumnWidth(5, (table.width() / 7))
        table.setColumnWidth(6, (table.width() / 7))
        table.horizontalHeader().setStretchLastSection(True)

    def load_rows(self):
        """
        :return:Loads the rows with the data from the db
        """
        self.datalist = self.stockinventory.load_stock()
        if self.datalist:
            self.add_row_in_stock_table(*self.datalist)
        else:
            self.stock_table.clearContents()
            self.stock_table.setRowCount(0)
        logger.info('Stock rows loaded')

    def print_pdf(self):
        """
        prints the pdf/text of stock
        :return:none
        """
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            p = dialog.printer()
            printing = PrintNow(p.printerName(), self.datalist, 'stock')
            printing.start_print()
            logger.info('Stock printed')

    def got_focus(self, event):
        self.add_row_in_stock_table()


class KitchenStore(Stock):
    """Kitchen store inventroy details Managment"""
    global logger

    def __init__(self):
        logger.info('Inside KitchenStore')
        Stock.__init__(self)
        self.stockinventory = KitechenInventory()
        self.load_rows()

    def assign_shortcuts(self):
        """add shortcut entries as required"""
        pass

    def load_rows(self):
        """loads the entry details"""
        Stock.load_rows(self)
        logger.info('Kitchen rows loaded')

    def print_pdf(self):
        """print the details"""
        Stock.print_pdf(self)
        logger.info('Kitchen rows print initiated')


class AddStock():
    """Stock Addition or Updation tab"""
    global logger

    def __init__(self):
        #####
        logger.info('Inside Add stock')
        self.add_tab_2 = QWidget()
        self.add_tab_2.setObjectName("add_tab_2")
        self.gridLayout_5 = QGridLayout(self.add_tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QLabel(self.add_tab_2)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.add_stock_date = QDateEdit(self.add_tab_2)
        self.add_stock_date.setDisplayFormat('dd/MM/yyyy')
        self.add_stock_date.setMinimumDate(QDate.currentDate())
        self.add_stock_date.setCalendarPopup(True)
        self.add_stock_date.setObjectName("add_stock_date")
        self.horizontalLayout_5.addWidget(self.add_stock_date)
        # self.label_3 = QLabel(self.add_tab_2)
        # self.label_3.setObjectName("label_3")
        # self.horizontalLayout_5.addWidget(self.label_3)
        # self.add_stock_suppliercode = QLineEdit(self.add_tab_2)
        # self.add_stock_suppliercode.setObjectName("add_stock_suppliercode")
        # self.horizontalLayout_5.addWidget(self.add_stock_suppliercode)
        self.label_2 = QLabel(self.add_tab_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.add_stock_batchno = QLineEdit(self.add_tab_2)
        self.add_stock_batchno.setObjectName("add_stock_batchno")
        self.horizontalLayout_5.addWidget(self.add_stock_batchno)
        self.add_stock_searchbatch_button = QPushButton(self.add_tab_2)
        self.add_stock_searchbatch_button.setObjectName("add_stock_searchbatch_button")
        self.horizontalLayout_5.addWidget(self.add_stock_searchbatch_button)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem7, 1, 1, 1, 1)
        self.add_stock_table_insertrow_button = QPushButton(self.add_tab_2)
        self.add_stock_table_insertrow_button.setObjectName("add_stock_table_insertrow_button")
        self.gridLayout_4.addWidget(self.add_stock_table_insertrow_button, 1, 0, 1, 1)
        self.add_stock_table = QTableWidget(self.add_tab_2)
        self.add_stock_table.setObjectName("add_stock_table")
        self.add_stock_table.setColumnCount(10)
        self.add_stock_table.setRowCount(0)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.add_stock_table.setHorizontalHeaderItem(9, item)
        self.add_stock_table.horizontalHeader().setStretchLastSection(True)
        self.add_stock_table.verticalHeader().setCascadingSectionResizes(True)
        self.add_stock_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_4.addWidget(self.add_stock_table, 0, 0, 1, 3)
        self.add_stock_addstock_button = QPushButton(self.add_tab_2)
        self.add_stock_addstock_button.setObjectName("add_stock_addstock_button")
        self.gridLayout_4.addWidget(self.add_stock_addstock_button, 1, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        ##retranslate
        self.label.setText(QApplication.translate("MainWindow", "Date:", None, QApplication.UnicodeUTF8))
        # self.label_3.setText(
        # QApplication.translate("MainWindow", "Supplier Code", None, QApplication.UnicodeUTF8))
        self.label_2.setText(
            QApplication.translate("MainWindow", "Batch No:", None, QApplication.UnicodeUTF8))
        self.add_stock_searchbatch_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.add_stock_table_insertrow_button.setText(
            QApplication.translate("MainWindow", "Insert New Row", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select All", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Unit", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Rate", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(7).setText(
            QApplication.translate("MainWindow", "Amount", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(8).setText(
            QApplication.translate("MainWindow", "Supplier", None, QApplication.UnicodeUTF8))
        self.add_stock_table.horizontalHeaderItem(9).setText(
            QApplication.translate("MainWindow", "Ex. Date", None, QApplication.UnicodeUTF8))
        self.add_stock_addstock_button.setText(
            QApplication.translate("MainWindow", "Add Stock", None, QApplication.UnicodeUTF8))
        #### signals and slotts &&& other stuffs
        self.count = 0
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.schedule = SchedulePurchase()
        self.supplier = BusinessParty(category='Supplier')
        self.add = AddStockInventory()
        self.item = ItemProduct()
        self.batch_number = None
        self.get_batch()
        self.add_stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.add_stock_table_insertrow_button.clicked.connect(self.add_new_blank_rows)
        self.add_stock_addstock_button.clicked.connect(self.commit)
        self.add_tab_2.setFocusPolicy(Qt.StrongFocus)
        self.add_stock_searchbatch_button.clicked.connect(self.search_batch)
        self.add_stock_table.horizontalHeader().sectionClicked.connect(self.select_all_checkboxes)
        self.add_tab_2.focusInEvent = self.just_to_get_focus
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assign shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryadd_search']),
                  self.add_tab_2, self.search_batch)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryadd_newrow']),
                  self.add_tab_2, self.add_new_blank_rows)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryadd_addstock']),
                  self.add_tab_2, self.commit)

    def select_all_checkboxes(self, item):
        """selects all chekboxes"""
        # self.select_all = self.mainwindow.release_discardtable.horizontalHeaderItem(item)
        if item == 0:
            r = self.add_stock_table.rowCount()
            for i in range(r):
                chekbox = self.add_stock_table.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def get_batch(self):
        """get batch details of the stock"""
        self.batch_number = self.schedule.get_largest_batch()

    def add_new_blank_rows(self):
        """
        deletes the schedules in the database
        """
        table = self.add_stock_table
        item = table.item(0, 0)
        if item:
            message = QMessageBox.critical(QMessageBox(), 'Warning!', 'This will remove all the entries',
                QMessageBox.Ok | QMessageBox.Cancel)
            if message == QMessageBox.Ok:
                table.setRowCount(0)
                table.clearContents()
                self.add_row_to_table('new')
        elif not item:
            self.add_row_to_table('new')


    def add_row_to_table(self, *args):
        """
        new row entry
        complex stuff of auto complete to be added to each combo box
        :return:
        """
        # todo tryton needs data from moves to be added to the combobox
        table = self.add_stock_table
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    chk = QCheckBox()
                    table.setCellWidget(i, 0, chk)
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(j['category'])
                    table.setItem(i, 3, item)
                    item = QTableWidgetItem(j['unit'])
                    table.setItem(i, 4, item)
                    quantity = QLineEdit()
                    quantity.setValidator(QDoubleValidator(0.000, 999.999, 3))
                    quantity.setText(j['quantity'])
                    quantity.editingFinished.connect(lambda row=i: self.calculate_amount(row=row))
                    table.setCellWidget(i, 5, quantity)
                    rate = QLineEdit()
                    rate.setValidator(QDoubleValidator(0.000, 999.999, 3))
                    rate.setText(j['rate'])
                    rate.editingFinished.connect(lambda row=i: self.calculate_amount(row=row))
                    table.setCellWidget(i, 6, rate)
                    amount = QLineEdit()
                    amount.setValidator(QDoubleValidator(0.000, 999.999, 3))
                    amount.editingFinished.connect(lambda row=i: self.calculate_amount(row=row))
                    value = Decimal(quantity.text()).multiply(Decimal(rate.text()))
                    amount.setText(value.to_eng())
                    table.setCellWidget(i, 7, amount)
                    supplier = QComboBox()
                    self.populate_suppliers(supplier)
                    if j.get('supplier'):
                        item = supplier
                        index = item.findText(j['supplier'])
                        item.setCurrentIndex(index)
                    table.setCellWidget(i, 8, supplier)
                    date = QDateTimeEdit()
                    date.setDisplayFormat('dd/MM/yyyy')
                    date.setMinimumDate(QDate.currentDate())
                    table.setCellWidget(i, 9, date)
            elif args[0] == 'new':
                row = table.rowCount() + 1
                table.setRowCount(row)
                chk = QCheckBox()
                table.setCellWidget(row - 1, 0, chk)
                codeline = QLineEdit()
                codeline.editingFinished.connect(lambda: self.get_details_of_code(row))
                table.setCellWidget(row - 1, 1, codeline)
                itemcombo = QComboBox()
                self.fill_item_list(itemcombo)
                itemcombo.currentIndexChanged.connect(lambda: self.get_details_of_item(row))
                table.setCellWidget(row - 1, 2, itemcombo)
                item = QTableWidgetItem()
                table.setItem(row - 1, 3, item)
                unit = QTableWidgetItem()
                table.setItem(row - 1, 4, unit)
                quantity = QLineEdit()
                quantity.editingFinished.connect(lambda: self.calculate_amount(row - 1))
                table.setCellWidget(row - 1, 5, quantity)
                rate = QLineEdit()
                rate.editingFinished.connect(lambda: self.calculate_amount(row - 1))
                table.setCellWidget(row - 1, 6, rate)
                amount = QLineEdit()
                amount.editingFinished.connect(lambda: self.calculate_amount(row - 1))
                table.setCellWidget(row - 1, 7, amount)
                supplier = QComboBox()
                self.populate_suppliers(supplier)
                table.setCellWidget(row - 1, 8, supplier)
                date = QDateTimeEdit()
                date.setDisplayFormat('dd/MM/yyyy')
                date.setMinimumDate(QDate.currentDate())
                table.setCellWidget(row - 1, 9, date)
        table.setColumnWidth(0, ((table.width() * 0.4) / 10))
        table.setColumnWidth(1, ((table.width() * 0.5) / 10))
        table.setColumnWidth(2, ((table.width() * 1.5) / 10))
        table.setColumnWidth(3, ((table.width() * 1.5) / 10))
        table.setColumnWidth(4, ((table.width() * 0.5) / 10))
        table.setColumnWidth(5, ((table.width() * 0.5) / 10))
        table.setColumnWidth(6, ((table.width() * 0.5) / 10))
        table.setColumnWidth(7, ((table.width() * 0.5) / 10))
        table.setColumnWidth(8, ((table.width() * 1.5) / 10))
        table.horizontalHeader().setStretchLastSection(
            True)  # important to resize last section else blank space after last column

    def calculate_amount(self, row):
        """
        calculates the value of the amount
        :param row: the row number
        :return:none
        """
        row = row
        table = self.add_stock_table
        rate = table.cellWidget(row, 6).text()
        quantity = table.cellWidget(row, 5).text()
        if rate and quantity:
            amount = Decimal(rate).multiply(Decimal(quantity))
            amount_line = table.cellWidget(row, 7)
            amount_line.setText(amount.to_eng())

    def populate_suppliers(self, combo):
        """
        fills the supplier list for each item line
        :param combo: the combo box of suppliers
        :return:none
        """
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")

        datalist = self.supplier.list_suppliers_with_id()
        itemfield.addItems(datalist.values())

    def fill_item_list(self, combo):
        """
        fill the item combo box
        :param combo: the combobox object
        :return: none
        """
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        itemfield.addItems(self.item.fill_item_list())

    def get_details_of_code(self, rowcount):
        """
        fills the item, category and units based on the code
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.add_stock_table
        codeline = table.cellWidget(row, 1)
        data = self.item.get_details_of_code(codeline.text())
        item = table.cellWidget(row, 2)
        index = item.findText(data['item'])
        item.setCurrentIndex(index)
        category = table.item(row, 3)
        category.setText(data['category'])
        units = table.item(row, 4)
        units.setText(data['units'])
        rate = table.cellWidget(row, 6)
        rate.setText(data['rate'])
        if data.get('supplier'):
            item = table.cellWidget(row, 8)
            index = item.findText(data['supplier'])
            item.setCurrentIndex(index)

    def get_details_of_item(self, rowcount):
        """
        fills the code, category and units based on the item
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.add_stock_table
        itemcombo = table.cellWidget(row, 2)
        data = self.item.get_details_of_item(itemcombo.currentText())
        code = table.cellWidget(row, 1)
        code.setText(data['code'])
        category = table.item(row, 3)
        category.setText(data['category'])
        units = table.item(row, 4)
        units.setText(data['units'])
        rate = table.cellWidget(row, 6)
        rate.setText(data['rate'])
        if data.get('supplier'):
            item = table.cellWidget(row, 8)
            index = item.findText(data['supplier'])
            item.setCurrentIndex(index)

    def search_batch(self):
        """
        searches the items of the batch number
        :return:
        """
        text = self.add_stock_batchno.text()
        if text:
            table = self.add_stock_table
            item = table.cellWidget(0, 1)
            if item:
                message = QMessageBox.critical(QMessageBox(), 'Warning!', 'This will remove all the entries',
                    QMessageBox.Ok | QMessageBox.Cancel)
                if message == QMessageBox.Ok:
                    table.setRowCount(0)
                    table.clearContents()

                    data = self.add.search_batch(text)
                    if data:
                        self.add_row_to_table(*data)
            elif not item:
                data = self.add.search_batch(text)
                if data:
                    self.add_row_to_table(*data)

    def commit(self):
        """
        saves the details in db before printing
        """
        logger.info('AddStock rows being added')
        data = self.get_data()
        table = self.add_stock_table
        item = table.cellWidget(0, 2)
        for i, j in data.iteritems():
            batch = self.batch_number
            if not batch:
                batch = "%s%s" % (datetime.today().strftime("%y%m"), '000')  # initial batch
            else:
                yearandmonth = datetime.today().strftime("%y%m")
                batch_list = list(batch)
                compare = "".join([batch_list[0], batch_list[1], batch_list[2], batch_list[3]])
                if compare >= yearandmonth:
                    digit = "".join([batch_list[4], batch_list[5], batch_list[6]])
                    if digit == "999":
                        digit = "000"
                    else:
                        digit = "%03d" % (int(digit) + 1)
                    batch = "%s%s" % (compare, digit)
                else:
                    batch = "%s000" % yearandmonth
            print batch
            if item:
                status = self.schedule.save_purchase(j, batch)
                if status:
                    state = self.add.confirm_purchase(j, batch)
                    if state:
                        self.batch_number = batch
                        msg = QMessageBox.information(QMessageBox(), 'Success!!',
                            'The products were added successfully!!', QMessageBox.Ok)
                        if msg == QMessageBox.Ok:
                            pass
            else:
                batch = self.add_stock_batchno.text()
                status = self.add.confirm_purchase(j, batch)
                if status:
                    self.batch_number = batch
                    msg = QMessageBox.information(QMessageBox(), 'Success!!',
                        'The products were added successfully!!', QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        pass
                else:
                    msg = QMessageBox.critical(QMessageBox(), 'Failure!!',
                        'The products could not be added,please check the batch number', QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        return False
            for row in j:
                model_index = table.indexFromItem(row['model_item'])
                row = model_index.row()
                table.removeRow(row)

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.add_stock_table
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            print "issue"
            chk = table.cellWidget(i, 0)
            if chk.isChecked():
                dictionary = {}
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['code'] = item.text()
                if dictionary['code'] == '':
                    break
                item = table.cellWidget(i, 2).currentText() if table.cellWidget(i, 2) is not None else table.item(i, 2).text()
                dictionary['item'] = item
                item = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
                dictionary['category'] = item.text()
                item = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
                dictionary['units'] = item.text()
                item = table.cellWidget(i, 5) if table.cellWidget(i, 5) is not None else table.item(i, 5)
                dictionary['quantity'] = item.text()
                if dictionary['quantity'] == '':
                    self.show_error('Quantity')
                    return False
                item = table.cellWidget(i, 6) if table.cellWidget(i, 6) is not None else table.item(i, 6)
                dictionary['rate'] = item.text()
                if dictionary['rate'] == '':
                    self.show_error('rate')
                    return False
                item = table.cellWidget(i, 8).currentText() if table.cellWidget(i, 8) is not None else table.item(i, 8).text()
                dictionary['supplier'] = item
                item = table.cellWidget(i, 9).date()
                dictionary['expiry_date'] = datetime.strptime(item.toString('yyyy-MM-dd'), '%Y-%m-%d')
                dictionary['model_item'] = table.item(i, 4)
                dataobj.append(dictionary)
        data = self.group_schedule_with_supplier(dataobj)
        return data

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)

    def group_schedule_with_supplier(self, dataobj):
        """
        groups the table data according to the supplier
        :param dataobj: the list of dictionary from getdata
        :return:arranged list of dictionary
        """
        dataobj = dataobj
        supplier = []
        for i in dataobj:
            if not supplier:
                supplier.append(i['supplier'])
            else:
                if i['supplier'] in supplier:
                    continue
                else:
                    supplier.append(i['supplier'])
        data = defaultdict(list)
        for n, i in enumerate(supplier):
            for j in dataobj:
                if j['supplier'] == i:
                    data[n].append(j)
        return data

    def just_to_get_focus(self, event):
        """
         just gets focus
        :return: none
        """
        pass


class Release():
    """Stock Releas Managment tab"""
    global logger

    def __init__(self):
        #######
        logger.info('Inside Release Tab')
        self.release_tab_3 = QWidget()
        self.release_tab_3.setObjectName("release_tab_3")
        self.gridLayout_18 = QGridLayout(self.release_tab_3)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.release_releasetable_today_button = QPushButton(self.release_tab_3)
        self.gridLayout_6.addWidget(self.release_releasetable_today_button, 1, 0, 1, 1)
        self.release_releasetable_newrow_button = QPushButton(self.release_tab_3)
        self.gridLayout_6.addWidget(self.release_releasetable_newrow_button, 1, 1, 1, 1)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem8, 1, 2, 1, 1)
        self.release_releasetable_button = QPushButton(self.release_tab_3)
        self.release_releasetable_button.setObjectName("release_releasetable_button")
        self.gridLayout_6.addWidget(self.release_releasetable_button, 1, 3, 1, 1)
        self.release_releasetable = QTableWidget(self.release_tab_3)
        self.release_releasetable.setObjectName("release_releasetable")
        self.release_releasetable.setColumnCount(7)
        self.release_releasetable.setRowCount(0)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.release_releasetable.setHorizontalHeaderItem(6, item)
        self.release_releasetable.horizontalHeader().setCascadingSectionResizes(True)
        self.release_releasetable.horizontalHeader().setStretchLastSection(True)
        self.release_releasetable.verticalHeader().setVisible(False)
        self.release_releasetable.verticalHeader().setCascadingSectionResizes(True)
        self.release_releasetable.verticalHeader().setStretchLastSection(False)
        self.gridLayout_6.addWidget(self.release_releasetable, 0, 0, 1, 4)
        self.gridLayout_18.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.release_discardtable = QTableWidget(self.release_tab_3)
        self.release_discardtable.setObjectName("release_discardtable")
        self.release_discardtable.setColumnCount(8)
        self.release_discardtable.setRowCount(0)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.release_discardtable.setHorizontalHeaderItem(7, item)
        self.release_discardtable.horizontalHeader().setCascadingSectionResizes(True)
        self.release_discardtable.horizontalHeader().setStretchLastSection(True)
        self.release_discardtable.verticalHeader().setVisible(False)
        self.release_discardtable.verticalHeader().setCascadingSectionResizes(True)
        self.release_discardtable.verticalHeader().setStretchLastSection(False)
        self.gridLayout_7.addWidget(self.release_discardtable, 0, 0, 1, 3)
        self.release_discardtable_addnewbutton_button = QPushButton(self.release_tab_3)
        self.release_discardtable_addnewbutton_button.setObjectName("release_discardtable_addnewbutton_button")
        self.gridLayout_7.addWidget(self.release_discardtable_addnewbutton_button, 1, 0, 1, 1)
        spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem9, 1, 1, 1, 1)
        self.release_discardtable_button = QPushButton(self.release_tab_3)
        self.release_discardtable_button.setObjectName("release_discardtable_button")
        self.gridLayout_7.addWidget(self.release_discardtable_button, 1, 2, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_7, 1, 0, 1, 1)
        ###retranslate
        self.release_releasetable_today_button.setText(
            QApplication.translate("MainWindow", "Today's Release", None, QApplication.UnicodeUTF8))
        self.release_releasetable_newrow_button.setText(
            QApplication.translate("MainWindow", "New Row", None, QApplication.UnicodeUTF8))
        self.release_releasetable_button.setText(
            QApplication.translate("MainWindow", "Release", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select All", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Unit", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.release_releasetable.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Batch Info", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select All", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Unit", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Batch No", None, QApplication.UnicodeUTF8))
        self.release_discardtable.horizontalHeaderItem(7).setText(
            QApplication.translate("MainWindow", "Notes", None, QApplication.UnicodeUTF8))
        self.release_discardtable_addnewbutton_button.setText(
            QApplication.translate("MainWindow", "Add New Row", None, QApplication.UnicodeUTF8))
        self.release_discardtable_button.setText(
            QApplication.translate("MainWindow", "Discard", None, QApplication.UnicodeUTF8))
        #### signals and slotts &&& other stuffs
        self.release_discard = ReleaseDiscard()
        self.details = ItemProduct()
        self.ob = SchedulePurchase()
        self.item = ItemProduct()
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        # [self.add_row_to_releasetable() for i in range(5)]
        self.release_discardtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.release_releasetable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.release_releasetable_button.clicked.connect(self.release_stock)
        self.release_discardtable_button.clicked.connect(self.discard_stock)
        self.release_releasetable_newrow_button.clicked.connect(lambda: self.add_row_to_releasetable('new'))
        self.release_discardtable_addnewbutton_button.clicked.connect(lambda: self.add_row_to_discardtable('new'))
        self.release_releasetable_today_button.clicked.connect(self.todays_release)
        # item = QTableWidgetItem()
        # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        # item.setCheckState(Qt.Unchecked)
        # self.mainwindow.release_discardtable.setHorizontalHeaderItem(0, item)
        # not working when trying to create a check box in the vertical header
        self.release_discardtable.horizontalHeader().sectionClicked.connect(self.select_all_checkboxes_discard)
        self.release_releasetable.horizontalHeader().sectionClicked.connect(self.select_all_checkboxes_release)
        self.release_tab_3.setFocusPolicy(Qt.StrongFocus)
        self.release_tab_3.focusInEvent = self.just_to_get_focus
        self.add_row_to_releasetable('new')
        self.auto_populate_discardtable()
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns shortcut"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryrelease_todaysrelease']),
                  self.release_tab_3, self.todays_release)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryrelease_newrow']),
                  self.release_tab_3, lambda: self.add_row_to_releasetable('new'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryrelease_release']),
                  self.release_tab_3, self.release_stock)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryrelease_addnewrow']),
                  self.release_tab_3, lambda: self.add_row_to_discardtable('new'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryrelease_discard']),
                  self.release_tab_3, self.discard_stock)

    def todays_release(self):
        """loads stock to be released today"""
        logger.info('Release checked today\'s release')
        msg = QMessageBox.critical(QMessageBox(), 'Warning',
            'This will remove all the other rows in the table edited previously',
            QMessageBox.Ok | QMessageBox.Cancel)
        if msg == QMessageBox.Ok:
            day = (datetime.today()).strftime("%A")
            dataobj = self.ob.load_schedules(day=day.lower())
            if dataobj:
                self.add_row_to_releasetable(*dataobj)
            else:
                table = self.release_releasetable
                table.clearContents()
                table.setRowCount(0)

    def add_row_to_releasetable(self, *args):
        """new row entry to the table"""
        table = self.release_releasetable
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    chk = QCheckBox()
                    table.setCellWidget(i, 0, chk)
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(j['category'])
                    table.setItem(i, 3, item)
                    item = QTableWidgetItem(j['unit'])
                    table.setItem(i, 4, item)
                    quantity = QLineEdit()
                    quantity.setValidator(QDoubleValidator(0.000, 999.999, 3))
                    quantity.setText(str(j['quantity']))
                    quantity.editingFinished.connect(lambda item=item: self.check_quantity(item, table))
                    table.setCellWidget(i, 5, quantity)
                    batch = QTableWidgetItem()
                    table.setItem(i, 6, batch)
                self.trigger_editingFinished(table)
            elif args[0] == 'new':
                row = table.rowCount() + 1
                table.setRowCount(row)
                unit = QTableWidgetItem()
                table.setItem(row - 1, 4, unit)
                # had to change the order to get an item which
                # can be traced in a table even if rows are shuffled in discard stock
                chk = QCheckBox()
                table.setCellWidget(row - 1, 0, chk)
                code = QLineEdit()
                code.editingFinished.connect(lambda: self.get_details_of_code(unit, table))
                table.setCellWidget(row - 1, 1, code)
                itemcombo = QComboBox()
                self.fill_item_list(itemcombo)
                itemcombo.currentIndexChanged.connect(lambda: self.get_details_of_item(unit, table))
                itemcombo.focusInEvent = lambda s: self.focus_item_combo(itemcombo)
                table.setCellWidget(row - 1, 2, itemcombo)
                category = QTableWidgetItem()
                table.setItem(row - 1, 3, category)
                quantity = QLineEdit()
                quantity.setValidator(QDoubleValidator(0.000, 999.999, 3))
                quantity.editingFinished.connect(lambda: self.check_quantity(unit, table))
                table.setCellWidget(row - 1, 5, quantity)
                batch = QTableWidgetItem()
                table.setItem(row - 1, 6, batch)
        table.setColumnWidth(0, ((table.width() * 0.4) / 7))
        table.setColumnWidth(1, ((table.width() * 0.5) / 7))
        table.setColumnWidth(2, (table.width() / 7))
        table.setColumnWidth(3, (table.width() / 7))
        table.setColumnWidth(4, ((table.width() * 0.5) / 7))
        table.setColumnWidth(5, ((table.width() * 0.5) / 7))
        table.horizontalHeader().setStretchLastSection(True)

    def check_quantity(self, item, table):
        """
        check if the quantity is entered properly and checks the batch info for the product also add a new row below
        :param item: the table widget item
        :param table: the table of the widget
        :return:quantity
        """
        table = table
        row = self.get_rowcount(item, table)
        quantity_line = table.cellWidget(row, 5)
        quantity = quantity_line.text()
        item_combo = table.cellWidget(row, 2)
        if item_combo:
            item = item_combo.currentText()
        else:
            item = table.item(row, 2).text()
        batch = self.release_discard.collect_batch(item, quantity)
        text = []
        if batch:
            for i in batch:
                text.append(':'.join(i))
        else:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!!!', 'The item is not available, please check the stock.',
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                quantity_line.setText('0')
                return False
        batch_line = table.item(row, 6)
        batch_line.setText(','.join(text))
        if quantity:
            lastrow = table.rowCount() - 1
            if lastrow != row:
                check = table.cellWidget(lastrow, 5)
                if check:
                    chektext = check.text()
                    if str(chektext) is not '':
                        self.add_row_to_releasetable('new')
            else:
                self.add_row_to_releasetable('new')

    def trigger_editingFinished(self, table):
        """edit finished event handler"""
        row = table.rowCount()
        for i in range(row):
            item = table.item(i, 1)
            self.check_quantity(item, table)

    def focus_item_combo(self, itemcombo):
        """combobox focus event handler"""
        if itemcombo.count() == 0:
            self.fill_item_list(itemcombo)

    def fill_item_list(self, combo):
        """
        fill the item combo box
        :param combo: the combobox object
        :return: none
        """
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        itemfield.addItems(self.item.fill_item_list())

    def get_details_of_code(self, item, table):
        """
        fills the item, category and units based on the code
        :param rowcount: the row count
        :return: none
        """
        table = table
        row = self.get_rowcount(item, table)
        if table.objectName() == 'release_releasetable':
            codeline = table.cellWidget(row, 1)
            item = table.cellWidget(row, 2)
            category = table.item(row, 3)
            units = table.item(row, 4)
        else:
            codeline = table.cellWidget(row, 1)
            item = table.cellWidget(row, 2)
            category = table.item(row, 3)
            units = table.item(row, 4)
        data = self.details.get_details_of_code(codeline.text())
        index = item.findText(data['item'])
        item.setCurrentIndex(index)
        category.setText(data['category'])
        units.setText(data['units'])

    def get_details_of_item(self, item, table):
        """
        fills the code, category and units based on the item
        :param rowcount: the row count
        :return: none
        """
        table = table
        row = self.get_rowcount(item, table)
        if table.objectName() == 'release_releasetable':
            itemcombo = table.cellWidget(row, 2)
            code = table.cellWidget(row, 1)
            category = table.item(row, 3)
            units = table.item(row, 4)
        else:
            itemcombo = table.cellWidget(row, 2)
            code = table.cellWidget(row, 1)
            category = table.item(row, 3)
            units = table.item(row, 4)
        data = self.details.get_details_of_item(itemcombo.currentText())
        code.setText(data['code'])
        category.setText(data['category'])
        units.setText(data['units'])

    def get_rowcount(self, item, table):
        """
        gets the row count for the model
        :param item:any table item
        :param table:table object
        :return:row count
        """
        model_index = table.indexFromItem(item)
        row = model_index.row()
        return row

    def add_row_to_discardtable(self, *args):
        """adds new row entry"""
        table = self.release_discardtable
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    check = QCheckBox()
                    table.setCellWidget(i, 0, check)
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(j['category'])
                    table.setItem(i, 3, item)
                    item = QTableWidgetItem(j['unit'])
                    table.setItem(i, 4, item)
                    item = QTableWidgetItem(str(j['quantity']))
                    table.setItem(i, 5, item)
                    item = QTableWidgetItem(j['batch_number'])
                    table.setItem(i, 6, item)
                    combo = QComboBox()
                    combo.addItem("Expired")
                    combo.addItem("Stale")
                    combo.addItem("Damp")
                    combo.addItem("Spilled")
                    table.setCellWidget(i, 7, combo)
            elif args[0] == 'new':
                row = table.rowCount() + 1
                table.setRowCount(row)
                unit = QTableWidgetItem()
                table.setItem(row - 1, 4, unit)
                # had to change the order to get an item which
                # can be traced in a table even if rows are shuffled in discard stock
                check = QCheckBox()
                table.setCellWidget(row - 1, 0, check)
                code = QLineEdit()
                code.editingFinished.connect(lambda: self.get_details_of_code(unit, table))
                table.setCellWidget(row - 1, 1, code)
                itemcombo = QComboBox()
                self.fill_item_list(itemcombo)
                itemcombo.currentIndexChanged.connect(lambda: self.get_details_of_item(unit, table))
                table.setCellWidget(row - 1, 2, itemcombo)
                category = QTableWidgetItem()
                table.setItem(row - 1, 3, category)
                quantity = QLineEdit()
                table.setCellWidget(row - 1, 5, quantity)
                batch = QLineEdit()
                table.setCellWidget(row - 1, 6, batch)
                combo = QComboBox()
                combo.addItem("Expired")
                combo.addItem("Stale")
                combo.addItem("Damp")
                combo.addItem("Spilled")
                table.setCellWidget(row - 1, 7, combo)
        table.setColumnWidth(0, ((table.width() * 0.5) / 8))
        table.setColumnWidth(1, ((table.width() * 0.5) / 8))
        table.setColumnWidth(2, ((table.width() * 1.5) / 8))
        table.setColumnWidth(3, ((table.width() * 1.5) / 8))
        table.setColumnWidth(4, ((table.width() * 1) / 8))
        table.setColumnWidth(5, ((table.width() * 0.5) / 8))
        table.setColumnWidth(6, ((table.width() * 1) / 8))
        table.horizontalHeader().setStretchLastSection(True)

    def auto_populate_discardtable(self):
        """populates the discard table"""
        discard = self.release_discard.populate_discard()
        self.add_row_to_discardtable(*discard)
        logger.info('Release Discard table populated')

    def release_stock(self):
        """release the stock entry"""
        logger.info('Release stock release initiated')
        table = self.release_releasetable
        data = self.get_data()
        if data:
            for i in data:
                status = self.release_discard.release(i['item'], i['quantity'])
                if status:
                    model_index = table.indexFromItem(i['model_item'])
                    row = model_index.row()
                    table.removeRow(row)
                else:
                    msg = QMessageBox.critical(QMessageBox(), 'Fail!!!',
                        'The item is not available, please check the stock.',
                        QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        model_index = table.indexFromItem(i['model_item'])
                        row = model_index.row()
                        quantity_line = table.cellWidget(row, 4)
                        quantity_line.setText('0')


    def discard_stock(self):
        """discard the stock entry"""
        logger.info('Release discard item initiated')
        table = self.release_discardtable
        dataobj = self.get_data_discard()
        if dataobj:
            for i in dataobj:
                discard = self.release_discard
                status = discard.discard(i)
                if not status:
                    msg = QMessageBox.critical(QMessageBox(), 'Fail!!',
                        'Cannot discard item, the quantity or batch does not exist', QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        return False
                else:
                    model_index = table.indexFromItem(i['model_item'])
                    row = model_index.row()
                    table.removeRow(row)
            self.auto_populate_discardtable()

    def select_all_checkboxes_release(self, item):
        """selects all checkboxes in release table"""
        if item == 0:
            r = self.release_releasetable.rowCount()
            for i in range(r):
                chekbox = self.release_releasetable.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def select_all_checkboxes_discard(self, item):
        """sleects all checkboxes in the discard table"""
        if item == 0:
            r = self.release_discardtable.rowCount()
            for i in range(r):
                chekbox = self.release_discardtable.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.release_releasetable
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            dictionary = {}
            chk = table.cellWidget(i, 0)
            if chk.isChecked():
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['code'] = item.text()
                if dictionary['code'] == '':
                    break
                item = table.cellWidget(i, 2).currentText() if table.cellWidget(i, 2) is not None else table.item(i, 2).text()
                dictionary['item'] = item
                item = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
                dictionary['category'] = item.text()
                item = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
                dictionary['units'] = item.text()
                item = table.cellWidget(i, 5) if table.cellWidget(i, 5) is not None else table.item(i, 5)
                dictionary['quantity'] = item.text()
                if dictionary['quantity'] == '':
                    self.show_error('Quantity')
                    return False
                dictionary['model_item'] = table.item(i, 3)
                dataobj.append(dictionary)
        return dataobj

    def get_data_discard(self):
        """
        :return: fetches all the data for printing
        """
        table = self.release_discardtable
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            dictionary = {}
            checkbox = table.cellWidget(i, 0)
            if checkbox.isChecked():
                item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
                dictionary['code'] = item.text()
                if dictionary['code'] == '':
                    break
                item = table.cellWidget(i, 2).currentText() if table.cellWidget(i, 2) is not None else table.item(i, 2).text()
                dictionary['item'] = item
                item = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
                dictionary['category'] = item.text()
                item = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
                dictionary['units'] = item.text()
                item = table.cellWidget(i, 5) if table.cellWidget(i, 5) is not None else table.item(i, 5)
                dictionary['quantity'] = item.text()
                if dictionary['quantity'] == '':
                    self.show_error('Quantity')
                    return False
                item = table.cellWidget(i, 6) if table.cellWidget(i, 6) is not None else table.item(i, 6)
                dictionary['batch_number'] = item.text()
                item = table.cellWidget(i, 7).currentText() if table.cellWidget(i, 7) is not None else table.item(i, 7).text()
                dictionary['reason_for_discard'] = item
                dictionary['model_item'] = table.item(i, 3)
                dataobj.append(dictionary)
        return dataobj

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)

    def just_to_get_focus(self, event):
        """
        just to get focus
        :return:none
        """
        self.add_row_to_releasetable()
        self.add_row_to_discardtable()


class PurchaseSchedule():
    """purhcase shchedule Managment tab"""
    global logger

    def __init__(self):
        #####
        logger.info('Inside PurchaseSchedule')
        self.purchaseSchedule_tab_4 = QWidget()
        self.purchaseSchedule_tab_4.setObjectName("purchaseSchedule_tab_4")
        self.gridLayout_19 = QGridLayout(self.purchaseSchedule_tab_4)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.purchase_schedule_fromdate_label = QLabel(self.purchaseSchedule_tab_4)
        self.purchase_schedule_fromdate_label.setObjectName("purchase_schedule_fromdate_label")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_fromdate_label)
        self.purchase_schedule_fromdate_dateedit = QDateEdit(self.purchaseSchedule_tab_4)
        self.purchase_schedule_fromdate_dateedit.setMinimumDate(QDate.currentDate())
        self.purchase_schedule_fromdate_dateedit.setCalendarPopup(True)
        self.purchase_schedule_fromdate_dateedit.setObjectName("purchase_schedule_fromdate_dateedit")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_fromdate_dateedit)
        self.purchase_schedule_todate_label = QLabel(self.purchaseSchedule_tab_4)
        self.purchase_schedule_todate_label.setObjectName("purchase_schedule_todate_label")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_todate_label)
        self.purchase_schedule_todate_dateedit = QDateEdit(self.purchaseSchedule_tab_4)
        self.purchase_schedule_todate_dateedit.setMinimumDate(QDate.currentDate())
        self.purchase_schedule_todate_dateedit.setCalendarPopup(True)
        self.purchase_schedule_todate_dateedit.setObjectName("purchase_schedule_todate_dateedit")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_todate_dateedit)
        self.purchase_schedule_supplier_label = QLabel(self.purchaseSchedule_tab_4)
        self.purchase_schedule_supplier_label.setObjectName("purchase_schedule_todate_label")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_supplier_label)
        self.purchase_schedule_supplier_combobox = QComboBox(self.purchaseSchedule_tab_4)
        self.purchase_schedule_supplier_combobox.setObjectName("purchase_schedule_supplier_combobox")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_supplier_combobox)
        self.purchase_schedule_search_button = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_schedule_search_button.setObjectName("purchase_schedule_search_button")
        self.horizontalLayout_6.addWidget(self.purchase_schedule_search_button)
        self.gridLayout_19.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.purchase_schedule_table = QTableWidget(self.purchaseSchedule_tab_4)
        self.purchase_schedule_table.setObjectName("purchase_schedule_table")
        self.purchase_schedule_table.setColumnCount(7)
        self.purchase_schedule_table.setRowCount(0)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.purchase_schedule_table.setHorizontalHeaderItem(6, item)
        self.purchase_schedule_table.horizontalHeader().setCascadingSectionResizes(True)
        self.purchase_schedule_table.horizontalHeader().setStretchLastSection(True)
        self.purchase_schedule_table.verticalHeader().setVisible(False)
        self.purchase_schedule_table.verticalHeader().setCascadingSectionResizes(True)
        self.purchase_schedule_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_8.addWidget(self.purchase_schedule_table, 0, 0, 1, 5)
        self.purchase_schedule_add_button = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_schedule_add_button.setObjectName("purchase_schedule_add_button")
        self.gridLayout_8.addWidget(self.purchase_schedule_add_button, 1, 0, 1, 1)
        self.batch_label = QLabel(self.purchaseSchedule_tab_4)
        self.batch_label.setText("Batch Number Of the Order:")
        self.batch_label.setStyleSheet("color:#4B77BE;")
        self.batch_label.setObjectName("batch_label")
        self.gridLayout_8.addWidget(self.batch_label, 1, 1, 1, 1)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem10, 1, 2, 1, 1)
        self.purchase_schedule_print_button = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_schedule_print_button.setObjectName("purchase_schedule_print_button")
        self.gridLayout_8.addWidget(self.purchase_schedule_print_button, 1, 4, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_8, 1, 0, 1, 1)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.purchase_addschedule_today_flatbutton = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_addschedule_today_flatbutton.setObjectName("purchase_addschedule_today_flatbutton")
        self.horizontalLayout_14.addWidget(self.purchase_addschedule_today_flatbutton)
        self.purchase_addschedule_tommorow_flatbutton = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_addschedule_tommorow_flatbutton.setObjectName("purchase_addschedule_tommorow_flatbutton")
        self.horizontalLayout_14.addWidget(self.purchase_addschedule_tommorow_flatbutton)
        self.purchase_addschedule_thisweek_flatbutton = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_addschedule_thisweek_flatbutton.setObjectName("purchase_addschedule_thisweek_flatbutton")
        self.horizontalLayout_14.addWidget(self.purchase_addschedule_thisweek_flatbutton)
        self.purchase_addschedule_thismonth_flatbutton = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_addschedule_thismonth_flatbutton.setObjectName("purchase_addschedule_thismonth_flatbutton")
        self.horizontalLayout_14.addWidget(self.purchase_addschedule_thismonth_flatbutton)
        self.gridLayout_19.addLayout(self.horizontalLayout_14, 2, 0, 1, 1)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.loaded_type = QLabel(self.purchaseSchedule_tab_4)
        self.loaded_type.setStyleSheet("color:#4B77BE;")
        self.loaded_type.setObjectName("loaded_type")
        self.gridLayout_9.addWidget(self.loaded_type, 1, 0, 1, 1)
        spacerItem11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem11, 1, 1, 1, 1)
        self.purchase_addschedule_clear_button = QPushButton(self.purchaseSchedule_tab_4)
        self.purchase_addschedule_clear_button.setObjectName("purchase_addschedule_clear_button")
        self.gridLayout_9.addWidget(self.purchase_addschedule_clear_button, 1, 2, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_9, 3, 0, 1, 1)
        ###retranslate
        self.purchase_schedule_fromdate_label.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_todate_label.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_supplier_label.setText(
            QApplication.translate("MainWindow", "Supplier", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select All", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Unit", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Supplier", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_table.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_add_button.setText(
            QApplication.translate("MainWindow", "Add Item", None, QApplication.UnicodeUTF8))
        self.purchase_schedule_print_button.setText(
            QApplication.translate("MainWindow", "Print", None, QApplication.UnicodeUTF8))
        self.purchase_addschedule_today_flatbutton.setText(
            QApplication.translate("MainWindow", "Today", None, QApplication.UnicodeUTF8))
        self.purchase_addschedule_tommorow_flatbutton.setText(
            QApplication.translate("MainWindow", "Tommorow", None, QApplication.UnicodeUTF8))
        self.purchase_addschedule_thisweek_flatbutton.setText(
            QApplication.translate("MainWindow", "This Week", None, QApplication.UnicodeUTF8))
        self.purchase_addschedule_thismonth_flatbutton.setText(
            QApplication.translate("MainWindow", "This Month", None, QApplication.UnicodeUTF8))
        self.loaded_type.setText(
            QApplication.translate("MainWindow", "Loaded Type", None, QApplication.UnicodeUTF8))
        self.purchase_addschedule_clear_button.setText(
            QApplication.translate("MainWindow", "Clear", None, QApplication.UnicodeUTF8))
        ##signals and slotts && other stuffs
        self.scheduletable_count = 0
        self.addtable_count = 0
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.purchase_schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.batch_number = None
        self.schedule = SchedulePurchase()
        self.supplier = BusinessParty(category='Supplier')
        self.item = ItemProduct()
        self.get_batch()
        self.set_supplier_name()
        self.ob = SchedulePurchase()
        self.purchase_schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.purchase_schedule_search_button.clicked.connect(self.search_schedules)
        self.purchase_schedule_print_button.clicked.connect(self.commit_and_print)
        self.purchase_schedule_add_button.clicked.connect(self.add_new_blank_rows)
        self.purchase_addschedule_clear_button.clicked.connect(self.clear_table)
        self.purchase_addschedule_today_flatbutton.clicked.connect(lambda: self.load_schedules('today'))
        self.purchase_addschedule_tommorow_flatbutton.clicked.connect(lambda: self.load_schedules('tomorrow'))
        self.purchase_addschedule_thisweek_flatbutton.clicked.connect(lambda: self.load_schedules('week'))
        self.purchase_addschedule_thismonth_flatbutton.clicked.connect(lambda: self.load_schedules('month'))
        self.purchase_schedule_table.horizontalHeader().sectionClicked.connect(self.select_all_rows)
        self.purchaseSchedule_tab_4.setFocusPolicy(Qt.StrongFocus)
        self.purchaseSchedule_tab_4.focusInEvent = self.load_rows
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns shortcut entries"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_search']),
                  self.purchaseSchedule_tab_4, self.search_schedules)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_additem']),
                  self.purchaseSchedule_tab_4, self.add_new_blank_rows)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_print']),
                  self.purchaseSchedule_tab_4, self.commit_and_print)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_today']),
                  self.purchaseSchedule_tab_4, lambda: self.load_schedules('today'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_tommorow']),
                  self.purchaseSchedule_tab_4, lambda: self.load_schedules('tomorrow'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_thismonth']),
                  self.purchaseSchedule_tab_4, lambda: self.load_schedules('month'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_thisweek']),
                  self.purchaseSchedule_tab_4, lambda: self.load_schedules('week'))
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorypurchase_clear']),
                  self.purchaseSchedule_tab_4, self.clear_table)

    def get_batch(self):
        """get the batch number for the entry"""
        self.batch_number = self.schedule.get_largest_batch()

    def set_supplier_name(self, *args):
        """
        Populates the suppliers name
        """
        supplierlist = self.purchase_schedule_supplier_combobox
        text = None
        if supplierlist.currentText():
            text = supplierlist.currentText()
        datalist = self.supplier.list_suppliers_with_id()
        datalist[0] = 'All'
        supplierlist.clear()
        supplierlist.addItems(datalist.values())
        if text:
            ind = supplierlist.findText(text)
            supplierlist.setCurrentIndex(ind)

    def add_new_blank_rows(self):
        """
        deletes the schedules in the database
        """
        self.add_schedules('new')

    def add_schedules(self, *args):
        """
        Populates the Schedules when we load the tab
        """
        table = self.purchase_schedule_table
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    check = QCheckBox()
                    table.setCellWidget(i, 0, check)
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 2, item)
                    item = QTableWidgetItem(j['category'])
                    table.setItem(i, 3, item)
                    item = QTableWidgetItem(j['unit'])
                    table.setItem(i, 4, item)
                    supplier = QComboBox()
                    self.populate_suppliers(supplier)
                    if j.get('supplier'):
                        item = supplier
                        index = item.findText(j['supplier'])
                        item.setCurrentIndex(index)
                    table.setCellWidget(i, 5, supplier)
                    line = QLineEdit()
                    line.setValidator(QDoubleValidator(0.000, 999.999, 3))
                    line.setText(j['quantity'])
                    table.setCellWidget(i, 6, line)
            elif args[0] == 'new':
                row = table.rowCount() + 1
                table.setRowCount(row)
                check = QCheckBox()
                table.setCellWidget(row - 1, 0, check)
                codeline = QLineEdit()
                codeline.editingFinished.connect(lambda: self.get_details_of_code(row))
                table.setCellWidget(row - 1, 1, codeline)
                itemcombo = QComboBox()
                self.fill_item_list(itemcombo)
                itemcombo.currentIndexChanged.connect(lambda: self.get_details_of_item(row))
                table.setCellWidget(row - 1, 2, itemcombo)
                item = QTableWidgetItem()
                table.setItem(row - 1, 3, item)
                unit = QTableWidgetItem()
                table.setItem(row - 1, 4, unit)
                supplier = QComboBox()
                self.populate_suppliers(supplier)
                table.setCellWidget(row - 1, 5, supplier)
                quantity = QLineEdit()
                quantity.setValidator(QDoubleValidator(0.000, 999.999, 3))
                table.setCellWidget(row - 1, 6, quantity)
        table.setColumnWidth(0, table.width() / 9)
        table.setColumnWidth(1, table.width() / 7)
        table.setColumnWidth(2, table.width() / 7)
        table.setColumnWidth(3, table.width() / 7)
        table.setColumnWidth(4, table.width() / 7)
        table.setColumnWidth(5, table.width() / 7)

    def populate_suppliers(self, combo):
        """
        fills the supplier list for each item line
        :param combo: the combo box of suppliers
        :return:none
        """
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        datalist = self.supplier.list_suppliers_with_id()
        itemfield.addItems(datalist.values())

    def fill_item_list(self, combo):
        """
        fill the item combo box
        :param combo: the combobox object
        :return: none
        """
        itemfield = combo
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")

        itemfield.addItems(self.item.fill_item_list())

    def get_details_of_code(self, rowcount):
        """
        fills the item, category and units based on the code
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.purchase_schedule_table
        codeline = table.cellWidget(row, 1)
        data = self.item.get_details_of_code(codeline.text())
        item = table.cellWidget(row, 2)
        index = item.findText(data['item'])
        item.setCurrentIndex(index)
        category = table.item(row, 3)
        category.setText(data['category'])
        units = table.item(row, 4)
        units.setText(data['units'])
        if data.get('supplier'):
            item = table.cellWidget(row, 5)
            index = item.findText(data['supplier'])
            item.setCurrentIndex(index)

    def get_details_of_item(self, rowcount):
        """
        fills the code, category and units based on the item
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.purchase_schedule_table
        itemcombo = table.cellWidget(row, 2)
        data = self.item.get_details_of_item(itemcombo.currentText())
        code = table.cellWidget(row, 1)
        code.setText(data['code'])
        category = table.item(row, 3)
        category.setText(data['category'])
        units = table.item(row, 4)
        units.setText(data['units'])
        if data.get('supplier'):
            item = table.cellWidget(row, 5)
            index = item.findText(data['supplier'])
            item.setCurrentIndex(index)

    def search_schedules(self):
        """
        Searches for schedules when search button is pressed
        """
        logger.info('PurchaseSchedule searching schedule initiated')
        from_date = self.purchase_schedule_fromdate_dateedit.text()
        to_date = self.purchase_schedule_todate_dateedit.text()
        from_date = from_date.split('/')
        from_date.reverse()
        from_date = "-".join(from_date)
        to_date = to_date.split('/')
        to_date.reverse()
        to_date = "-".join(to_date)
        supplier = self.purchase_schedule_supplier_combobox.currentText()
        dataobj = self.ob.load_schedules(from_date, to_date, supplier=supplier)
        if dataobj:
            self.add_schedules(*dataobj)
        else:
            self.purchase_schedule_table.clearContents()
            self.purchase_schedule_table.setRowCount(0)
        self.set_supplier_name()

    def load_schedules(self, load_type):
        """
        loads schedule according to the load_type
        :param load_type: today, tomorrow,week(this week),month(this month)
        :return:none
        """
        logger.info('PurchaseSchedule load_schedule initiated')
        dataobj = None
        table = self.purchase_schedule_table
        row = table.rowCount()
        for i in range(row):
            widget = table.cellWidget(i, 1)
            if widget:
                msg = QMessageBox.critical(QMessageBox(), "Warning!!",
                    "This will remove all the added rows are you sure?",
                    QMessageBox.Ok | QMessageBox.Cancel)
                if msg == QMessageBox.Ok:
                    break
                else:
                    return False
        load_type = load_type

        if load_type == 'today':
            date = (datetime.today()).strftime("%Y-%m-%d")
            dataobj = self.ob.load_schedules(date, date)
            self.loaded_type.setText("Today's Requirement")
        elif load_type == 'tomorrow':
            date = datetime.today() + timedelta(days=1)
            date = (date).strftime("%Y-%m-%d")
            dataobj = self.ob.load_schedules(date, date)
            self.loaded_type.setText("Tomorrow's Requirement")
        elif load_type == 'week':
            start_date = datetime.today()
            end_date = datetime.today() + timedelta(days=7)
            dataobj = self.ob.load_schedules(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            self.loaded_type.setText("This Weeks's Requirement")
        else:
            start_date = datetime.today()
            end_date = datetime.today() + timedelta(days=30)
            dataobj = self.ob.load_schedules(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            self.loaded_type.setText("This Month's Requirement")
        if dataobj:
            print dataobj
            self.add_schedules(*dataobj)

    def select_all_rows(self, item):
        """selects all row entries"""
        if item == 0:
            r = self.purchase_schedule_table.rowCount()
            for i in range(r):
                chekbox = self.purchase_schedule_table.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def commit_and_print(self):
        """
        saves the details in db before printing
        """
        logger.info('PurchaseSchedule committing schedule initiated')
        data = self.get_data()
        batch_to_show = []
        table = self.purchase_schedule_table
        if data:
            self.batch_label.setText("Batch Number Of the Order:")
            for i, j in data.iteritems():
                yearandmonth = datetime.today().strftime("%y%m")
                batch = self.batch_number
                if not batch:
                    batch = "%s000" % yearandmonth
                else:
                    batch_list = list(batch)
                    compare = "".join([batch_list[0], batch_list[1], batch_list[2], batch_list[3]])
                    if compare >= yearandmonth:
                        digit = "".join([batch_list[4], batch_list[5], batch_list[6]])
                        if digit == "999":
                            digit = "000"
                        else:
                            digit = "%03d" % (int(digit) + 1)
                        batch = "%s%s" % (compare, digit)
                    else:
                        batch = "%s000" % yearandmonth
                print batch
                to_print = [j, batch]
                dialog = QPrintDialog()
                if dialog.exec_() == QDialog.Accepted:
                    status = self.schedule.save_purchase(j, batch)
                    if status:
                        p = dialog.printer()
                        self.batch_number = batch
                        batch_to_show.append(batch)
                        print p.printerName()
                        printing = PrintNow(p.printerName(), to_print, 'purchase')
                        try:
                            printing.start_print()
                        except Exception, e:
                            msg = QMessageBox.critical(QMessageBox(), "Print error!!",
                                "The printer was not properly connected!!",
                                QMessageBox.Ok)
                            if msg == QMessageBox.Ok:
                                pass
                        for l in j:
                            model_index = table.indexFromItem(l['model_item'])
                            row = model_index.row()
                            table.removeRow(row)
                    else:
                        msg = QMessageBox.critical(QMessageBox(), "Fail!!",
                            "The Purchase could not be saved!!",
                            QMessageBox.Ok)
                        if msg == QMessageBox.Ok:
                            return False
        text1 = self.batch_label.text()
        text2 = ",".join(batch_to_show)
        self.batch_label.setText("%s%s" % (text1, text2))

    def clear_table(self):
        """
        Clear table entries
        """
        msg = QMessageBox.critical(QMessageBox(), 'Warning!!', 'This will clear all rows.',
            QMessageBox.Ok | QMessageBox.Cancel)
        if msg == QMessageBox.Ok:
            table = self.purchase_schedule_table
            table.clearContents()
            table.setRowCount(0)

    def load_rows(self, event):
        """
        :return:loads the rows
        """
        self.add_schedules()

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.purchase_schedule_table
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            print "issue"
            chekbox = self.purchase_schedule_table.cellWidget(i, 0)
            if not chekbox.isChecked():
                continue
            else:
                pass
            dictionary = {}
            item = table.cellWidget(i, 1) if table.cellWidget(i, 1) is not None else table.item(i, 1)
            dictionary['code'] = item.text()
            if dictionary['code'] == '':
                break
            item = table.cellWidget(i, 2).currentText() if table.cellWidget(i, 2) is not None else table.item(i, 2).text()
            dictionary['item'] = item
            item = table.cellWidget(i, 3).currentText() if table.cellWidget(i, 3) is not None else table.item(i, 3).text()
            dictionary['category'] = item
            item = table.cellWidget(i, 4).currentText() if table.cellWidget(i, 4) is not None else table.item(i, 4).text()
            dictionary['units'] = item
            item = table.cellWidget(i, 5).currentText() if table.cellWidget(i, 5) is not None else table.item(i, 5).text()
            dictionary['supplier'] = item
            item = table.cellWidget(i, 6) if table.cellWidget(i, 6) is not None else table.item(i, 6)
            dictionary['quantity'] = item.text()
            if dictionary['quantity'] == '':
                self.show_error('Quantity')
                return False
            if dictionary['quantity'] == '0':
                continue
            dictionary['model_item'] = table.item(i, 3)
            dataobj.append(dictionary)
        data = self.group_schedule_with_supplier(dataobj)
        return data

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)

    def group_schedule_with_supplier(self, dataobj):
        """
        groups the table data according to the supplier
        :param dataobj: the list of dictionary from getdata
        :return:arranged list of dictionary
        """
        dataobj = dataobj
        supplier = []
        for i in dataobj:
            if not supplier:
                supplier.append(i['supplier'])
            else:
                if i['supplier'] in supplier:
                    continue
                else:
                    supplier.append(i['supplier'])
        data = defaultdict(list)
        for n, i in enumerate(supplier):
            for j in dataobj:
                if j['supplier'] == i:
                    data[n].append(j)
        return data


class Supplier():
    """Supplier Managment tab"""
    global logger

    def __init__(self):
        ####
        logger.info('Inside Supplier')
        self.supplier_tab_5 = QWidget()
        self.supplier_tab_5.setObjectName("supplier_tab_5")
        self.gridLayout_11 = QGridLayout(self.supplier_tab_5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.supplier_table = QTableWidget(self.supplier_tab_5)
        self.supplier_table.setObjectName("supplier_table")
        self.supplier_table.setColumnCount(3)
        self.supplier_table.setRowCount(0)
        item = QTableWidgetItem()
        self.supplier_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.supplier_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.supplier_table.setHorizontalHeaderItem(2, item)
        self.supplier_table.horizontalHeader().setCascadingSectionResizes(True)
        self.supplier_table.horizontalHeader().setStretchLastSection(True)
        self.supplier_table.verticalHeader().setVisible(False)
        self.supplier_table.verticalHeader().setCascadingSectionResizes(True)
        self.supplier_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_10.addWidget(self.supplier_table, 0, 0, 1, 3)
        spacerItem12 = QSpacerItem(78, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem12, 1, 1, 1, 1)
        self.supplier_add_button = QPushButton(self.supplier_tab_5)
        self.supplier_add_button.setObjectName("supplier_add_button")
        self.gridLayout_10.addWidget(self.supplier_add_button, 1, 2, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        ###retranslate
        self.supplier_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.supplier_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Name", None, QApplication.UnicodeUTF8))
        self.supplier_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Address", None, QApplication.UnicodeUTF8))
        self.supplier_add_button.setText(
            QApplication.translate("MainWindow", "Add", None, QApplication.UnicodeUTF8))
        ###signals & slots and other stuffs
        self.suppliertable_count = 0
        self.search = BusinessParty(category='Supplier')
        self.supplier_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.supplier_add_button.clicked.connect(self.add_new_supplier)
        self.supplier_table.itemDoubleClicked.connect(self.row_clicked)
        # self.get_suppliers()
        self.supplier_tab_5.setFocusPolicy(Qt.StrongFocus)
        self.supplier_tab_5.focusInEvent = self.load_rows
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns shortucts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorysupplier_add']),
                  self.supplier_tab_5, self.add_new_supplier)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventorysupplier_view']),
                  self.supplier_tab_5, self.row_selected)

    def row_selected(self):
        """checks the selected row"""
        rows = sorted(set(index.row() for index in
                          self.supplier_table.selectedIndexes()))
        if rows:
            self.add_new_supplier(self.supplier_table.item(rows[0], 0))

    def get_suppliers(self):
        """
        populate the suppliers from db
        """
        logger.info('Supplier Searching for suppliers')
        search_list = self.search.load_suppliers()
        self.add_rows(*search_list)


    def add_rows(self, *args):
        """
        adds a new row to the supplier table
        """
        table = self.supplier_table
        if args:
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                item = QTableWidgetItem(j['code'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(j['name'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(j['address'])
                table.setItem(i, 2, item)
        table.setColumnWidth(0, table.width() / 5.5)
        table.setColumnWidth(1, table.width() / 5.5)
        table.setColumnWidth(2, table.width() / 2.5)

    def add_new_supplier(self, *args):
        """
        save new suppliers to the db
        """
        if not args:
            supplier = SupplierAddDialog(parent=self, category='Supplier')
        else:
            supplier = SupplierAddDialog(parent=self, code=args[0], category='Supplier')
        supplier.exec_()

    def row_clicked(self, item):
        """
        Pops up the supplier to be edited
        :param item: item clicked
        :return:none
        """
        model_index = self.supplier_table.indexFromItem(item)
        row = model_index.row()
        self.add_new_supplier(self.supplier_table.item(row, 0))

    def load_rows(self, event):
        """
        :return: adds the rows
        """
        self.get_suppliers()


class SupplierAddDialog(QDialog):  # overloading in Billing
    """popup to add new supplier"""
    global logger

    def __init__(self, parent=None, code=None, category=None):
        logger.info('Inside %s' % self.__class__.__name__)
        QDialog.__init__(self)
        self.parent = parent
        self.dialogue = Ui_Supplier_Add()
        self.dialogue.setupUi(self)
        self.code = False
        self.dialogue.supplieradd_save_button.clicked.connect(self.save_supplier)
        self.supplier = BusinessParty(category=category)
        self.category = 'Supplier'
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.dialogue.supplieradd_delete_button.clicked.connect(self.delete_supplier)
        self.dialogue.supplieradd_code_linedit.setValidator(QDoubleValidator(1, 99999, 5))
        self.dialogue.supplieradd_name_linedit.textChanged.connect(
            lambda: self.auto_capital(self.dialogue.supplieradd_name_linedit))
        if code:
            self.code = code.text()
            self.load_supplier(code.text())
            self.dialogue.supplieradd_code_linedit.setDisabled(True)
        else:
            self.dialogue.supplieradd_code_linedit.setPlaceholderText('Not Assigned')

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def load_supplier(self, code):
        """
        loads the supplier
        :param code: The code of the supplier
        :return:None
        """
        newcode = code
        supplier_data = self.supplier.get_supplier(newcode)
        self.dialogue.supplieradd_name_linedit.setText(supplier_data['name'])
        self.dialogue.supplieradd_street_linedit.setText(supplier_data['street'])
        self.dialogue.supplieradd_city_linedit.setText(supplier_data['city'])
        self.dialogue.supplieradd_pin_linedit.setText(supplier_data['zip'])
        self.dialogue.supplieradd_code_linedit.setText(supplier_data['pan'])

    def save_supplier(self):
        """
        saves the Supplier details
        :return:None
        """
        logger.info('%s saving supplier initiated' % self.__class__.__name__)
        dictonary = {}
        dictonary['name'] = self.dialogue.supplieradd_name_linedit.text()
        dictonary['street'] = self.dialogue.supplieradd_street_linedit.text()
        dictonary['city'] = self.dialogue.supplieradd_city_linedit.text()
        dictonary['zip'] = self.dialogue.supplieradd_pin_linedit.text()
        dictonary['pan'] = self.dialogue.supplieradd_code_linedit.text()
        for i, j in dictonary.iteritems():
            if not j:
                QMessageBox.critical(QMessageBox(), 'Error!!!', 'The value of %s is invalid' % i.title(),
                    QMessageBox.Ok)
                return False
        if self.code:
            save = self.supplier.edit_supplier(dictonary)
        else:
            save = self.supplier.create_supplier(dictonary)
        if save:
            if self.parent:
                self.parent.get_suppliers()
            self.dialogue.supplieradd_code_linedit.setDisabled(True)
            self.code = dictonary['pan']
            response = QMessageBox.information(
                self, "Success!!", "The %s has been saved successfully, do you want to close this?" % self.category,
                                   QMessageBox.Cancel | QMessageBox.Ok)
            if response == QMessageBox.Ok:
                self.close()
        else:
            QMessageBox.critical(self, "Failure!!", "The %s was not saved!!!Duplicate code Entry" % self.category
                                 , QMessageBox.Ok)

    def delete_supplier(self):
        """deletes a supplier entry"""
        logger.info('%s deleting supplier initiated' % self.__class__.__name__)
        if self.code:
            ask = QMessageBox.question(self, "Confirm!!", "The current %s be deleted" % self.category,
                                       QMessageBox.Yes | QMessageBox.No)
            if ask == QMessageBox.Yes:
                status = self.supplier.delete_supplier(self.code)
                if status[0]:
                    QMessageBox.information(self, "Success!!", "%s" % status[1],
                                            QMessageBox.Ok)
                    if self.parent:
                        self.parent.get_suppliers()
                else:
                    QMessageBox.critical(self, 'Failure!!', '%s' % status[1], QMessageBox.Ok)
                self.close()


class Item():
    """Ingredient Item Managment Tab"""
    global logger

    def __init__(self):
        ####
        logger.info('Inside Item')
        self.itemdetail_tab_6 = QWidget()
        self.itemdetail_tab_6.setObjectName("itemdetail_tab_6")
        self.gridLayout_20 = QGridLayout(self.itemdetail_tab_6)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.item_table = QTableWidget(self.itemdetail_tab_6)
        self.item_table.setSortingEnabled(True)
        self.item_table.setObjectName("item_table")
        self.item_table.setColumnCount(4)
        self.item_table.setRowCount(0)
        item = QTableWidgetItem()
        self.item_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.item_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.item_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.item_table.setHorizontalHeaderItem(3, item)
        self.item_table.horizontalHeader().setCascadingSectionResizes(False)
        self.item_table.horizontalHeader().setStretchLastSection(True)
        self.item_table.verticalHeader().setVisible(True)
        self.item_table.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout_20.addWidget(self.item_table, 0, 0, 1, 2)
        spacerItem22 = QSpacerItem(612, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_20.addItem(spacerItem22, 1, 0, 1, 1)
        self.item_table_add_button = QPushButton(self.itemdetail_tab_6)
        self.item_table_add_button.setObjectName("item_table_add_button")
        self.gridLayout_20.addWidget(self.item_table_add_button, 1, 1, 1, 1)
        ####retranslate
        self.item_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.item_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.item_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.item_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Rate", None, QApplication.UnicodeUTF8))
        self.item_table_add_button.setText(
            QApplication.translate("MainWindow", "Add New Item", None, QApplication.UnicodeUTF8))
        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.item = ItemProduct()
        self.item_table_add_button.clicked.connect(self.add_item)
        self.item_table.itemDoubleClicked.connect(self.popup_edit)
        self.item_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.item_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.item_table.setShowGrid(False)
        self.item_table.setAlternatingRowColors(True)
        # self.update_item()
        self.popup = object
        self.itemdetail_tab_6.setFocusPolicy(Qt.StrongFocus)
        self.itemdetail_tab_6.focusInEvent = self.load_rows
        self.update_item()
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns shortucts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryitem_addnewitem']),
                  self.itemdetail_tab_6, self.add_item)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_inventoryitem_view']),
                  self.itemdetail_tab_6, self.row_selected)

    def row_selected(self):
        """check the row selected"""
        rows = sorted(set(index.row() for index in
                          self.item_table.selectedIndexes()))
        if rows:
            self.add_item(self.item_table.item(rows[0], 0))

    def add_item(self, *args):
        """
        :return: Pops up a new dialogue to add the items
        """
        if not args:
            self.popup = ItemAddDialogue(parent=self)
            self.popup.exec_()
        else:
            self.popup = ItemAddDialogue(parent=self, code=args[0])
            self.popup.exec_()

    def update_item(self):
        """
        :return:Populates the item table
        """
        logger.info('Item loading items')
        itemlist = self.item.load_items()
        if not itemlist == []:
            self.add_row(*itemlist)
        else:
            self.item_table.clearContents()
            self.item_table.setRowCount(0)

    def popup_edit(self, item):
        """
        Pops up the item to be edited
        :param item: item clicked
        :return:none
        """
        model_index = self.item_table.indexFromItem(item)
        row = model_index.row()
        self.add_item(self.item_table.item(row, 0))

    def add_row(self, *args):
        """adds new row table"""
        table = self.item_table
        if args:
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                item = QTableWidgetItem(j['item_no'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(j['item'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(j['category'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(j['rate'])
                table.setItem(i, 3, item)
        table.setColumnWidth(0, table.width() / 3.5)
        table.setColumnWidth(1, table.width() / 3.5)
        table.setColumnWidth(2, table.width() / 3.5)

    def load_rows(self, event):
        """
        :return:checks and adds new rows
        """
        self.add_row()


class ItemAddDialogue(QDialog):
    """popup to add new Item"""
    global logger

    def __init__(self, parent=None, code=None):
        logger.info('Inside ItemAddDialogue')
        QDialog.__init__(self)
        self.parent = parent
        self.dialogue = Ui_new_item()
        self.dialogue.setupUi(self)
        self.dialogue.itemdialogue_delete_button.clicked.connect(self.delete_item_item)
        self.dialogue.itemdialogue_additem_button.clicked.connect(self.add_item)
        self.row_count = 0
        self.search = CategoryOfProduct()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.editable = False
        self.itemproduct = ItemProduct()
        self.dialogue.itemdialogue_rate_lineedit.setValidator(QDoubleValidator(1.000, 999.000, 3))
        self.dialogue.itemdialogue_codenumber_lineedit.setValidator(QIntValidator(0, 99999999))
        self.dialogue.itemdialogue_itemname_lineedit.textChanged.connect(
            lambda: self.auto_capital(self.dialogue.itemdialogue_itemname_lineedit))
        self.dialogue.itemdialogue_newcategory_button.clicked.connect(self.popup_category)
        self.complete_unit()
        self.complete_category()
        self.id = None
        self.dialogue.itemdialogue_addsuplier_button.clicked.connect(self.add_supplier_popup)
        self.dialogue.itemdialogue_supplier_table.itemDoubleClicked.connect(self.popup_delete)
        self.dialogue.itemdialogue_supplier_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if not code:
            self.dialogue.itemdialogue_delete_button.setDisabled(True)
            self.dialogue.itemdialogue_delete_button.setToolTip("Cannot Delete Item which is not added")
            self.dialogue.itemdialogue_codenumber_lineedit.setPlaceholderText('Not Assigned')
            self.dialogue.itemdialogue_addsuplier_button.setDisabled(True)
            self.dialogue.itemdialogue_addsuplier_button.setToolTip("Please Save before adding a supplier")
        else:
            self.editable = True
            self.dialogue.itemdialogue_itemunit_combobox.setDisabled(True)
            self.setWindowTitle('Edit Item')
            self.dialogue.itemdialogue_additem_button.setText('Save')
            self.id = code.text()
            self.dialogue.itemdialogue_codenumber_lineedit.setText(self.id)
            self.load_rows(self.id)
            self.load_supplier_table()

    def complete_category(self, event=None):
        """
        fills the category in the combobox
        :return:none
        """
        itemfield = self.dialogue.itemdialogue_itemcategory_combobox
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        itemfield.clear()
        itemfield.addItems(self.search.search_categories())

    def complete_unit(self):
        """
        fills the unit
        :return:none
        """
        unitfield = self.dialogue.itemdialogue_itemunit_combobox
        unitfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        search = self.itemproduct
        unitfield.addItems(search.complete_unit())

    def delete_item_item(self):
        """
        :return: deletes the current item from the item
        """
        ask = QMessageBox.question(self, "Confirm!!", "The current item item will be deleted",
                                   QMessageBox.Yes | QMessageBox.No)
        if ask == QMessageBox.Yes:
            logger.info('ItemAddDialogue deleting item initiated')
            todelete = self.itemproduct
            status = todelete.delete_rows(self.id)
            if status[0]:
                QMessageBox.information(self, "Success!!", "%s" % status[1],
                                        QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Failure!!', '%s' % status[1], QMessageBox.Ok)
            self.close()
            self.parent.update_item()

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def load_rows(self, *args):
        """
        :param args:item code
        :return:Loads the rows from the database
        """
        loadrows = self.itemproduct
        row = loadrows.load_rows(id=args[0])
        self.dialogue.itemdialogue_itemname_lineedit.setText(row['name'])
        combo = self.dialogue.itemdialogue_itemcategory_combobox.findText(row['category'])
        self.dialogue.itemdialogue_itemcategory_combobox.setCurrentIndex(combo)
        combo = self.dialogue.itemdialogue_itemunit_combobox.findText(row['units'])
        self.dialogue.itemdialogue_itemunit_combobox.setCurrentIndex(combo)
        self.dialogue.itemdialogue_rate_lineedit.setText(row['rate'])

    def add_item(self):
        """
        adds the new item item
        :return:none
        """
        logger.info('ItemAddDialogue saving item initiated')
        name = self.dialogue.itemdialogue_itemname_lineedit.text()
        rate = self.dialogue.itemdialogue_rate_lineedit.text()
        code = self.id if self.id else self.dialogue.itemdialogue_codenumber_lineedit.text()
        category = self.dialogue.itemdialogue_itemcategory_combobox.currentText()
        units = self.dialogue.itemdialogue_itemunit_combobox.currentText()
        if (name and category and rate and code and units) == '':
            QMessageBox.critical(self, "Failure!!", "Enter proper values",
                                 QMessageBox.Ok)
            return False
        obj = {'name': name, 'rate': rate, 'id': code, 'category': category, 'units': units}
        additem = self.itemproduct
        if self.editable:
            ret = additem.save_item(obj)
        else:
            ret = additem.create_item(obj)
        if not ret:
            QMessageBox.critical(self, "Failure!!", "Duplicate Entry found",
                                 QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Success!!", "The Item was saved", QMessageBox.Ok)
            self.setWindowTitle('Edit Item')
            self.dialogue.itemdialogue_additem_button.setText('Save')
            self.id = code
            self.dialogue.itemdialogue_itemunit_combobox.setDisabled(True)
            self.dialogue.itemdialogue_codenumber_lineedit.setText(self.id)
            self.dialogue.itemdialogue_delete_button.setDisabled(False)
            self.dialogue.itemdialogue_delete_button.setToolTip("Deletes item")
            self.dialogue.itemdialogue_addsuplier_button.setDisabled(False)
            self.dialogue.itemdialogue_addsuplier_button.setToolTip("Adds a Supplier")
            self.editable = True
        self.parent.update_item()

    def popup_category(self):
        """
        pops up a dialogue for category
        :return:none
        """
        category = CategoryAddDialogue()
        category.exec_()
        self.complete_category()
        settext = category.category.categorydialogue_newcategory_linedit.text()
        itemfield = self.dialogue.itemdialogue_itemcategory_combobox
        index = itemfield.findText(settext)
        itemfield.setCurrentIndex(index)

    def add_supplier_popup(self):
        """
        pops up a supplier list to be added
        :return:none, but updates the table in with the parent object passed to the object
        """
        if self.id:
            logger.info('ItemAddDialogue supplier add initiated')
            ob = NewItemSupplierDialogue(parent=self, code=self.id)
            ob.exec_()
        else:
            QMessageBox.critical(self, "Error!!", "Please add the item before adding the supplier",
                                 QMessageBox.Ok)

    def load_supplier_table(self):
        """
        loads the supplier table data
        :return: none
        """
        search = self.itemproduct
        data = search.load_supplier_table(self.id)
        self.add_rows(data)

    def add_rows(self, data):
        """
        adds the rows to the supplier table
        :param data: list of dictionary
        :return: none
        """
        table = self.dialogue.itemdialogue_supplier_table
        if data:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(data))
            table.setStyleSheet("color:#000000;")
            for n, i in enumerate(data):
                item = QTableWidgetItem(i['code'])
                table.setItem(n, 0, item)
                name = QTableWidgetItem(i['name'])
                table.setItem(n, 1, name)
        table.setColumnWidth(0, table.width() / 2.5)

    def popup_delete(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        ask = QMessageBox.critical(self, "Warning!!", "This will delete the Supplier",
                                   QMessageBox.Ok | QMessageBox.Cancel)
        if ask == QMessageBox.Ok:
            logger.info('ItemAddDialogue deleting supplier initiated')
            table = self.dialogue.itemdialogue_supplier_table
            model_index = table.indexFromItem(item)
            row = model_index.row()
            code = table.item(row, 0).text()
            item = self.itemproduct
            status = item.delete_supplier_from_item(code=self.id, pan=code)
            if status:
                QMessageBox.information(self, "Success!!", "The Supplier was Deleted", QMessageBox.Ok)
                table.removeRow(row)
            else:
                QMessageBox.critical(self, "Failure!!", "The Supplier was not Deleted",
                                     QMessageBox.Ok)


class CategoryAddDialogue(QDialog):
    """popup to add new category"""
    global logger

    def __init__(self):
        logger.info('Inside CategoryAddDialogue')
        QDialog.__init__(self)
        self.category = Ui_new_category()
        self.category.setupUi(self)
        self.newcategory = CategoryOfProduct()
        self.category.categorydialogue_newcategory_linedit.textChanged.connect(
            lambda: self.auto_capital(self.category.categorydialogue_newcategory_linedit))
        self.category.categorydialogue_addcategory_button.clicked.connect(self.add_category)

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def add_category(self):
        """
        adds a new category to the category types
        :return: none
        """
        logger.info('CategoryAddDialogue add category initiated')
        status = self.newcategory.create_category(self.category.categorydialogue_newcategory_linedit.text())
        if status:
            QMessageBox.information(self, "Success!!", "The Category was saved", QMessageBox.Ok)
            self.close()
        else:
            QMessageBox.critical(self, "Failure!!", "The Category was not saved, may be duplicate",
                                 QMessageBox.Ok)


class NewItemSupplierDialogue(QDialog):
    """popup to add new supplier to an item"""
    global logger

    def __init__(self, parent=None, code=None):
        logger.info('Inside NewItemSupplierDialogue')
        QDialog.__init__(self)
        self.dialog = Ui_new_supplier()
        self.dialog.setupUi(self)
        self.supplier = BusinessParty(category='Supplier')
        self.add = ItemProduct()
        self.parent = parent
        self.supplier_list = None
        self.code = code
        self.dialog.newsupplier_name_combobox.currentIndexChanged.connect(lambda: self.change_label())
        self.dialog.newsupplier_add_button.clicked.connect(self.add_supplier)
        self.set_supplier_name()


    def set_supplier_name(self):
        """
        Populates the suppliers name
        """
        supplierlist = self.dialog.newsupplier_name_combobox
        supplierlist.setStyleSheet("QAbstractItemView{"
                                   "background: #4B77BE;"
                                   "}")
        self.supplier_list = self.supplier.list_suppliers_with_id()
        supplierlist.clear()
        supplierlist.addItems(self.supplier_list.values())

    def change_label(self):
        """
        changes the label according to the supplier selected
        :return: none
        """
        com = self.dialog.newsupplier_name_combobox.currentText()
        for i, j in self.supplier_list.iteritems():
            if j == com:
                self.dialog.newsupplier_code_label.setText(i)

    def add_supplier(self):
        """
        adds the supplier to the product_suppliers of the item
        :return:none
        """
        logger.info('NewItemSupplierDialogue supplier save initiated')
        pan = self.dialog.newsupplier_code_label.text()
        if pan.isdigit():
            state = self.add.add_supplier_to_item(code=self.code, pan=pan)
            if state:
                QMessageBox.information(self, "Success!!", "The Supplier was saved", QMessageBox.Ok)
                self.parent.load_supplier_table()
                self.close()
            else:
                QMessageBox.critical(self, "Failure!!", "The Supplier was not saved, may be duplicate",
                                     QMessageBox.Ok)
