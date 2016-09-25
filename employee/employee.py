#! /usr/bin/env python

""" Employee Module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QGridLayout, QTableWidget, QPushButton, QAbstractItemView, QPrintDialog, QDialog, QLabel, QDateEdit, QLineEdit, \
    QMessageBox, QCheckBox, QDoubleValidator, QComboBox, QVBoxLayout, QFont, QButtonGroup, QShortcut, QKeySequence

from PySide.QtCore import Qt, QDate, QTime
from employee_popupGUI.employee_details_popup import Ui_Dialog
from employee_popupGUI.salary_settings_popup import Ui_salary_settings
from employee_popupGUI.shift_add_popup import Ui_shift_popup
from employee_popupGUI.department_add_popup import Ui_department_popup
from employee_popupGUI.designation_add_popup import Ui_new_designation
from employee_tryton import EmployeeManagement, EmployeeManagementList, ShiftList, ShiftManagement, SalarySettingList, \
    SalarySettingManagement, AttendenceManagement, PayrollManagement
from printer.print_execute import PrintNow
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class Employee():
    """Main Employee tab container class"""

    def __init__(self):
        ####
        self.employee_tab_3 = QWidget()
        self.employee_tab_3.setStyleSheet("")
        self.employee_tab_3.setObjectName("employee_tab_3")
        self.horizontalLayout = QHBoxLayout(self.employee_tab_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.employee_detail_tabWidget = QTabWidget(self.employee_tab_3)
        self.employee_detail_tabWidget.setObjectName("employee_detail_tabWidget")
        self.add_tabs()
        self.horizontalLayout.addWidget(self.employee_detail_tabWidget)
        ####signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.employee_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.employee_tab_3.setFocusPolicy(Qt.StrongFocus)
        self.employee_tab_3.focusInEvent = self.change_focus


    def add_tabs(self):
        """
        :return: add new tab to the widget
        """
        employee = EmployeeDetail()
        attendence = Attendence()
        payroll = PayRoll()
        shift = Shift()
        salarysettings = SalarySettings()
        QShortcut(QKeySequence(settings.custom_shortcut['employeetab_employee']),
                  self.employee_detail_tabWidget, lambda: self.change_index(0))
        QShortcut(QKeySequence(settings.custom_shortcut['employeetab_attendance']),
                  self.employee_detail_tabWidget, lambda: self.change_index(1))
        QShortcut(QKeySequence(settings.custom_shortcut['employeetab_payroll']),
                  self.employee_detail_tabWidget, lambda: self.change_index(2))
        QShortcut(QKeySequence(settings.custom_shortcut['employeetab_shift']),
                  self.employee_detail_tabWidget, lambda: self.change_index(3))
        QShortcut(QKeySequence(settings.custom_shortcut['employeetab_salsettings']),
                  self.employee_detail_tabWidget, lambda: self.change_index(4))
        self.employee_detail_tabWidget.addTab(employee.employeedetail_tab_1, 'Employee')
        self.employee_detail_tabWidget.addTab(attendence.attendence_tab_2, 'Attendence')
        self.employee_detail_tabWidget.addTab(payroll.payroll_tab_3, 'Payroll')
        self.employee_detail_tabWidget.addTab(shift.shift_tab_4, 'Shift')
        self.employee_detail_tabWidget.addTab(salarysettings.salary_tab_5, 'Salary Setting')

    def change_focus(self, event=None):
        """
        :return:sets focus for the  child widgets
        """
        wid = self.employee_detail_tabWidget.currentWidget()
        if wid.isVisible():
            wid.setFocus()

    def change_index(self, index):
        """chages the tab index"""
        self.employee_detail_tabWidget.setCurrentIndex(index)


class NewDepartment(QDialog):
    """New department entry class"""
    global logger

    def __init__(self, parent=None, emp_management_obj=None):
        QDialog.__init__(self)
        logger.info('Inside NewDepartment')
        self.dialog = Ui_department_popup()
        self.dialog.setupUi(self)
        self.parent = parent
        self.management = emp_management_obj
        self.dialog.department_add_save_button.clicked.connect(self.save_department)
        self.dialog.department_add_delete_button.clicked.connect(self.delete_department)
        self.dialog.department_add_id_lineedit.setValidator(QDoubleValidator(1, 999, 3))
        self.dialog.department_add_name_lineedit.textChanged.connect(
            lambda: self.auto_capital(self.dialog.department_add_name_lineedit))

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def save_department(self):
        """Saves a new department entry"""
        logger.info('NewDepartment saving initiated')
        data = {}
        data['name'] = self.dialog.department_add_name_lineedit.text()
        data['dep_id'] = self.dialog.department_add_id_lineedit.text()
        status = self.management.save_department(data)
        if status[0]:
            self.parent.load_department()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % status[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()
        else:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!!',
                "%s, would you like to close?" % status[1],
                QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()
            else:
                pass

    def delete_department(self):
        """deletes the deparmtent entry"""
        logger.info('NewDepartment deleting initiated')
        data = {}
        data['name'] = self.dialog.department_add_name_lineedit.text()
        data['dep_id'] = self.dialog.department_add_id_lineedit.text()
        status = self.management.delete_department(data)
        if status[0]:
            self.parent.load_department()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % status[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()
        else:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!!',
                "%s, would you like to close?" % status[1],
                QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()
            else:
                pass


class NewDesignation(QDialog):
    """New designation entry class"""
    global logger

    def __init__(self, parent=None, emp_management_obj=None):
        logger.info('Inside NewDesignation')
        QDialog.__init__(self)
        self.dialog = Ui_new_designation()
        self.dialog.setupUi(self)
        self.parent = parent
        self.management = emp_management_obj
        self.dialog.designation_add_save_button.clicked.connect(self.save_designation)
        self.dialog.designation_add_delete_button.clicked.connect(self.delete_designation)
        self.dialog.designation_add_code_lineedit.setValidator(QDoubleValidator(1, 999, 3))
        self.dialog.designation_add_name_lineedit.textChanged.connect(
            lambda: self.auto_capital(self.dialog.designation_add_name_lineedit))

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def save_designation(self):
        """saves a new designation entry"""
        logger.info('NewDesignation saving initiated')
        data = {}
        data['name'] = self.dialog.designation_add_name_lineedit.text()
        data['des_code'] = self.dialog.designation_add_code_lineedit.text()
        status = self.management.save_designation(data)
        if status[0]:
            if self.parent:
                self.parent.load_designation()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % status[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()
        else:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!!',
                "%s, would you like to close?" % status[1],
                QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()
            else:
                pass

    def delete_designation(self):
        """deletes a designation entry"""
        logger.info('NewDesignation deleting initiated')
        data = {}
        data['name'] = self.dialog.designation_add_name_lineedit.text()
        data['des_code'] = self.dialog.designation_add_code_lineedit.text()
        status = self.management.delete_designation(data)
        if status[0]:
            if self.parent:
                self.parent.load_designation()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % status[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()
        else:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!!',
                "%s, would you like to close?" % status[1],
                QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()
            else:
                pass


class EmployeeDetailDialog(QDialog):
    """Pop up for the empoloyee details"""
    global logger

    def __init__(self, parent=None, code=None):
        logger.info('Inside EmployeeDetailDialogue')
        QDialog.__init__(self)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.parent = parent
        self.dialog.employeedialogue_employeeid_lineedit.setValidator(QDoubleValidator(1, 999, 3))
        self.dialog.employeedialogue_employeebasicpay_lineedit.setValidator(QDoubleValidator(1, 999999, 6))
        self.dialog.employeedialogue_newdesignation_pushbutton.setVisible(False)
        name = self.dialog.employeedialogue_employeename_lineedit
        name.textChanged.connect(lambda: self.auto_capital(name))
        father = self.dialog.employeedialogue_employeefathername_lineedit
        father.textChanged.connect(lambda: self.auto_capital(father))
        surname = self.dialog.employeedialogue_employeesurname_lineedit
        surname.textChanged.connect(lambda: self.auto_capital(surname))
        self.dialog.employeedialogue_employdesignation_combobox.setStyleSheet("QAbstractItemView{""background: #4B77BE;""}")
        self.dialog.employeedialogue_employeedepartment_combobox.setStyleSheet("QAbstractItemView{""background: #4B77BE;""}")
        self.dialog.employeedialogue_employeeperiod_combobox.setStyleSheet("QAbstractItemView{""background: #4B77BE;""}")
        self.dialog.employeedialogue_employeesex_combobox.setStyleSheet("QAbstractItemView{""background: #4B77BE;""}")
        self.dialog.employeedialogue_employeeshift_combobox.setStyleSheet("QAbstractItemView{""background: #4B77BE;""}")
        self.dialog.employeedialogue_employeeaddress_textedit.setTabChangesFocus(True)
        self.dialog.employeedialogue_employeedoj_dateedit.setMaximumDate(QDate.currentDate())
        self.dialog.employeedialogue_employeedoj_dateedit.setDate(QDate.currentDate())
        today = datetime.today()
        fourteenyearsback = today - relativedelta(years=14)
        self.dialog.employeedialogue_employeedob_dateedit.setMaximumDate(
            QDate.fromString(fourteenyearsback.strftime('%d/%m/%Y'), 'dd/MM/yyyy'))
        self.dialog.employeedialogue_employeedob_dateedit.setDate(
            QDate.fromString(fourteenyearsback.strftime('%d/%m/%Y'), 'dd/MM/yyyy'))
        if code:
            self.employee_id = code
        else:
            self.employee_id = None
        if not self.employee_id:
            self.dialog.employeedialogue_employeedelete_pushbutton.setVisible(False)
            self.dialog.employeedialogue_employeeid_lineedit.setPlaceholderText('Not Assigned')
            self.management = EmployeeManagement()
        else:
            self.management = EmployeeManagement(emp_id=self.employee_id)
            self.load_data()
        self.load_department()
        self.load_designation()
        self.load_shifts()
        self.dialog.employeedialogue_newdepartment_pushbutton.clicked.connect(self.pop_new_department)
        #self.dialog.employeedialogue_newdesignation_pushbutton.clicked.connect(self.pop_new_designation)
        self.dialog.employeedialogue_employeesave_pushbutton.clicked.connect(self.save_or_edit_employee)
        self.dialog.employeedialogue_employeedelete_pushbutton.clicked.connect(self.delete_employee)

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def pop_new_designation(self):
        """new designation entry popup"""
        designation = NewDesignation(parent=self, emp_management_obj=self.management)
        designation.exec_()

    def pop_new_department(self):
        """new designation entry popup"""
        department = NewDepartment(parent=self, emp_management_obj=self.management)
        department.exec_()

    def load_designation(self):
        """loads the existing designations"""
        combo = self.dialog.employeedialogue_employdesignation_combobox
        data = self.management.load_designation()
        combo.clear()
        combo.addItems(data)

    def load_department(self):
        """loadst the existing departments"""
        combo = self.dialog.employeedialogue_employeedepartment_combobox
        data = self.management.load_department()
        combo.clear()
        combo.addItems(data)

    def load_shifts(self):
        """loads the existing shifts"""
        combo = self.dialog.employeedialogue_employeeshift_combobox
        data = self.management.get_shift_list()
        combo.clear()
        combo.addItems(data)

    def save_or_edit_employee(self):
        """
        :return:if code give then save edit else save new employee.
        """
        logger.info('EmployeeDetailDialogue save or edit initiated')
        data = {}
        data['employee_id'] = self.dialog.employeedialogue_employeeid_lineedit.text()
        data['department'] = self.dialog.employeedialogue_employeedepartment_combobox.currentText()
        data['designation'] = self.dialog.employeedialogue_employdesignation_combobox.currentText()
        data['name'] = self.dialog.employeedialogue_employeename_lineedit.text()
        data['surname'] = self.dialog.employeedialogue_employeesurname_lineedit.text()
        data['fathersname'] = self.dialog.employeedialogue_employeefathername_lineedit.text()
        data['gender'] = self.dialog.employeedialogue_employeesex_combobox.currentText()
        data['dob'] = self.dialog.employeedialogue_employeedob_dateedit.text()
        data['doj'] = self.dialog.employeedialogue_employeedoj_dateedit.text()
        data['pan'] = self.dialog.employeedialogue_employeepan_lineedit.text()
        data['adhar'] = self.dialog.employeedialogue_employeeadhar_lineedit.text()
        data['salary'] = self.dialog.employeedialogue_employeebasicpay_lineedit.text()
        data['period'] = self.dialog.employeedialogue_employeeperiod_combobox.currentText()
        data['shift'] = self.dialog.employeedialogue_employeeshift_combobox.currentText()
        data['address'] = self.dialog.employeedialogue_employeeaddress_textedit.toPlainText()
        data['phone'] = self.dialog.employeedialogue_employeecontact_lineedit.text()
        for i, j in data.iteritems():
            if i == 'phone':
                try:
                    ll = list(j)
                    if len(ll) != 10:
                        raise ValueError('wrong value')
                    int(j)
                except Exception:
                    msg = QMessageBox.critical(QMessageBox(), 'Fail!', 'Invalid %s!!' % i,QMessageBox.Ok | QMessageBox.Cancel)
                    if msg == QMessageBox.Ok:
                        return False
            if j == '':
                msg = QMessageBox.critical(QMessageBox(), 'Fail!', 'Invalid %s!!' % i,QMessageBox.Ok | QMessageBox.Cancel)
                if msg == QMessageBox.Ok:
                    return False
        state = self.management.save_employee(data)
        if not state[0]:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!', '%s!!' % state[1], QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                return False
        else:
            self.parent.get_employee_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % state[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()
            self.dialog.employeedialogue_employeedelete_pushbutton.setVisible(True)

    def delete_employee(self):
        """
        :return: delete the employee
        """
        logger.info('EmployeeDetailDialogue delete initiated')
        msg = QMessageBox.critical(QMessageBox(), 'Warning!!', 'This will delete the employee entry', QMessageBox.Ok,
            QMessageBox.Cancel)
        if msg == QMessageBox.Cancel:
            return False
        status = self.management.remove_employee()
        if status:
            self.parent.get_employee_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', 'The employee was deleted successfully!!',
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()

    def load_data(self):
        """loads the details of the employee"""
        data = self.management.load_employee()
        self.dialog.employeedialogue_employeeid_lineedit.setText(data['employee_id'])
        index = self.dialog.employeedialogue_employeedepartment_combobox.findText(data['department'])
        self.dialog.employeedialogue_employeedepartment_combobox.setCurrentIndex(index)
        index = self.dialog.employeedialogue_employdesignation_combobox.findText(data['designation'])
        self.dialog.employeedialogue_employdesignation_combobox.setCurrentIndex(index)
        self.dialog.employeedialogue_employeename_lineedit.setText(data['name'])
        self.dialog.employeedialogue_employeesurname_lineedit.setText(data['surname'])
        self.dialog.employeedialogue_employeefathername_lineedit.setText(data['fathersname'])
        index = self.dialog.employeedialogue_employeesex_combobox.findText(data['gender'])
        self.dialog.employeedialogue_employeesex_combobox.setCurrentIndex(index)
        self.dialog.employeedialogue_employeedob_dateedit.setDate(QDate.fromString(data['dob'], 'dd-MM-yyyy'))
        self.dialog.employeedialogue_employeedoj_dateedit.setDate(QDate.fromString(data['doj'], 'dd-MM-yyyy'))
        self.dialog.employeedialogue_employeepan_lineedit.setText(data['pan'])
        self.dialog.employeedialogue_employeeadhar_lineedit.setText(data['adhar'])
        self.dialog.employeedialogue_employeebasicpay_lineedit.setText(data['salary'])
        index = self.dialog.employeedialogue_employeeshift_combobox.findText(data['shift'])
        self.dialog.employeedialogue_employeeshift_combobox.setCurrentIndex(index)
        index = self.dialog.employeedialogue_employeeperiod_combobox.findText(data['period'])
        self.dialog.employeedialogue_employeeperiod_combobox.setCurrentIndex(index)
        self.dialog.employeedialogue_employeeaddress_textedit.insertPlainText(data['address'])
        self.dialog.employeedialogue_employeecontact_lineedit.setText(data['phone'])


class EmployeeDetail():
    """Empoloyee details management tab"""
    global logger

    def __init__(self):
        ######
        logger.info('Inside EmployeeDetail')
        self.employeedetail_tab_1 = QWidget()  #####taken v
        self.employeedetail_tab_1.setObjectName("employeedetail_tab_1")
        self.gridLayout_16 = QGridLayout(self.employeedetail_tab_1)
        self.gridLayout_16.setObjectName("gridLayout_16")
        spacerItem16 = QSpacerItem(640, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_16.addItem(spacerItem16, 1, 0, 1, 1)
        self.employeetab_add_button = QPushButton(self.employeedetail_tab_1)
        self.employeetab_add_button.setObjectName("employeetab_add_button")
        self.gridLayout_16.addWidget(self.employeetab_add_button, 1, 1, 1, 1)
        self.employeetab_table = QTableWidget(self.employeedetail_tab_1)
        self.employeetab_table.setObjectName("employeetab_table")
        self.employeetab_table.setColumnCount(7)
        self.employeetab_table.setRowCount(0)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.employeetab_table.setHorizontalHeaderItem(6, item)
        self.employeetab_table.horizontalHeader().setCascadingSectionResizes(True)
        self.employeetab_table.horizontalHeader().setStretchLastSection(True)
        self.employeetab_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_16.addWidget(self.employeetab_table, 0, 0, 1, 2)
        ###retranslates
        self.employeetab_add_button.setText(
            QApplication.translate("MainWindow", "Add", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Id", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Name", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Age", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Gender", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Department", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Designation", None, QApplication.UnicodeUTF8))
        self.employeetab_table.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "Shift", None, QApplication.UnicodeUTF8))
        ####signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.employeedetail_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.employeedetail_tab_1.focusInEvent = self.load_rows
        self.employeetab_add_button.clicked.connect(self.popup_employee_form)
        self.employeemanagmentlist = EmployeeManagementList()
        self.get_employee_details()
        self.employeetab_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.employeetab_table.itemDoubleClicked.connect(self.popup_edit)
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """adds shortcuts to the buttons"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtemployee_add']),
                  self.employeedetail_tab_1, self.popup_employee_form)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtemployee_view']),
                  self.employeedetail_tab_1, self.row_selected)

    def row_selected(self):
        """checks the present row selected"""
        rows = sorted(set(index.row() for index in
                          self.employeetab_table.selectedIndexes()))
        if rows:
            self.popup_employee_form(self.employeetab_table.item(rows[0], 0).text())


    def get_employee_details(self):
        """
        populates the table with the employee details
        """
        # should query the db for data
        # for each row in the db call the add_new_row(*args) function
        data = self.employeemanagmentlist.load_data()
        if not data:
            self.employeetab_table.clearContents()
            self.employeetab_table.setRowCount(0)
        self.add_new_row(*data)


    def add_new_row(self, *args):
        """adds a new row entry empty or loaded"""
        table = self.employeetab_table
        if args:  # we dont have data yet
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                item = QTableWidgetItem(j['employee_id'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(j['name'])
                table.setItem(i, 1, item)
                date_string = j['dob']
                born = datetime.strptime(date_string, '%d-%m-%Y')
                today = datetime.today()
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                item = QTableWidgetItem(str(age))
                table.setItem(i, 2, item)
                item = QTableWidgetItem(j['gender'])
                table.setItem(i, 3, item)
                item = QTableWidgetItem(j['department'])
                table.setItem(i, 4, item)
                item = QTableWidgetItem(j['designation'])
                table.setItem(i, 5, item)
                if j.get('shift'):
                    item = QTableWidgetItem(j['shift'])
                    table.setItem(i, 6, item)

        table.setColumnWidth(0, ((table.width() * 0.5) / 7))
        table.setColumnWidth(1, ((table.width() * 2) / 7))
        table.setColumnWidth(2, ((table.width() * 0.5) / 7))
        table.setColumnWidth(3, ((table.width() * 0.5) / 7))
        table.setColumnWidth(4, (table.width() / 7))
        table.setColumnWidth(5, (table.width() / 7))
        table.horizontalHeader().setStretchLastSection(True)

    def popup_employee_form(self, *args):
        """
        who=the employee number of the employee to be viewed
        if no who parameter provided then an empty form pops up...
        shows a form to edit the employee details
        after success adds a new row to te table
        """
        print "form"
        if not args:
            self.popup = EmployeeDetailDialog(parent=self)
            self.popup.exec_()
        else:
            self.popup = EmployeeDetailDialog(parent=self, code=args[0])
            self.popup.exec_()

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.employeetab_table
        print "item spotted"
        model_index = table.indexFromItem(item)
        row = model_index.row()
        self.popup_employee_form(table.item(row, 0).text())

    def load_rows(self, event):
        """
        :return: loads the rows for the table.
        """
        self.add_new_row()


class Attendence():
    """Attendence management tab"""
    global logger

    def __init__(self):
        #####
        logger.info('Inside Attendence')
        self.attendence_tab_2 = QWidget()
        self.attendence_tab_2.setObjectName("attendence_tab_2")
        self.gridLayout_13 = QGridLayout(self.attendence_tab_2)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem17)
        self.attendencetab_dateedit = QDateEdit(self.attendence_tab_2)
        self.attendencetab_dateedit.setInputMethodHints(Qt.ImhPreferNumbers)
        self.attendencetab_dateedit.setCalendarPopup(True)
        self.attendencetab_dateedit.setObjectName("attendencetab_dateedit")
        self.horizontalLayout_15.addWidget(self.attendencetab_dateedit)
        self.attendencetab_search_button = QPushButton(self.attendence_tab_2)
        self.attendencetab_search_button.setObjectName("attendencetab_search_button")
        self.horizontalLayout_15.addWidget(self.attendencetab_search_button)
        self.verticalLayout_10.addLayout(self.horizontalLayout_15)
        self.attendencetab_table = QTableWidget(self.attendence_tab_2)
        font = QFont()
        font.setPointSize(11)
        self.attendencetab_table.setFont(font)
        self.attendencetab_table.setWordWrap(True)
        self.attendencetab_table.setObjectName("attendencetab_table")
        self.attendencetab_table.setColumnCount(6)
        self.attendencetab_table.setRowCount(0)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.attendencetab_table.setHorizontalHeaderItem(5, item)
        self.attendencetab_table.horizontalHeader().setCascadingSectionResizes(True)
        self.attendencetab_table.horizontalHeader().setDefaultSectionSize(120)
        self.attendencetab_table.horizontalHeader().setStretchLastSection(True)
        self.attendencetab_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_10.addWidget(self.attendencetab_table)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.attendencetab_createnew_button = QPushButton(self.attendence_tab_2)
        self.attendencetab_createnew_button.setObjectName("attendencetab_createnew_button")
        self.horizontalLayout_16.addWidget(self.attendencetab_createnew_button)
        spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem18)
        self.attendencetab_save_button = QPushButton(self.attendence_tab_2)
        self.attendencetab_save_button.setObjectName("attendencetab_save_button")
        self.horizontalLayout_16.addWidget(self.attendencetab_save_button)
        self.verticalLayout_10.addLayout(self.horizontalLayout_16)
        self.gridLayout_13.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        ### retranslate
        self.attendencetab_createnew_button.setText(
            QApplication.translate("MainWindow", "Create Attendence", None, QApplication.UnicodeUTF8))
        self.attendencetab_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "dd-MM-yyyy", None, QApplication.UnicodeUTF8))
        self.attendencetab_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.attendencetab_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Attendence", None, QApplication.UnicodeUTF8))
        self.attendencetab_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Employee", None, QApplication.UnicodeUTF8))
        self.attendencetab_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Holiday", None, QApplication.UnicodeUTF8))
        self.attendencetab_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Leave", None, QApplication.UnicodeUTF8))  # leave_applied
        self.attendencetab_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Remark", None, QApplication.UnicodeUTF8))  # leave_reason
        self.attendencetab_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Type", None, QApplication.UnicodeUTF8))  # leave_type
        self.attendencetab_save_button.setText(
            QApplication.translate("MainWindow", "Save", None, QApplication.UnicodeUTF8))
        ### signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.attendencetab_save_button.clicked.connect(self.save_the_data)
        self.attendencetab_search_button.clicked.connect(self.load_the_data)
        self.attendencetab_createnew_button.clicked.connect(self.create_attendence)
        self.attendencetab_table.horizontalHeader().sectionClicked.connect(self.select_all_rows)
        self.attendencetab_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        daysbefore = datetime.today() - timedelta(days=3)
        date3daysbefore = daysbefore.strftime('%d-%m-%Y')
        self.attendencetab_dateedit.setDate(QDate.fromString(date3daysbefore, 'dd-MM-yyyy'))
        self.attendencetab_dateedit.setMaximumDate(QDate.currentDate())
        self.attendence = AttendenceManagement()
        self.attendence_tab_2.setFocusPolicy(Qt.StrongFocus)
        self.attendence_tab_2.focusInEvent = self.load_rows
        self.leave_types = {'none': 'None',
                            'cl': 'Casual Leave',
                            'lop': 'Loss of Pay',
                            'compoff': 'Compansatory Off'}
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """shortcuts entry function"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtattendence_search']),
                  self.attendencetab_table, self.load_the_data)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtattendence_save']),
                  self.attendencetab_table, self.save_the_data)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtattendence_create']),
                  self.attendencetab_table, self.create_attendence)

    def select_all_rows(self, item):
        """
        selects all rows in the 0th column
        :param item: column number
        :return:none
        """
        table = self.attendencetab_table
        if item == 0:
            r = table.rowCount()
            for i in range(r):
                chekbox = table.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def load_the_data(self):
        """
        :param date: the qdate value passed when a date is changed
        :return:the attendence of employees on that date
        """
        table = self.attendencetab_table
        data = self.attendence.load_attendence(self.attendencetab_dateedit.text())
        if data[0]:
            self.add_rows(*data[1])
        else:
            table.clearContents()
            table.setRowCount(0)
            msg = QMessageBox.critical(QMessageBox(), 'Error!!', '%s' % data[1], QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                return True

    def create_attendence(self):
        """Creats a new attendence entry"""
        logger.info('Attendence create attendence initiated')
        table = self.attendencetab_table
        data = self.attendence.new_attendence(self.attendencetab_dateedit.text())
        if data[0]:
            self.add_rows(*data[1])
        else:
            table.clearContents()
            table.setRowCount(0)
            msg = QMessageBox.critical(QMessageBox(), 'Error!!', '%s' % data[1], QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                return True

    def add_rows(self, *args):
        """
        :param data: the data passed from the load_data_function
        :return:adds new row to the table
        """
        table = self.attendencetab_table  # should be 0 if we had the data from db and auto increment the count in loop
        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for n, data in enumerate(args):
                chk = QCheckBox()
                table.setCellWidget(n, 0, chk)
                employee = QTableWidgetItem(data['employee'])
                table.setItem(n, 1, employee)
                is_holiday = QCheckBox()
                if data.get('is_holiday'):
                    if data['is_holiday']:
                        is_holiday.setCheckState(Qt.Checked)
                table.setCellWidget(n, 2, is_holiday)
                leave_applied = QCheckBox()
                if data.get('leave_applied'):
                    if data['leave_applied']:
                        leave_applied.setCheckState(Qt.Checked)
                table.setCellWidget(n, 3, leave_applied)
                leave_reason = QLineEdit()
                if data.get('leave_reason'):
                    leave_reason.setText(data['leave_reason'])
                table.setCellWidget(n, 4, leave_reason)
                leave_type = QComboBox()
                leave_type.addItems(self.leave_types.values())
                index = leave_type.findText(self.leave_types[data['leave_type']])
                leave_type.setCurrentIndex(index)
                table.setCellWidget(n, 5, leave_type)
        table.setColumnWidth(0, table.width() / 6)
        table.setColumnWidth(1, table.width() / 6)
        table.setColumnWidth(2, table.width() / 6)
        table.horizontalHeader().setStretchLastSection(True)

    def save_the_data(self):
        """
        :return:none
        saves the data to the db
        """
        logger.info('Attendence save attandence initiated')
        date_string = self.attendencetab_dateedit.text()
        data = self.get_data()
        if data:
            status = self.attendence.save_attendence(day=date_string, data=data)
            if status[0]:
                msg = QMessageBox.information(QMessageBox(), 'Success!!', '%s' % status[1],
                    QMessageBox.Ok)
                if msg == QMessageBox.Ok:
                    return True
            else:
                msg = QMessageBox.critical(QMessageBox(), 'Failure!!', '%s' % status[1],
                    QMessageBox.Ok)
                if msg == QMessageBox.Ok:
                    return True

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.attendencetab_table
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            dictionary = {}
            checkbox = table.cellWidget(i, 0)
            if checkbox.isChecked():
                employee = table.item(i, 1)
                dictionary['employee'] = employee.text()
                is_holiday = table.cellWidget(i, 2)
                dictionary['is_holiday'] = True if is_holiday.isChecked() else False
                leave_applied = table.cellWidget(i, 3)
                dictionary['leave_applied'] = True if leave_applied.isChecked() else False
                leave_reason = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
                dictionary['leave_reason'] = leave_reason.text()
                if (dictionary['is_holiday'] == False and dictionary['leave_applied'] == False) and \
                                dictionary['leave_reason'] == 'Unassigned':
                    dictionary['leave_reason'] = 'Present'
                elif dictionary['is_holiday'] == True and dictionary['leave_reason'] == 'Unassigned':
                    self.show_error('Remark')
                    return False
                leave_type = self.change_type(table.cellWidget(i, 5))
                dictionary['leave_type'] = leave_type
                if dictionary['leave_applied'] == True and dictionary['leave_reason'] == 'Unassigned':
                    dictionary['leave_reason'] = table.cellWidget(i, 5).currentText()
                dataobj.append(dictionary)
        return dataobj

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), 'Fail!!!', "Please Enter %s properly" % text, QMessageBox.Ok)

    def change_type(self, item):
        """loads the leave type from the backend"""
        text = item.currentText()
        for i, j in self.leave_types.iteritems():
            if text == j:
                value = i
                return value

    def load_rows(self, event):
        """dummy event to get focus"""
        pass


class PayRoll():
    """Payroll management Tab"""
    global logger

    def __init__(self):
        ###
        logger.info('Inside PayRoll')
        self.payroll_tab_3 = QWidget()
        self.payroll_tab_3.setObjectName("payroll_tab_3")
        self.gridLayout_14 = QGridLayout(self.payroll_tab_3)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_7 = QLabel(self.payroll_tab_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_17.addWidget(self.label_7)
        self.payrolltab_type_combobox = QComboBox(self.payroll_tab_3)
        self.payrolltab_type_combobox.setObjectName("payrolltab_type_combobox")
        self.payrolltab_type_combobox.addItem("")
        self.payrolltab_type_combobox.addItem("")
        self.payrolltab_type_combobox.addItem("")
        self.horizontalLayout_17.addWidget(self.payrolltab_type_combobox)
        spacerItem19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem19)
        self.payrolltab_dateedit = QDateEdit(self.payroll_tab_3)
        self.payrolltab_dateedit.setWrapping(False)
        self.payrolltab_dateedit.setCalendarPopup(True)
        self.payrolltab_dateedit.setObjectName("payrolltab_dateedit")
        self.horizontalLayout_17.addWidget(self.payrolltab_dateedit)
        self.payrolltab_search_button = QPushButton(self.payroll_tab_3)
        self.payrolltab_search_button.setObjectName("payrolltab_search_button")
        self.horizontalLayout_17.addWidget(self.payrolltab_search_button)
        self.gridLayout_14.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)
        self.payrolltab_table = QTableWidget(self.payroll_tab_3)
        self.payrolltab_table.setObjectName("payrolltab_table")
        self.payrolltab_table.setColumnCount(6)
        self.payrolltab_table.setRowCount(0)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.payrolltab_table.setHorizontalHeaderItem(5, item)
        self.payrolltab_table.horizontalHeader().setStretchLastSection(True)
        self.payrolltab_table.verticalHeader().setVisible(False)
        self.payrolltab_table.verticalHeader().setCascadingSectionResizes(True)
        self.payrolltab_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_14.addWidget(self.payrolltab_table, 1, 0, 1, 1)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem20)
        self.payrolltab_save_button = QPushButton(self.payroll_tab_3)
        self.payrolltab_save_button.setObjectName("payrolltab_save_button")
        self.horizontalLayout_18.addWidget(self.payrolltab_save_button)
        self.gridLayout_14.addLayout(self.horizontalLayout_18, 2, 0, 1, 1)
        ##retranslate
        self.label_7.setText(
            QApplication.translate("MainWindow", "Select Type:", None, QApplication.UnicodeUTF8))
        self.payrolltab_type_combobox.setItemText(0, QApplication.translate("MainWindow", "Monthly", None,QApplication.UnicodeUTF8))
        self.payrolltab_type_combobox.setItemText(1, QApplication.translate("MainWindow", "Weekly", None,QApplication.UnicodeUTF8))
        self.payrolltab_type_combobox.setItemText(2, QApplication.translate("MainWindow", "Daily", None,QApplication.UnicodeUTF8))
        self.payrolltab_dateedit.setDisplayFormat(
            QApplication.translate("MainWindow", "MMMM-yyyy", None, QApplication.UnicodeUTF8))
        self.payrolltab_search_button.setText(
            QApplication.translate("MainWindow", "Search", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Select", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Id", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Employee", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Total Days", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Total Leaves", None, QApplication.UnicodeUTF8))
        self.payrolltab_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Net Salary", None, QApplication.UnicodeUTF8))
        self.payrolltab_save_button.setText(
            QApplication.translate("MainWindow", "Save and Print", None, QApplication.UnicodeUTF8))
        ###slots and signals && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.buttongroup = QButtonGroup()
        self.buttongroup.setExclusive(True)
        # self.payrolltab_dateedit.dateChanged.connect(self.load_employee_payroll)
        self.payrolltab_save_button.clicked.connect(self.save_and_print)
        self.payrolltab_search_button.clicked.connect(self.load_employee_payroll)
        self.payrolltab_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.payrolltab_table.horizontalHeader().sectionClicked.connect(self.select_all_rows)
        # date = self.payrolltab_dateedit.date()
        # self.load_employee_payroll(date)
        today = datetime.today().strftime('%B-%Y')
        self.payrolltab_dateedit.setDate(QDate.fromString(today, "MMMM-yyyy"))
        self.payroll_tab_3.setFocusPolicy(Qt.StrongFocus)
        self.payroll_tab_3.focusInEvent = self.load_rows
        self.period = {'Monthly': 'monthly', 'Weekly': 'weekly', 'Daily': 'daily'}
        self.payroll = PayrollManagement()
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """Assigns shortcuts for the tabs"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtpayroll_search']),
                  self.payroll_tab_3, self.load_employee_payroll)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtpayroll_save']),
                  self.payroll_tab_3, self.save_and_print)

    def select_all_rows(self, item):
        """
        selects all rows in the 0th column
        :param item: column number
        :return:none
        """
        table = self.payrolltab_table
        if item == 0:
            r = table.rowCount()
            for i in range(r):
                chekbox = table.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def load_employee_payroll(self):
        """
        :param date:passed by datechange event of dateEdit widget provides only month and year no 'day'
        :return:loads the table with the payroll of employees
        """
        table = self.payrolltab_table
        date_string = self.payrolltab_dateedit.text()
        date = datetime.strptime(date_string, '%B-%Y')
        pd = self.payrolltab_type_combobox.currentText()
        period = self.period[pd]
        data = self.payroll.create_payroll(period=period, to_date=date)
        if data:
            self.add_rows(*data)  # should pass this with a list of values with * prefix
        else:
            table.clearContents()
            table.setRowCount(0)

    def add_rows(self, *args):
        """creates a new row entry"""
        table = self.payrolltab_table

        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for i, data in enumerate(args):
                chk = QCheckBox()
                table.setCellWidget(i, 0, chk)
                item = QTableWidgetItem(data['employee_id'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(data['employee'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(data['total_days'])
                table.setItem(i, 3, item)
                item = QTableWidgetItem(data['total_leaves'])
                table.setItem(i, 4, item)
                item = QTableWidgetItem(data['net_salary'])
                table.setItem(i, 5, item)
        table.setColumnWidth(0, ((table.width() * 0.5) / 6))
        table.setColumnWidth(1, ((table.width() * 0.7) / 6))
        table.setColumnWidth(2, ((table.width() * 2) / 6))
        table.setColumnWidth(3, ((table.width() * 0.8) / 6))
        table.setColumnWidth(4, ((table.width() * 0.8) / 6))
        table.horizontalHeader().setStretchLastSection(True)

    def save_and_print(self):
        """
        :return:pops up a payslip of the selected user
        """
        logger.info('PayRoll save and print initiated')
        table = self.payrolltab_table
        row = table.rowCount()
        lines = []
        for i in range(row):
            chk = table.cellWidget(i, 0)
            if chk.isChecked():
                dictionary = {}
                emp_id = table.item(i, 1).text()
                dictionary['employee_id'] = emp_id
                lines.append(dictionary)
        for i in lines:
            date_string = self.payrolltab_dateedit.text()
            date = datetime.strptime(date_string, '%B-%Y')
            pd = self.payrolltab_type_combobox.currentText()
            period = self.period[pd]
            printer_data = self.payroll.save_payroll(data=i, period=period, to_date=date)
            if printer_data:
                dialog = QPrintDialog()
                if dialog.exec_() == QDialog.Accepted:
                    p = dialog.printer()
                    printing = PrintNow(p.printerName(), printer_data, 'payslip')
                    printing.start_print()


    def load_rows(self, event):
        """
        :return:if no rows then adds new rows
        """
        self.add_rows()


class ShiftAddPopup(QDialog):
    """Shift creation popup"""
    global logger

    def __init__(self, slot=None, parent=None):
        QDialog.__init__(self)
        logger.info('Inside ShiftAddPopup')
        self.dialog = Ui_shift_popup()
        self.dialog.setupUi(self)
        self.parent = parent
        self.slot = slot
        self.dialog.shift_name_linedit.textChanged.connect(lambda: self.auto_capital(self.dialog.shift_name_linedit))
        self.dialog.shift_save_button.clicked.connect(self.save_shift)
        self.dialog.shift_delete_button.clicked.connect(self.delete_shift)
        self.shift = ShiftManagement(slot=self.slot)
        if self.slot:
            self.load_slot()
        else:
            self.dialog.shift_name_linedit.setPlaceholderText('Not Assigned')

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def load_slot(self):
        """Loads the shift entries"""
        data = self.shift.load_shift()
        self.dialog.shift_name_linedit.setText(data['slot'])
        self.dialog.shift_intime_timeedit.setTime(QTime.fromString(data['in_time'], 'hh:mm AP'))
        self.dialog.shift_outtime_timeedit.setTime(QTime.fromString(data['out_time'], 'hh:mm AP'))
        self.dialog.shift_mon_checkbox.setCheckState(Qt.Checked) if data['monday'] else None
        self.dialog.shift_tue_checkbox.setCheckState(Qt.Checked) if data['tuesday']  else None
        self.dialog.shift_wed_checkbox.setCheckState(Qt.Checked) if data['wednesday']else None
        self.dialog.shift_thu_checkbox.setCheckState(Qt.Checked) if data['thursday'] else None
        self.dialog.shift_fri_checkbox.setCheckState(Qt.Checked) if data['friday']   else None
        self.dialog.shift_sat_checkbox.setCheckState(Qt.Checked) if data['saturday'] else None
        self.dialog.shift_sun_checkbox.setCheckState(Qt.Checked) if data['sunday']   else None

    def save_shift(self):
        """Saves a shift entry"""
        logger.info('ShiftAddPopup save shift initiated')
        data = {}
        data['slot'] = self.dialog.shift_name_linedit.text()
        data['in_time'] = self.dialog.shift_intime_timeedit.text()
        data['out_time'] = self.dialog.shift_outtime_timeedit.text()
        data['monday'] = True if self.dialog.shift_mon_checkbox.isChecked() else False
        data['tuesday'] = True if self.dialog.shift_tue_checkbox.isChecked() else False
        data['wednesday'] = True if self.dialog.shift_wed_checkbox.isChecked() else False
        data['thursday'] = True if self.dialog.shift_thu_checkbox.isChecked() else False
        data['friday'] = True if self.dialog.shift_fri_checkbox.isChecked() else False
        data['saturday'] = True if self.dialog.shift_sat_checkbox.isChecked() else False
        data['sunday'] = True if self.dialog.shift_sun_checkbox.isChecked() else False
        if data['slot'] == '':
            QMessageBox.critical(QMessageBox(), 'Error', 'Invalid Shift Name', QMessageBox.Ok)
            return False
        state = self.shift.save_shift(data)
        if not state[0]:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!', '%s!!' % state[1], QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                return False
        else:
            self.parent.get_shift_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % state[1],QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()

    def delete_shift(self):
        """deletes  a shift entry"""
        logger.info('ShiftAddPopup delete initiated')
        state = self.shift.delete_shift()
        if not state[0]:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!', '%s!!' % state[1], QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                return False
        else:
            self.parent.get_shift_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % state[1],QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                self.close()


class Shift():
    """shift management tab"""
    global logger

    def __init__(self):
        ######
        logger.info('Inside Shift')
        self.shift_tab_4 = QWidget()  #####taken v
        self.shift_tab_4.setObjectName("shift_tab_4")
        self.gridLayout_16 = QGridLayout(self.shift_tab_4)
        self.gridLayout_16.setObjectName("gridLayout_16")
        spacerItem16 = QSpacerItem(640, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_16.addItem(spacerItem16, 1, 0, 1, 1)
        self.shifttab_add_button = QPushButton(self.shift_tab_4)
        self.shifttab_add_button.setObjectName("shifttab_add_button")
        self.gridLayout_16.addWidget(self.shifttab_add_button, 1, 1, 1, 1)
        self.shifttab_table = QTableWidget(self.shift_tab_4)
        self.shifttab_table.setObjectName("shifttab_table")
        self.shifttab_table.setColumnCount(10)
        self.shifttab_table.setRowCount(0)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.shifttab_table.setHorizontalHeaderItem(9, item)
        self.shifttab_table.horizontalHeader().setCascadingSectionResizes(True)
        self.shifttab_table.horizontalHeader().setStretchLastSection(True)
        self.shifttab_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_16.addWidget(self.shifttab_table, 0, 0, 1, 2)
        ###retranslates
        self.shifttab_add_button.setText(
            QApplication.translate("MainWindow", "Add Shift", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Slot", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "In Time", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Out Time", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "MON", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "TUE", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "WED", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(6).setText(
            QApplication.translate("MainWindow", "THU", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(7).setText(
            QApplication.translate("MainWindow", "FRI", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(8).setText(
            QApplication.translate("MainWindow", "SAT", None, QApplication.UnicodeUTF8))
        self.shifttab_table.horizontalHeaderItem(9).setText(
            QApplication.translate("MainWindow", "SUN", None, QApplication.UnicodeUTF8))
        ####signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.shift = ShiftList()
        self.shift_tab_4.setFocusPolicy(Qt.StrongFocus)
        self.shift_tab_4.focusInEvent = self.load_rows
        # self.get_shift_details()
        self.shifttab_add_button.clicked.connect(self.popup_shift_form)
        self.shifttab_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.shifttab_table.itemDoubleClicked.connect(self.popup_edit)
        self.get_shift_details()
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns the shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtshift_view']),
                  self.shift_tab_4, self.row_selected)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtshift_add']),
                  self.shift_tab_4, self.popup_shift_form)

    def row_selected(self):
        """checks the row presently selected"""
        rows = sorted(set(index.row() for index in
                          self.shifttab_table.selectedIndexes()))
        if rows:
            self.popup_shift_form(self.shifttab_table.item(rows[0], 0).text())

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.shifttab_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        self.popup_shift_form(table.item(row, 0).text())

    def get_shift_details(self):
        """
        populates the table with the shift details
        """
        # should query the db for data
        # for each row in the db call the add_new_row(*args) function
        data = self.shift.load_shifts()
        if not data:
            self.shifttab_table.clearContents()
            self.shifttab_table.setRowCount(0)
        else:
            self.add_new_row(*data)

    def add_new_row(self, *args):
        """adds new row entry"""
        table = self.shifttab_table
        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for i, data in enumerate(args):
                item = QTableWidgetItem(data['slot'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(data['in_time'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(data['out_time'])
                table.setItem(i, 2, item)
                if data['monday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 3, check)
                if data['tuesday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 4, check)
                if data['wednesday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 5, check)
                if data['thursday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 6, check)
                if data['friday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 7, check)
                if data['saturday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 8, check)
                if data['sunday']:
                    check = QCheckBox()
                    check.setCheckState(Qt.Checked)
                    check.setDisabled(True)
                    table.setCellWidget(i, 9, check)
        table.setColumnWidth(0, ((table.width() * 2) / 10))
        table.setColumnWidth(1, ((table.width() * 2) / 10))
        table.setColumnWidth(2, ((table.width() * 2) / 10))
        table.setColumnWidth(3, ((table.width() * 0.5) / 10))
        table.setColumnWidth(4, ((table.width() * 0.5) / 10))
        table.setColumnWidth(5, ((table.width() * 0.5) / 10))
        table.setColumnWidth(6, ((table.width() * 0.5) / 10))
        table.setColumnWidth(7, ((table.width() * 0.5) / 10))
        table.setColumnWidth(8, ((table.width() * 0.5) / 10))
        table.horizontalHeader().setStretchLastSection(True)

    def popup_shift_form(self, *args):
        """
        who=the shift number of the shift to be viewed
        if no who parameter provided then an empty form pops up...
        shows a form to edit the shift details
        after success adds a new row to te table
        """
        print "form"
        if not args:
            self.popup = ShiftAddPopup(parent=self)
            self.popup.exec_()
        else:
            self.popup = ShiftAddPopup(parent=self, slot=args[0])
            self.popup.exec_()

    def load_rows(self, event):
        """
        :return: loads the rows for the table.
        """
        self.add_new_row()


class SalarySettingsPopup(QDialog):
    """Salary settings entry popup"""
    global logger

    def __init__(self, designation=None, parent=None):
        logger.info('Inside SalarySettingPopup')
        QDialog.__init__(self)
        self.dialog = Ui_salary_settings()
        self.dialog.setupUi(self)
        self.designation = designation
        self.parent = parent
        self.dialog.salarysettings_save_button.clicked.connect(self.save_settings)
        self.dialog.salarysettings_delete_button.clicked.connect(self.delete_settings)
        self.dialog.salarysettings_newdesignation_button.clicked.connect(self.pop_new_designation)
        self.management = EmployeeManagement()
        self.salary_setting = SalarySettingManagement(self.designation)
        # self.dialog.salarysettings_designation_combobox.setPlaceholderText('Not Assigned')
        # self.dialog.salarysettings_designation_combobox.textChanged.connect(
        #     lambda: self.auto_capital(self.dialog.salarysettings_designation_combobox))
        self.load_designation()
        if self.designation:
            self.load_settings()
            self.dialog.salarysettings_newdesignation_button.setVisible(False)
        else:
            pass

    def pop_new_designation(self):
        """pops up new designation"""
        designation = NewDesignation(parent=self, emp_management_obj=self.management)
        designation.exec_()

    def load_designation(self):
        """loads the designation entries"""
        combo = self.dialog.salarysettings_designation_combobox
        data = self.management.load_designation()
        combo.clear()
        combo.addItems(data)


    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def load_settings(self):
        """loads the salary settings details"""
        data = self.salary_setting.load_setting()
        index = self.dialog.salarysettings_designation_combobox.findText(data['designation'])
        self.dialog.salarysettings_designation_combobox.setCurrentIndex(index)
        self.dialog.salarysettings_da_linedit.setText(data['da'])
        self.dialog.salarysettings_hra_linedit.setText(data['hra'])
        self.dialog.salarysettings_pf_linedit.setText(data['pf'])
        self.dialog.salarysettings_esi_linedit.setText(data['esi'])
        self.dialog.salarysettings_proftax_linedit.setText(data['proftax'])


    def save_settings(self):
        """saves the settings details"""
        logger.info('SalarySettingPopup save initiated')
        data = {}
        data['designation'] = self.dialog.salarysettings_designation_combobox.currentText()
        data['da'] = self.dialog.salarysettings_da_linedit.text()
        data['hra'] = self.dialog.salarysettings_hra_linedit.text()
        data['pf'] = self.dialog.salarysettings_pf_linedit.text()
        data['esi'] = self.dialog.salarysettings_esi_linedit.text()
        data['proftax'] = self.dialog.salarysettings_proftax_linedit.text()
        for i, j in data.iteritems():
            if j == '':
                QMessageBox.critical(QMessageBox(), 'Error', 'Invalid %s value' % i.title(), QMessageBox.Ok)
                return False
        state = self.salary_setting.save_setting(data)
        if not state[0]:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!', '%s!!' % state[1], QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                return False
        else:
            self.parent.get_salary_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % state[1],
                QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()

    def delete_settings(self):
        """deletes the salary setting entry"""
        logger.info('SalarySettingPopup delete initiated')
        state = self.salary_setting.delete_setting()
        if not state[0]:
            msg = QMessageBox.critical(QMessageBox(), 'Fail!', '%s!!' % state[1], QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Ok:
                return False
        else:
            self.parent.get_salary_details()
            msg = QMessageBox.information(QMessageBox(), 'Success!!', "%s!!" % state[1], QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()


class SalarySettings():
    """Salarysettings management Tab"""
    global logger

    def __init__(self):
        ######
        logger.info('Inside SalarySettings')
        self.salary_tab_5 = QWidget()  #####taken v
        self.salary_tab_5.setObjectName("salary_tab_5")
        self.gridLayout_16 = QGridLayout(self.salary_tab_5)
        self.gridLayout_16.setObjectName("gridLayout_16")
        spacerItem16 = QSpacerItem(640, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_16.addItem(spacerItem16, 1, 0, 1, 1)
        self.salarysetting_add_button = QPushButton(self.salary_tab_5)
        self.salarysetting_add_button.setObjectName("salarysetting_add_button")
        self.gridLayout_16.addWidget(self.salarysetting_add_button, 1, 1, 1, 1)
        self.salarysetting_table = QTableWidget(self.salary_tab_5)
        self.salarysetting_table.setObjectName("salarysetting_table")
        self.salarysetting_table.setColumnCount(6)
        self.salarysetting_table.setRowCount(0)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.salarysetting_table.setHorizontalHeaderItem(5, item)
        self.salarysetting_table.horizontalHeader().setCascadingSectionResizes(True)
        self.salarysetting_table.horizontalHeader().setStretchLastSection(True)
        self.salarysetting_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_16.addWidget(self.salarysetting_table, 0, 0, 1, 2)
        ###retranslates
        self.salarysetting_add_button.setText(
            QApplication.translate("MainWindow", "New Salary Setting", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Designation", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "DA", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "HRA", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "PF", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "ESI", None, QApplication.UnicodeUTF8))
        self.salarysetting_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "PT", None, QApplication.UnicodeUTF8))
        ####signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.salary_tab_5.setFocusPolicy(Qt.StrongFocus)
        self.salary_tab_5.focusInEvent = self.load_rows
        self.salarysetting_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.salarysetting_table.itemDoubleClicked.connect(self.popup_edit)
        self.salarysetting_add_button.clicked.connect(self.popup_salarysettings_form)
        self.salarysettinglist = SalarySettingList()
        self.get_salary_details()
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assigns shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtsal_view']),
                  self.salary_tab_5, self.row_selected)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_empmgtsal_new']),
                  self.salary_tab_5, self.popup_salarysettings_form)

    def row_selected(self):
        """determines the present row selected"""
        rows = sorted(set(index.row() for index in
                          self.salarysetting_table.selectedIndexes()))
        if rows:
            self.popup_salarysettings_form(self.salarysetting_table.item(rows[0], 0).text())


    def get_salary_details(self):
        """
        populates the table with the employee details
        """
        data = self.salarysettinglist.load_salary_setting()
        if data:
            self.add_new_row(*data)
        else:
            self.salarysetting_table.clearContents()
            self.salarysetting_table.setRowCount(0)

    def add_new_row(self, *args):
        """new row entry"""
        table = self.salarysetting_table
        if args:
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(args))
            for i, data in enumerate(args):
                item = QTableWidgetItem(data['designation'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(data['da'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(data['hra'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(data['pf'])
                table.setItem(i, 3, item)
                item = QTableWidgetItem(data['esi'])
                table.setItem(i, 4, item)
                item = QTableWidgetItem(data['proftax'])
                table.setItem(i, 5, item)
        table.setColumnWidth(0, (table.width() / 6))
        table.setColumnWidth(1, (table.width() / 6))
        table.setColumnWidth(2, (table.width() / 6))
        table.setColumnWidth(3, (table.width() / 6))
        table.setColumnWidth(4, (table.width() / 6))
        table.horizontalHeader().setStretchLastSection(True)

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.salarysetting_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        self.popup_salarysettings_form(table.item(row, 0).text())

    def popup_salarysettings_form(self, *args):
        """
        who=the employee number of the employee to be viewed
        if no who parameter provided then an empty form pops up...
        shows a form to edit the employee details
        after success adds a new row to te table
        """
        if not args:
            self.popup = SalarySettingsPopup(parent=self)
            self.popup.exec_()
        else:
            self.popup = SalarySettingsPopup(parent=self, designation=args[0])
            self.popup.exec_()

    def load_rows(self, event):
        """
        :return: loads the rows for the table.
        """
        self.add_new_row()
