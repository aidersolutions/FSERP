#! /usr/bin/env python

""" Report Module Ui"""

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QGridLayout, QTableWidget, QPushButton, QDialog, QLabel, QDateEdit, QFileDialog, QVBoxLayout, QLineEdit, QPixmap, \
    QAbstractItemView, QMessageBox, QIntValidator

from PySide.QtCore import Qt
from inventory.inventory import Stock
from employee.employee import EmployeeDetail, EmployeeDetailDialog
from report_tryton import Pest, Water, Health
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class Report():
    """
    The Basic Report Module Class
    """

    def __init__(self):
        ####
        self.report_tab_5 = QWidget()
        self.report_tab_5.setStyleSheet("")
        self.report_tab_5.setObjectName("report_tab_5")
        self.horizontalLayout_8 = QHBoxLayout(self.report_tab_5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.report_detail_tabWidget = QTabWidget(self.report_tab_5)
        self.report_detail_tabWidget.setObjectName("report_detail_tabWidget")
        self.add_tabs()
        self.horizontalLayout_8.addWidget(self.report_detail_tabWidget)
        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.report_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.report_tab_5.setFocusPolicy(Qt.StrongFocus)
        self.report_tab_5.focusInEvent = self.change_focus

    def add_tabs(self):
        """
        add new tabs to the table
        """
        employee = EmployeeNew()
        hygiene = Hygiene()
        report = Stock()
        self.report_detail_tabWidget.addTab(employee.employeedetail_tab_1, 'Employee')
        self.report_detail_tabWidget.addTab(hygiene.reporthygiene_tab_2, 'Hygiene')
        self.report_detail_tabWidget.addTab(report.stock_tab_1, 'Stock')

    def change_focus(self, event=None):
        """
        sets focus for the  child widgets
        """
        wid = self.report_detail_tabWidget.currentWidget()
        if wid.isVisible():
            wid.setFocus()


class ReportEmployeeTestDialogue(QDialog):
    """
    Employee Report Popup Manager
    """
    global logger

    def __init__(self, code=None, parent=None):
        logger.info('Inside ReportEmployeeTestDialogue')
        super(ReportEmployeeTestDialogue, self).__init__(parent)
        self.resize(500, 500)
        self.vertical_23 = QVBoxLayout(self)
        self.vertical_23.setObjectName("vertical_23")
        self.label_1 = QLabel(self)
        self.vertical_23.addWidget(self.label_1)
        self.report_health_table = QTableWidget(self)
        self.report_health_table.setObjectName("report_health_table")
        self.report_health_table.setColumnCount(5)
        self.report_health_table.setRowCount(0)
        self.report_health_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        item = QTableWidgetItem()
        self.report_health_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.report_health_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.report_health_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.report_health_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.report_health_table.setHorizontalHeaderItem(4, item)
        self.report_health_table.horizontalHeader().setCascadingSectionResizes(True)
        self.report_health_table.horizontalHeader().setStretchLastSection(True)
        self.report_health_table.verticalHeader().setCascadingSectionResizes(True)
        self.vertical_23.addWidget(self.report_health_table)
        self.horizontal_21 = QHBoxLayout()
        self.report_health_newrow_buttuon = QPushButton(self)
        self.report_health_newrow_buttuon.setObjectName("report_health_newrow_buttuon")
        self.horizontal_21.addWidget(self.report_health_newrow_buttuon)
        spacerItem23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_21.addItem(spacerItem23)
        self.vertical_23.addLayout(self.horizontal_21)
        ### retanslate
        self.setWindowTitle(
            QApplication.translate("MainWindow", "Health Report", None, QApplication.UnicodeUTF8))
        self.label_1.setText(
            QApplication.translate("MainWindow", "Health Report", None, QApplication.UnicodeUTF8))
        self.report_health_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.report_health_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.report_health_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Organization Name", None, QApplication.UnicodeUTF8))
        self.report_health_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Test", None, QApplication.UnicodeUTF8))
        self.report_health_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Description", None, QApplication.UnicodeUTF8))
        self.report_health_newrow_buttuon.setText(
            QApplication.translate("MainWindow", "New Row", None, QApplication.UnicodeUTF8))
        ###signals and slots && other stuffs
        self.health = Health(emp_id=code)
        self.report_health_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_table_rows()
        self.report_health_table.itemDoubleClicked.connect(self.popup_health_edit)
        self.report_health_newrow_buttuon.clicked.connect(self.new_healthTest)
        self.focusInEvent = self.load_rows

    def new_healthTest(self, code=None):
        """
        pops up a dialog to add a new report or edit the existing report
        :param code:the code of the report
        """
        try:
            pop = HygieneReportPop(parent=self, table='health_table', code=code)
            pop.setWindowFlags(Qt.WindowTitleHint)
            pop.exec_()
            self.load_table_rows()
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def load_table_rows(self):
        """
        loads the table of reports
        """
        try:
            data = self.health.load_report()
            if data[0]:
                self.add_table_rows(*data[1])
                if not data[1]:
                    self.report_health_table.clearContents()
                    self.report_health_table.setRowCount(0)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def popup_health_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        """
        try:
            table = self.report_health_table
            model_index = table.indexFromItem(item)
            row = model_index.row()
            self.new_healthTest(table.item(row, 0).text())
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def add_table_rows(self, *args):
        """
        adds a new row to the pes table
        """
        try:
            table = self.report_health_table
            if args:
                table.setRowCount(len(args))
                for row, data in enumerate(args):
                    table.setItem(row, 0, QTableWidgetItem(data['code']))
                    table.setItem(row, 1, QTableWidgetItem(data['date']))
                    table.setItem(row, 2, QTableWidgetItem(data['organization']))
                    table.setItem(row, 3, QTableWidgetItem(data['test']))
                    table.setItem(row, 4, QTableWidgetItem(data['description']))
            table.setColumnWidth(0, (table.width() / 5) * 0.5)
            table.setColumnWidth(1, (table.width() / 5) * 0.5)
            table.setColumnWidth(2, table.width() / 5)
            table.setColumnWidth(3, table.width() / 5)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def load_rows(self, event):
        """
        loads the rows of the tables
        """
        self.add_table_rows()


class EmployeeDetailDialogEdit(EmployeeDetailDialog):
    """
    The Employee details Dialog Extended from Employee Module
    """
    global logger

    def __init__(self, parent, code):
        logger.info('Inside EmployeeDetailDialogueEdit')
        EmployeeDetailDialog.__init__(self, parent=parent, code=code)
        self.code = code
        self.dialog.employeedialogue_newdesignation_pushbutton.setVisible(False)
        self.dialog.employeedialogue_newdepartment_pushbutton.setVisible(False)
        self.dialog.employeedialogue_employeedelete_pushbutton.setVisible(False)
        # self.setDisabled(True)
        self.dialog.employeedialogue_employeeid_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeename_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeesurname_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeefathername_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeeadhar_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeebasicpay_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeecontact_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeepan_lineedit.setDisabled(True)
        self.dialog.employeedialogue_employeeaddress_textedit.setDisabled(True)
        self.dialog.employeedialogue_employeeshift_combobox.setDisabled(True)
        self.dialog.employeedialogue_employdesignation_combobox.setDisabled(True)
        self.dialog.employeedialogue_employeedepartment_combobox.setDisabled(True)
        self.dialog.employeedialogue_employeeperiod_combobox.setDisabled(True)
        self.dialog.employeedialogue_employeesex_combobox.setDisabled(True)
        self.dialog.employeedialogue_employeedob_dateedit.setDisabled(True)
        self.dialog.employeedialogue_employeedoj_dateedit.setDisabled(True)
        self.dialog.employeedialogue_employeesave_pushbutton.setText('View Test Details')
        self.dialog.employeedialogue_employeesave_pushbutton.clicked.connect(self.view_employee_details)

    def save_or_edit_employee(self):
        """
        Overriding this method to nullify its process
        """
        pass

    def view_employee_details(self):
        """
        popup for employee health report details
        """
        if self.code:
            self.popup = ReportEmployeeTestDialogue(code=self.code)
            self.popup.setWindowFlags(Qt.WindowTitleHint)
            self.popup.exec_()


class EmployeeNew(EmployeeDetail):
    """ The Employee Details Tab
    """
    global logger

    def __init__(self):
        logger.info('Inside EmployeeNew')
        EmployeeDetail.__init__(self)
        self.employeetab_add_button.setText('Refresh')

    def popup_employee_form(self, *args):
        """
        who=the employee number of the employee to be viewed
        Overrided to change the usage
        """
        if args:
            self.popup = EmployeeDetailDialogEdit(parent=self, code=args[0])
            self.popup.exec_()
        else:
            self.get_employee_details()


class Hygiene():
    """ The Hygiene Tab
    """
    global logger

    def __init__(self):
        ####
        logger.info('Inside Hygiene')
        self.reporthygiene_tab_2 = QWidget()
        self.reporthygiene_tab_2.setObjectName("reporthygiene_tab_2")
        self.vertical_23 = QVBoxLayout(self.reporthygiene_tab_2)
        self.vertical_23.setObjectName("vertical_23")
        self.label_1 = QLabel(self.reporthygiene_tab_2)
        self.vertical_23.addWidget(self.label_1)
        self.report_hyginepest_table = QTableWidget(self.reporthygiene_tab_2)
        self.report_hyginepest_table.setObjectName("report_hyginepest_table")
        self.report_hyginepest_table.setColumnCount(5)
        self.report_hyginepest_table.setRowCount(0)
        self.report_hyginepest_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        item = QTableWidgetItem()
        self.report_hyginepest_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.report_hyginepest_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.report_hyginepest_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.report_hyginepest_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.report_hyginepest_table.setHorizontalHeaderItem(4, item)
        self.report_hyginepest_table.horizontalHeader().setCascadingSectionResizes(True)
        self.report_hyginepest_table.horizontalHeader().setStretchLastSection(True)
        self.report_hyginepest_table.verticalHeader().setCascadingSectionResizes(True)
        self.vertical_23.addWidget(self.report_hyginepest_table)
        self.horizontal_21 = QHBoxLayout()
        self.report_hyginepest_newrow_buttuon = QPushButton(self.reporthygiene_tab_2)
        self.report_hyginepest_newrow_buttuon.setObjectName("report_hyginepest_newrow_buttuon")
        self.horizontal_21.addWidget(self.report_hyginepest_newrow_buttuon)
        spacerItem23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_21.addItem(spacerItem23)
        # self.report_hyginepest_save_button = QPushButton(self.reporthygiene_tab_2)
        # self.report_hyginepest_save_button.setObjectName("report_hyginepest_save_button")
        # self.horizontal_21.addWidget(self.report_hyginepest_save_button)
        self.vertical_23.addLayout(self.horizontal_21)
        self.label_2 = QLabel(self.reporthygiene_tab_2)
        self.vertical_23.addWidget(self.label_2)
        self.report_hyginewater_table = QTableWidget(self.reporthygiene_tab_2)
        self.report_hyginewater_table.setObjectName("report_hyginewater_table")
        self.report_hyginewater_table.setColumnCount(5)
        self.report_hyginewater_table.setRowCount(0)
        self.report_hyginewater_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        item = QTableWidgetItem()
        self.report_hyginewater_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.report_hyginewater_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.report_hyginewater_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.report_hyginewater_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.report_hyginewater_table.setHorizontalHeaderItem(4, item)
        self.report_hyginewater_table.horizontalHeader().setCascadingSectionResizes(True)
        self.report_hyginewater_table.horizontalHeader().setStretchLastSection(True)
        self.report_hyginewater_table.verticalHeader().setCascadingSectionResizes(True)
        self.vertical_23.addWidget(self.report_hyginewater_table)
        self.horizontal_22 = QHBoxLayout()
        self.report_hyginewater_newrow_buttuon = QPushButton(self.reporthygiene_tab_2)
        self.report_hyginewater_newrow_buttuon.setObjectName("report_hyginewater_newrow_buttuon")
        self.horizontal_22.addWidget(self.report_hyginewater_newrow_buttuon)
        spacerItem24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_22.addItem(spacerItem24)
        # self.report_hyginewater_save_button = QPushButton(self.reporthygiene_tab_2)
        # self.report_hyginewater_save_button.setObjectName("report_hyginewater_save_button")
        # self.horizontal_22.addWidget(self.report_hyginewater_save_button)
        self.vertical_23.addLayout(self.horizontal_22)
        ### retanslate
        self.label_1.setText(
            QApplication.translate("MainWindow", "Pest Test Report", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Organization Name", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Test", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Description", None, QApplication.UnicodeUTF8))
        self.report_hyginepest_newrow_buttuon.setText(
            QApplication.translate("MainWindow", "New Row", None, QApplication.UnicodeUTF8))
        # self.report_hyginepest_save_button.setText(
        # QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        self.label_2.setText(
            QApplication.translate("MainWindow", "Water Test Report", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Organization Name", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Test", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Description", None, QApplication.UnicodeUTF8))
        self.report_hyginewater_newrow_buttuon.setText(
            QApplication.translate("MainWindow", "New Row", None, QApplication.UnicodeUTF8))
        # self.report_hyginewater_save_button.setText(
        #     QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        ###signals and slots && other stuffs
        self.pest = Pest()
        self.water = Water()
        self.report_hyginepest_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.report_hyginewater_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_table_rows()
        self.report_hyginepest_table.itemDoubleClicked.connect(self.popup_pest_edit)
        self.report_hyginewater_table.itemDoubleClicked.connect(self.popup_water_edit)
        self.reporthygiene_tab_2.focusInEvent = self.load_rows  # very important for focus
        self.report_hyginepest_newrow_buttuon.clicked.connect(
            self.new_pestTest)  # if no focus available then we need lambda
        self.report_hyginewater_newrow_buttuon.clicked.connect(self.new_waterTest)

    def new_pestTest(self, code=None):
        """
        The pest report popup generator
        :param code: The code of the pest report
        """
        pop = HygieneReportPop(parent=self, table='pest_table', code=code)
        pop.setWindowFlags(Qt.WindowTitleHint)
        pop.exec_()
        self.load_table_rows()

    def new_waterTest(self, code=None):
        """
        The water report popup generator
        :param code: The code of the water report
        """
        pop = HygieneReportPop(parent=self, table='water_table', code=code)
        pop.setWindowFlags(Qt.WindowTitleHint)
        pop.exec_()
        self.load_table_rows()

    def load_table_rows(self):
        """
        Populates the rows for both the table
        """
        logger.info('Hygiene save table initiated')
        try:
            data = self.pest.load_report()
            if data[0]:
                self.add_table_rows('pest_table', *data[1])
                if not data[1]:
                    self.report_hyginepest_table.clearContents()
                    self.report_hyginepest_table.setRowCount(0)
            data = self.water.load_report()
            if data[0]:
                self.add_table_rows('water_table', *data[1])
                if not data[1]:
                    self.report_hyginewater_table.clearContents()
                    self.report_hyginewater_table.setRowCount(0)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def popup_pest_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        """
        table = self.report_hyginepest_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        self.new_pestTest(table.item(row, 0).text())

    def popup_water_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        """
        table = self.report_hyginewater_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        self.new_waterTest(table.item(row, 0).text())

    def add_table_rows(self, tablename, *args):
        """
        adds a new row to the pes table
        """
        if tablename == 'pest_table':
            table = self.report_hyginepest_table
        else:
            table = self.report_hyginewater_table
        if args:
            table.setRowCount(len(args))
            for row, data in enumerate(args):
                table.setItem(row, 0, QTableWidgetItem(data['code']))
                table.setItem(row, 1, QTableWidgetItem(data['date']))
                table.setItem(row, 2, QTableWidgetItem(data['organization']))
                table.setItem(row, 3, QTableWidgetItem(data['test']))
                table.setItem(row, 4, QTableWidgetItem(data['description']))
        table.setColumnWidth(0, (table.width() / 5) * 0.5)
        table.setColumnWidth(1, (table.width() / 5) * 0.5)
        table.setColumnWidth(2, table.width() / 5)
        table.setColumnWidth(3, table.width() / 5)

    def load_rows(self, event):
        """
        loads the rows of the tables
        """
        self.add_table_rows(tablename='pest_table')
        self.add_table_rows(tablename='water_table')


class HygieneReportPop(QDialog):
    """
    The Report Form Handler
    """

    def __init__(self, parent=None, code=None, table=None):
        super(HygieneReportPop, self).__init__()
        self.setup_pop()  # do not change the order of these two function
        self.code = code
        self.parent_object = parent
        self.image_data = None
        self.process_override(table=table)  # do not change the order of these two function
        if not code:
            self.update_button.setHidden(True)
            self.delete_button.setHidden(True)
            self.calculate_code()
        else:
            self.create_button.setHidden(True)
            self.update_data()

    def process_override(self, table):
        """
        Function that assigns the table and tryton backend handler objects based on the tables
        :param table: the table name
        """
        try:
            if table == 'pest_table':
                self.backend_handle = self.parent_object.pest
                self.table = self.parent_object.report_hyginepest_table
            elif table == 'water_table':
                self.backend_handle = self.parent_object.water
                self.table = self.parent_object.report_hyginewater_table
            elif table == 'health_table':
                self.backend_handle = self.parent_object.health
                self.table = self.parent_object.report_health_table
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def setup_pop(self):
        """
        sets up the form.
        """
        self.grid_layout = QGridLayout(self)
        self.label_1 = QLabel(self)
        self.grid_layout.addWidget(self.label_1, 0, 0, 1, 1)
        self.code_line = QLineEdit(self)
        self.code_line.setValidator(QIntValidator(0, 99999))
        self.grid_layout.addWidget(self.code_line, 0, 1, 1, 1)
        self.label_2 = QLabel(self)
        self.grid_layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.date_line = QDateEdit(self)
        self.date_line.setCalendarPopup(True)
        self.grid_layout.addWidget(self.date_line, 1, 1, 1, 1)
        self.label_3 = QLabel(self)
        self.grid_layout.addWidget(self.label_3, 2, 0, 1, 1)
        self.organization_line = QLineEdit(self)
        self.grid_layout.addWidget(self.organization_line, 2, 1, 1, 1)
        self.label_4 = QLabel(self)
        self.grid_layout.addWidget(self.label_4, 3, 0, 1, 1)
        self.test_line = QLineEdit(self)
        self.grid_layout.addWidget(self.test_line, 3, 1, 1, 1)
        self.label_5 = QLabel(self)
        self.grid_layout.addWidget(self.label_5, 4, 0, 1, 1)
        self.description_line = QLineEdit(self)
        self.grid_layout.addWidget(self.description_line, 4, 1, 1, 1)
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(':/images/upload.png')
        # self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation) #not used
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)
        self.grid_layout.addWidget(self.image_label, 0, 2, 5, 2)
        self.horizontal = QHBoxLayout()
        self.delete_button = QPushButton(self)
        self.horizontal.addWidget(self.delete_button)
        self.create_button = QPushButton(self)
        self.horizontal.addWidget(self.create_button)
        self.update_button = QPushButton(self)
        self.horizontal.addWidget(self.update_button)
        self.upload_button = QPushButton(self)
        self.horizontal.addWidget(self.upload_button)
        self.grid_layout.addLayout(self.horizontal, 5, 0, 1, 4)
        ### retanslate
        self.label_1.setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.label_2.setText(
            QApplication.translate("MainWindow", "Date", None, QApplication.UnicodeUTF8))
        self.date_line.setDisplayFormat(
            QApplication.translate("MainWindow", "dd/MM/yyyy", None, QApplication.UnicodeUTF8))
        self.label_3.setText(
            QApplication.translate("MainWindow", "Organization Name", None, QApplication.UnicodeUTF8))
        self.label_4.setText(
            QApplication.translate("MainWindow", "Test", None, QApplication.UnicodeUTF8))
        self.label_5.setText(
            QApplication.translate("MainWindow", "Description", None, QApplication.UnicodeUTF8))
        self.delete_button.setText(
            QApplication.translate("MainWindow", "Delete", None, QApplication.UnicodeUTF8))
        self.create_button.setText(
            QApplication.translate("MainWindow", "Create", None, QApplication.UnicodeUTF8))
        self.update_button.setText(
            QApplication.translate("MainWindow", "Update", None, QApplication.UnicodeUTF8))
        self.upload_button.setText(
            QApplication.translate("MainWindow", "Upload", None, QApplication.UnicodeUTF8))
        self.create_button.clicked.connect(self.create_report)
        self.upload_button.clicked.connect(self.open_file)
        self.update_button.clicked.connect(self.update_report)
        self.delete_button.clicked.connect(self.delete_report)
        self.image_label.mouseReleaseEvent = self.image_viewer

    def update_data(self):
        """
        Updates the data in the form
        """
        try:
            data = self.backend_handle.read_report(code=int(self.code))
            if data:
                if data[0]:
                    data = data[1]
                    self.code_line.setText(data['code'])
                    self.code_line.setDisabled(True)
                    self.date_line.setDate(data['date'])
                    self.organization_line.setText(data['organization'])
                    self.test_line.setText(data['test'])
                    self.description_line.setText(data['description'])
                    self.image_data = str(data['report'])
                    self.pixmap = QPixmap()
                    self.pixmap.loadFromData(self.image_data)
                    self.image_label.setPixmap(self.pixmap.scaled(self.image_label.size(),
                        Qt.KeepAspectRatio, Qt.FastTransformation))
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def image_viewer(self, event=None):
        """pops up a image viewer to check the details"""
        dialog = QDialog()
        dialog.setWindowFlags(Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
        layout = QHBoxLayout(dialog)
        label = QLabel(dialog)
        # self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(self.pixmap)
        label.setScaledContents(True)
        layout.addWidget(label)
        dialog.exec_()

    def open_file(self):
        """
        saves the file
        """
        dialog = QFileDialog(self)
        dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        dialog.setStyleSheet('color:black;')
        name = ''
        if dialog.exec_():
            name = dialog.selectedFiles()
        if name:
            self.image_data = open(name[0], 'rb').read()
            self.pixmap = QPixmap(name[0])
        self.image_label.setPixmap(self.pixmap.scaled(self.image_label.size(),
            Qt.KeepAspectRatio, Qt.FastTransformation))

    def create_report(self):
        """
        Creates a new Report
        """
        try:
            data = self.get_data()
            if data:
                status = self.backend_handle.create_report(data=data)
                if status:
                    if status[0]:
                        QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                        self.create_button.setHidden(True)
                        self.delete_button.setVisible(True)
                        self.update_button.setVisible(True)
                        self.code = data['code']
                        self.update_data()
                    else:
                        QMessageBox.critical(self, 'Error', status[1], QMessageBox.Ok)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def update_report(self):
        """
        Updates an existing Report
        """
        try:
            data = self.get_data()
            if data:
                status = self.backend_handle.update_report(data=data)
                if status:
                    if status[0]:
                        QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                    else:
                        QMessageBox.critical(self, 'Error', status[1], QMessageBox.Ok)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def get_data(self):
        """
        Gets the data from the form as a dictionary
        :return:dictionary
        """
        try:
            data = {}
            data['code'] = self.code_line.text()
            data['date'] = self.date_line.text()
            data['organization'] = self.organization_line.text()
            data['test'] = self.test_line.text()
            data['description'] = self.description_line.text()
            data['report'] = self.image_data
            for key, value in data.iteritems():
                if not value:
                    QMessageBox.critical(self, 'Error', 'Insert Proper value for %s' % key.title(), QMessageBox.Ok)
                    return False
            return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def delete_report(self):
        """
        Deletes the existing report
        :return:
        """
        try:
            code = self.code_line.text()
            status = self.backend_handle.delete_report(code=code)
            if status:
                if status[0]:
                    QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                    self.close()
                else:
                    QMessageBox.critical(self, 'Error', status[1], QMessageBox.Ok)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def calculate_code(self):
        """
        Calculates the entry number, Eases the user for entering the code
        """
        try:
            table = self.table
            if table:
                code = []
                rows = table.rowCount()
                for row in range(rows):
                    code.append(table.item(row, 0).text())
                if code:
                    new_code = str(int(max(code)) + 1)
                    self.code_line.setText(new_code)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'