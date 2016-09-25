#! /usr/bin/env python

""" Waste Module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from datetime import datetime, timedelta

from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QTableWidget, QPushButton, QAbstractItemView, QLabel, QDateEdit, QLineEdit, \
    QMessageBox, QComboBox, QVBoxLayout

from PySide.QtCore import Qt, QDate
from inventory.inventory_tryton import BusinessParty, SchedulePurchase, AddStockInventory
from waste_tryton import WasteMenu, WasteIngredients
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class Waste():
    """Waste management main container"""
    def __init__(self):
        ####
        self.waste_tab_6 = QWidget()
        self.waste_tab_6.setStyleSheet("")
        self.waste_tab_6.setObjectName("waste_tab_6")
        self.verticalLayout = QVBoxLayout(self.waste_tab_6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.waste_detail_tabWidget = QTabWidget(self.waste_tab_6)
        self.waste_detail_tabWidget.setObjectName("waste_detail_tabWidget")
        self.add_tabs()
        self.verticalLayout.addWidget(self.waste_detail_tabWidget)

        ##signals and slotts && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.waste_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.waste_tab_6.setFocusPolicy(Qt.StrongFocus)
        self.waste_tab_6.focusInEvent = self.change_focus

    def add_tabs(self):
        """
        :return: adds new tabs
        """
        dish = WasteDish()
        self.waste_detail_tabWidget.addTab(dish.wastedetail_tab_1, "Dish Waste")
        item = WasteItems()
        self.waste_detail_tabWidget.addTab(item.wastedetail_tab_1, "Item Waste")


    def change_focus(self, event=None):
        """captures focus to inititate the events for the coprresponding tab"""
        wid = self.waste_detail_tabWidget.currentWidget()
        if wid.isVisible():
            wid.setFocus()


class WasteDish():
    """Dish waste management tab"""
    global logger

    def __init__(self):
        ###
        logger.info('Inside WasteDish')
        self.wastedetail_tab_1 = QWidget()
        self.wastedetail_tab_1.setObjectName("wastedetail_tab_1")
        self.verticalLayout_9 = QVBoxLayout(self.wastedetail_tab_1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.waste_fromdate_label = QLabel(self.wastedetail_tab_1)
        self.waste_fromdate_label.setObjectName('waste_fromdate_label')
        self.horizontalLayout_12.addWidget(self.waste_fromdate_label)
        self.waste_fromdate_dateedit = QDateEdit(self.wastedetail_tab_1)
        self.waste_fromdate_dateedit.setCalendarPopup(True)
        self.waste_fromdate_dateedit.setObjectName("waste_fromdate_dateedit")
        self.horizontalLayout_12.addWidget(self.waste_fromdate_dateedit)
        self.waste_todate_label = QLabel(self.wastedetail_tab_1)
        self.waste_todate_label.setObjectName('waste_todate_label')
        self.horizontalLayout_12.addWidget(self.waste_todate_label)
        self.waste_todate_dateedit = QDateEdit(self.wastedetail_tab_1)
        self.waste_todate_dateedit.setCalendarPopup(True)
        self.waste_todate_dateedit.setObjectName("waste_todate_dateedit")
        self.waste_todate_dateedit.setMaximumDate(QDate.currentDate())
        self.horizontalLayout_12.addWidget(self.waste_todate_dateedit)
        spacerItem28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem28)
        self.waste_table_search_button = QPushButton(self.wastedetail_tab_1)
        self.waste_table_search_button.setObjectName("waste_table_search_button")
        self.horizontalLayout_12.addWidget(self.waste_table_search_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.waste_table = QTableWidget(self.wastedetail_tab_1)
        self.waste_table.setObjectName("waste_table")
        self.waste_table.setColumnCount(5)
        self.waste_table.setRowCount(0)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(4, item)
        self.waste_table.horizontalHeader().setCascadingSectionResizes(False)
        self.waste_table.horizontalHeader().setStretchLastSection(True)
        self.waste_table.verticalHeader().setVisible(False)
        self.waste_table.verticalHeader().setCascadingSectionResizes(False)
        self.waste_table.setSortingEnabled(True)
        self.verticalLayout_8.addWidget(self.waste_table)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.waste_table_newrow_button = QPushButton(self.wastedetail_tab_1)
        self.waste_table_newrow_button.setObjectName("waste_table_newrow_button")
        self.horizontalLayout_13.addWidget(self.waste_table_newrow_button)
        spacerItem29 = QSpacerItem(612, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem29)
        self.waste_table_discard_button = QPushButton(self.wastedetail_tab_1)
        self.waste_table_discard_button.setObjectName("waste_table_discard_button")
        self.horizontalLayout_13.addWidget(self.waste_table_discard_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        ##retranslate
        self.waste_fromdate_label.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.waste_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.waste_todate_label.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.waste_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.waste_table_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Reason", None, QApplication.UnicodeUTF8))
        self.waste_table_newrow_button.setText(
            QApplication.translate("MainWindow", "New Row", None, QApplication.UnicodeUTF8))
        self.waste_table_discard_button.setText(
            QApplication.translate("MainWindow", "Discard Item", None, QApplication.UnicodeUTF8))
        self.wastedetail_tab_1.setTabOrder(self.waste_fromdate_dateedit, self.waste_todate_dateedit)
        self.wastedetail_tab_1.setTabOrder(self.waste_todate_dateedit, self.waste_table_search_button)
        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.schedule = SchedulePurchase()
        self.suplier = BusinessParty(category='Supplier')
        self.add = AddStockInventory()
        self.item = WasteMenu()
        self.waste_fromdate_dateedit.setDate(QDate.currentDate())
        self.waste_todate_dateedit.setDate(QDate.currentDate())
        self.waste_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.waste_table_newrow_button.clicked.connect(self.add_new_blank_rows)
        self.waste_table_discard_button.clicked.connect(self.discard)
        self.waste_table_search_button.clicked.connect(self.search_discard)
        self.wastedetail_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.wastedetail_tab_1.focusInEvent = self.load_rows



    def load_rows(self, event=None):
        pass

    def add_new_blank_rows(self):
        """
        deletes the schedules in the database
        """
        table = self.waste_table
        item = table.item(0, 0)
        if item:
            message = QMessageBox.critical(QMessageBox(), 'Warning!', 'This will remove all the entries',
                QMessageBox.Ok | QMessageBox.Cancel)
            if message == QMessageBox.Ok:
                table.setRowCount(0)
                table.clearContents()
                self.add_row_to_table('new')
                self.waste_table_discard_button.setVisible(True)
        elif not item:
            self.waste_table_discard_button.setVisible(True)
            self.add_row_to_table('new')


    def add_row_to_table(self, *args):
        """
        complex stuff of auto complete to be added to each combo box
        :return:
        """
        table = self.waste_table
        if args:
            if args[0] != 'new':
                table.clearContents()
                table.setRowCount(0)
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    code = QTableWidgetItem(j['code'])
                    table.setItem(i, 0, code)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 1, item)
                    category = QTableWidgetItem(j['category'])
                    table.setItem(i, 2, category)
                    quantity = QTableWidgetItem(str(j['quantity']))
                    table.setItem(i, 3, quantity)
                    reason = QTableWidgetItem(j['reason_for_discard'])
                    table.setItem(i, 4, reason)
            if args[0] == 'new':
                row = table.rowCount() + 1
                table.setRowCount(row)
                codeline = QLineEdit()
                codeline.editingFinished.connect(lambda: self.get_details_of_code(row))
                table.setCellWidget(row - 1, 0, codeline)
                itemcombo = QComboBox()
                self.fill_item_list(itemcombo)
                itemcombo.currentIndexChanged.connect(lambda: self.get_details_of_item(row))
                table.setCellWidget(row - 1, 1, itemcombo)
                category = QTableWidgetItem()
                table.setItem(row - 1, 2, category)
                quantity = QLineEdit()
                table.setCellWidget(row - 1, 3, quantity)
                combo = QComboBox()
                combo.addItem("Cancelled")
                combo.addItem("Mishandling")
                combo.addItem("Excess")
                table.setCellWidget(row - 1, 4, combo)
        table.setColumnWidth(0, (table.width() / 5))
        table.setColumnWidth(1, (table.width() / 5))
        table.setColumnWidth(2, (table.width() / 5))
        table.setColumnWidth(3, (table.width() / 5))
        table.horizontalHeader().setStretchLastSection(
            True)  # important to resize last section else blank space after last column

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
        self.item.populate_item(itemfield)

    def get_details_of_code(self, rowcount):
        """
        fills the item, category and units based on the code
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.waste_table
        codeline = table.cellWidget(row, 0)
        data = self.item.get_details_of_code(codeline.text())
        item = table.cellWidget(row, 1)
        index = item.findText(data['item'])
        item.setCurrentIndex(index)
        category = table.item(row, 2)
        category.setText(data['category'])

    def get_details_of_item(self, rowcount):
        """
        fills the code, category and units based on the item
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.waste_table
        itemcombo = table.cellWidget(row, 1)
        data = self.item.get_details_of_item(itemcombo.currentText())
        code = table.cellWidget(row, 0)
        code.setText(data['code'])
        category = table.item(row, 2)
        category.setText(data['category'])

    def discard(self):
        """
        saves the details in db before printing
        """
        logger.info('WasteDish discard initiated')
        table = self.waste_table
        data = self.get_data()
        if data:
            for i in data:
                status = self.item.discard(i)
                if status:
                    model_index = table.indexFromItem(i['model_item'])
                    row = model_index.row()
                    table.removeRow(row)
                else:
                    msg = QMessageBox.critical(QMessageBox(), "Error!!", "The item cannot be discarded", QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        return False

    def search_discard(self):
        """
        searches the discard from_date and to_date
        :return:none
        """
        table = self.waste_table
        item = table.cellWidget(0, 0)
        if item:
            msg = QMessageBox.critical(QMessageBox(), 'Warning!', 'This will delete all the rows added',
                QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Cancel:
                return False
        f_date = self.waste_fromdate_dateedit.text()
        from_date = datetime.strptime(f_date, '%d/%m/%Y')
        t_date = self.waste_todate_dateedit.text()
        to_date = datetime.strptime(t_date, '%d/%m/%Y')
        to_date = to_date + timedelta(hours=23, minutes=59, seconds=59)
        dataobj = self.item.find_itemdiscard(from_date=from_date, to_date=to_date)
        self.add_row_to_table(*dataobj)
        self.waste_table_discard_button.setVisible(False)

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.waste_table
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            dictionary = {}
            item = table.cellWidget(i, 0) if table.cellWidget(i, 0) is not None else table.item(i, 0)
            dictionary['code'] = item.text()
            if dictionary['code'] == '':
                break
            item = table.cellWidget(i, 1).currentText() if table.cellWidget(i, 1) is not None else table.item(i, 1).text()
            dictionary['item'] = item
            item = table.cellWidget(i, 2) if table.cellWidget(i, 2) is not None else table.item(i, 2)
            dictionary['category'] = item.text()
            item = table.cellWidget(i, 3) if table.cellWidget(i, 3) is not None else table.item(i, 3)
            dictionary['quantity'] = item.text()
            if dictionary['quantity'] == '':
                self.show_error('Quantity')
                return False
            item = table.cellWidget(i, 4).currentText() if table.cellWidget(i, 4) is not None else table.item(i, 4).text()
            dictionary['reason_for_discard'] = item
            dictionary['model_item'] = table.item(i, 2)
            dataobj.append(dictionary)
        return dataobj

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), "Fail!!", "Please Enter %s properly" % text, QMessageBox.Ok)


class WasteItems():
    """Item waste management tab"""
    global logger

    def __init__(self):
        ###
        logger.info('Inside WasteItems')
        self.wastedetail_tab_1 = QWidget()
        self.wastedetail_tab_1.setObjectName("wastedetail_tab_1")
        self.verticalLayout_9 = QVBoxLayout(self.wastedetail_tab_1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.waste_fromdate_label = QLabel(self.wastedetail_tab_1)
        self.waste_fromdate_label.setObjectName('waste_fromdate_label')
        self.horizontalLayout_12.addWidget(self.waste_fromdate_label)
        self.waste_fromdate_dateedit = QDateEdit(self.wastedetail_tab_1)
        self.waste_fromdate_dateedit.setCalendarPopup(True)
        self.waste_fromdate_dateedit.setObjectName("waste_fromdate_dateedit")
        self.horizontalLayout_12.addWidget(self.waste_fromdate_dateedit)
        self.waste_todate_label = QLabel(self.wastedetail_tab_1)
        self.waste_todate_label.setObjectName('waste_todate_label')
        self.horizontalLayout_12.addWidget(self.waste_todate_label)
        self.waste_todate_dateedit = QDateEdit(self.wastedetail_tab_1)
        self.waste_todate_dateedit.setCalendarPopup(True)
        self.waste_todate_dateedit.setObjectName("waste_todate_dateedit")
        self.waste_todate_dateedit.setMaximumDate(QDate.currentDate())
        self.horizontalLayout_12.addWidget(self.waste_todate_dateedit)
        spacerItem28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem28)
        self.waste_table_search_button = QPushButton(self.wastedetail_tab_1)
        self.waste_table_search_button.setObjectName("waste_table_search_button")
        self.horizontalLayout_12.addWidget(self.waste_table_search_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.waste_table = QTableWidget(self.wastedetail_tab_1)
        self.waste_table.setObjectName("waste_table")
        self.waste_table.setColumnCount(6)
        self.waste_table.setRowCount(0)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.waste_table.setHorizontalHeaderItem(5, item)
        self.waste_table.horizontalHeader().setCascadingSectionResizes(False)
        self.waste_table.horizontalHeader().setStretchLastSection(True)
        self.waste_table.verticalHeader().setVisible(False)
        self.waste_table.verticalHeader().setCascadingSectionResizes(False)
        self.waste_table.setSortingEnabled(True)
        self.verticalLayout_8.addWidget(self.waste_table)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        ##retranslate
        self.waste_fromdate_label.setText(
            QApplication.translate("MainWindow", "From Date", None, QApplication.UnicodeUTF8))
        self.waste_fromdate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.waste_todate_label.setText(
            QApplication.translate("MainWindow", "To Date", None, QApplication.UnicodeUTF8))
        self.waste_todate_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.waste_table_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Units", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Quantity", None, QApplication.UnicodeUTF8))
        self.waste_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Reason", None, QApplication.UnicodeUTF8))

        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.item = WasteIngredients()
        self.waste_fromdate_dateedit.setDate(QDate.currentDate())
        self.waste_todate_dateedit.setDate(QDate.currentDate())
        self.waste_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.waste_table_search_button.clicked.connect(self.search_discard)
        self.wastedetail_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.wastedetail_tab_1.focusInEvent = self.load_rows


    def load_rows(self, event=None):
        """calling add row to restructure the table every time container resizes"""
        self.add_row_to_table()

    def search_discard(self):
        """
        searches the discard from_date and to_date
        :return:none
        """
        f_date = self.waste_fromdate_dateedit.text()
        from_date = datetime.strptime(f_date, '%d/%m/%Y')
        t_date = self.waste_todate_dateedit.text()
        to_date = datetime.strptime(t_date, '%d/%m/%Y')
        to_date = to_date + timedelta(hours=23, minutes=59, seconds=59)
        dataobj = self.item.find_itemdiscard(from_date=from_date, to_date=to_date)
        self.add_row_to_table(*dataobj)

    def add_row_to_table(self, *args):
        """
        complex stuff of auto complete to be added to each combo box
        :return:
        """
        table = self.waste_table
        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                code = QTableWidgetItem(j['code'])
                table.setItem(i, 0, code)
                item = QTableWidgetItem(j['item'])
                table.setItem(i, 1, item)
                category = QTableWidgetItem(j['category'])
                table.setItem(i, 2, category)
                unit = QTableWidgetItem(str(j['units']))
                table.setItem(i, 3, unit)
                quantity = QTableWidgetItem(str(j['quantity']))
                table.setItem(i, 4, quantity)
                reason = QTableWidgetItem(j['reason_for_discard'])
                table.setItem(i, 5, reason)
        table.setColumnWidth(0, (table.width() / 6))
        table.setColumnWidth(1, (table.width() / 6))
        table.setColumnWidth(2, (table.width() / 6))
        table.setColumnWidth(3, (table.width() / 6))
        table.setColumnWidth(4, (table.width() / 6))
        table.horizontalHeader().setStretchLastSection(True)