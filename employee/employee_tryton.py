#! /usr/bin/env python

""" Employee Module backend """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

import calendar
from decimal import Decimal
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction

from datetime import datetime, timedelta
import inflect
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class EmployeeManagement():
    """
    Manages the Employees
    """

    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Designation = pool.get('employee.designation')
        Department = pool.get('department.department')
        Employee = pool.get('company.employee')
        Salary = pool.get('payroll.salary')
        SalarySettings = pool.get('payroll.salarysettings')
        Party = pool.get('party.party')
        Shift = pool.get('attendance.shiftdetails')
        User = pool.get('res.user')
        Account = pool.get('account.account')
        Address = pool.get('party.address')
        Contact_Mechanism = pool.get('party.contact_mechanism')

    def __init__(self, emp_id=None):
        logger.info('Inside EmployeeManagement')
        with Transaction().start(DBNAME, 1):
            user = self.User(id=1)
            self.company = user.main_company
            accounts = self.Account.search([
                ('kind', 'in', ['receivable', 'payable', 'revenue', 'expense']),
                ('company', '=', self.company.id), ])

            self.accounts = {a.kind: a for a in accounts}

            self.employee_id = emp_id
            self.employee = None
            if self.employee_id:
                employee = self.Employee.search(['employee_id', '=', self.employee_id])
                if employee:
                    self.employee = employee[0]

    def get_shift_list(self):
        """
        searches for the shifts that exists
        :return:the list of shifts
        """
        with Transaction().start(DBNAME, 1):
            shifts = tuple(i.slot for i in self.Shift.search([]))
            return shifts

    def load_employee(self):
        """
        loads the employee corresponding to the id employee_id passed in the initialization
        :return:data dictionary object with use details
        """
        with Transaction().start(DBNAME, 1):
            if self.employee_id:
                self.employee = self.Employee.search(['employee_id', '=', self.employee_id])[0]
                employee = self.employee
                data = {}
                data['employee_id'] = str(employee.employee_id)
                data['department'] = employee.department.name
                data['designation'] = employee.designation.name
                data['name'] = employee.name
                data['surname'] = employee.surname
                data['fathersname'] = employee.fathersname
                data['gender'] = employee.gender.title()
                data['dob'] = employee.dob.strftime("%d-%m-%Y")
                data['doj'] = employee.doj.strftime("%d-%m-%Y")
                data['pan'] = employee.pan
                data['adhar'] = employee.adhar
                data['salary'] = str(employee.salary.basic_pay)
                data['shift'] = employee.shift.slot if employee.shift else None
                data['period'] = employee.salary.period.title()
                data['phone'] = employee.party.phone
                data['address'] = employee.party.addresses[0].full_address
                return data

    def save_employee(self, data):
        """
        saves the employee details
        :param data:the data dictionary with the use details
        :return:boolean value True if the employee saved
        """
        logger.info('EmployeeManagement save employee initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                if self.employee_id:  # edit mode
                    if int(data['employee_id']) != int(self.employee_id):
                        check = self.Employee.search(['employee_id', '=', int(data['employee_id'])])
                        if check:
                            return [False, 'Duplicate entry with same employee-id']
                    else:
                        employee = self.Employee(id=self.employee.id)
                        salary = self.Salary(id=employee.salary.id)
                        party = self.Party(id=employee.party.id)
                        address = self.Address(id=employee.party.addresses[0])
                        contact_mechanism = self.Contact_Mechanism(id=party.contact_mechanisms[0].id)
                else:
                    employee = self.Employee()
                    salary = self.Salary()
                    party = self.Party()
                    party.account_payable = self.accounts['payable']
                    party.account_receivable = self.accounts['receivable']
                    address = self.Address()
                    party.addresses = (address,)
                    contact_mechanism = self.Contact_Mechanism()
                    party.contact_mechanisms = (contact_mechanism,)
                    contact_mechanism.type = 'phone'
                    check = self.Employee.search(['employee_id', '=', int(data['employee_id'])])
                    if check:
                        return [False, 'Duplicate entry with same employee-id']
                department = self.Department.search(['name', '=', data['department']])[-1]
                designation = self.Designation.search(['name', '=', data['designation']])[-1]
                setting = self.SalarySettings.search(['designation', '=', designation.id])
                if setting:
                    salary_settings = setting[-1]
                else:
                    salary_settings = self.SalarySettings()
                employee.employee_id = int(data['employee_id'])
                employee.department = department
                employee.designation = designation
                try:
                    sal_des_list = list[salary_settings.designation]
                    sal_des_list.append(designation)
                except Exception:
                    sal_des_list = (designation,)
                salary_settings.designation = sal_des_list
                employee.name = data['name']
                employee.surname = data['surname']
                employee.fathersname = data['fathersname']
                employee.gender = data['gender'].lower()
                employee.dob = datetime.strptime(data['dob'], "%d-%m-%Y")
                employee.doj = datetime.strptime(data['doj'], "%d-%m-%Y")
                employee.pan = data['pan']
                employee.adhar = data['adhar']
                salary.basic_pay = Decimal(data['salary'])
                salary.salary_settings = salary_settings
                salary.period = (data['period']).lower()
                party.name = data['name']
                contact_mechanism.value = data['phone']
                address.street = data['address']
                employee.salary = salary
                employee.party = party
                if data['shift']:
                    shift = self.Shift.search(['slot', '=', data['shift']])[0]
                    employee.shift = shift
                    employee.shift.slot = data['shift']
                employee.company = self.company
                salary_settings.save()
                salary.save()
                party.save()
                employee.save()
                self.employee_id = int(data['employee_id'])
                self.employee = employee
                transaction.cursor.commit()
                return [True, 'Employee saved']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown Issue']

    def remove_employee(self):
        """
        removes an employee corresponding to the employee_id passed in the initialization
        :return: booloean value True if the employee is deleted
        """
        logger.info('EmployeeManagement delete employee initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                if self.employee_id:
                    if self.employee:
                        employee = self.Employee(id=self.employee.id)
                        party = employee.party
                        address = party.addresses[0]
                        employee.delete((employee,))
                        address.delete((address,))
                        party.delete((party,))
                        transaction.cursor.commit()
                        return True
                return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_designation(self):
        """
        loads the designation list
        :return: the list of designations
        """
        with Transaction().start(DBNAME, 1):
            designation_list = tuple(i.name for i in self.Designation.search([]))
            return designation_list

    def load_department(self):
        """
        loads the department list
        :return: the list of departments
        """
        with Transaction().start(DBNAME, 1):
            department_list = [i.name for i in self.Department.search([])]
            return department_list

    def save_department(self, data):
        """
        saves the department
        :param data:data dictionary with the department values to be saved
        :return: boolean values if True the department is saved
        """
        logger.info('EmployeeManagement save department initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                chk = self.Department.search(
                    ['OR', [('department_id', '=', int(data['dep_id'])), ], [('name', '=', data['name']), ], ])
                if chk:
                    return [False, 'Duplicate Department entry']
                else:
                    department = self.Department()
                    department.name = data['name']
                    department.department_id = int(data['dep_id'])
                    department.company = self.company

                    department.save()
                    transaction.cursor.commit()
                    return [True, 'Successfully saved the Department']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown Error']

    def delete_department(self, data):
        """
        deletes the department
        :param data:data dictionary with the department values to be deleted
        :return: boolean values if True the department is deleted
        """
        logger.info('EmployeeManagement delete department initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                chk = self.Department.search([('name', '=', data['name'])])
                if chk:
                    department = chk[0]
                    emp_list = department.employees
                    if emp_list:
                        return [False, 'Employees Exist in the Department']
                    else:
                        department.delete()
                        transaction.cursor.commit()
                        return [True, 'Department deleted successfully']
                else:
                    return [False, 'Record Not Found']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unkown error check debug']

    def save_designation(self, data):
        """
        saves the designation
        :param data:data dictionary with the designation values to be saved
        :return: boolean values if True the designation is saved
        """
        logger.info('EmployeeManagement designation save initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                chk = self.Designation.search(
                    ['OR', [('code', '=', int(data['des_code'])), ], [('name', '=', data['name']), ], ])
                if chk:
                    return [False, 'Duplicate Designation entry']
                else:
                    designation = self.Designation()
                    designation.name = data['name']
                    designation.code = int(data['des_code'])

                    designation.save()
                    transaction.cursor.commit()
                    return [True, 'Successfully saved the Designation']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown Error']

    def delete_designation(self, data):
        """
        deletes the designation
        :param data:data dictionary with the designation values to be deleted
        :return: boolean values if True the designation is deleted
        """
        logger.info('EmployeeManagement delete designation initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                chk = self.Designation.search([('name', '=', data['name'])])
                if chk:
                    designation = chk[0]
                    emp_list = designation.employees
                    if emp_list:
                        return [False, 'Employees exists in the Designation, change their designation to delete']
                    else:
                        designation.delete((designation,))
                        transaction.cursor.commit()
                        return [True, 'Designation deleted successfully']
                else:
                    return [False, 'Record Not Found']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown Error']


class EmployeeManagementList():
    """
    Lists out the general registered employee list
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Employee = pool.get('company.employee')

    def __init__(self):
        logger.info('Inside EmployeeManagementList')


    def load_data(self):
        """
        loads the employee details
        :return:list with the dictionary of employee data
        """
        with Transaction().start(DBNAME, 1):
            employee = self.Employee.search([])
            lines = []
            for i in employee:
                data = {}
                data['employee_id'] = str(i.employee_id)
                data['department'] = i.department.name.title()
                data['designation'] = i.designation.name.title()
                data['name'] = i.name
                data['gender'] = i.gender.title()
                data['dob'] = i.dob.strftime("%d-%m-%Y")
                data['shift'] = i.shift.slot
                lines.append(data)
            return lines


class AttendenceManagement():
    """
    Manages the attendance of the employees
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Employee = pool.get('company.employee')
        Shift = pool.get('attendance.shiftdetails')
        Payroll = pool.get('payroll.payroll')
        Attendence = pool.get('attendance.attendance')

    def __init__(self):
        logger.info('Inside AttendenceManagement')

    def new_attendence(self, day):
        """
        Creates a new attendance of the for a day
        :param day:day string eg:'20-06-2015'
        :return:boolean value True if the attendance was created successfully
        """
        logger.info('AttendenceManagement new attendence initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                day_string = day
                day = datetime.strptime(day_string, '%d-%m-%Y')
                today = datetime.today()
                employee_list = self.Employee.search([])
                attendence_check = self.Attendence.search(['date', '=', day])
                if attendence_check:
                    pass
                else:
                    if (today - day).days > 3:
                        return [False, 'Cannot create attendance for a date more than 3 days back']
                    lines = []
                    for i in employee_list:
                        dictionary = {}
                        attendence = self.Attendence()
                        attendence.employee = i
                        attendence.shift = i.shift
                        attendence.date = day
                        attendence.leave_type = 'none'
                        attendence.is_holiday = False  # for unknown reason it is being default True
                        attendence.leave_reason = 'Unassigned'
                        attendence.leave_applied = False
                        dictionary['employee'] = attendence.employee.name
                        dictionary['leave_applied'] = attendence.leave_applied
                        dictionary['leave_reason'] = 'Unassigned'
                        dictionary['leave_type'] = attendence.leave_type
                        try:
                            attendence.save()
                        except Exception:
                            return [False, 'Cannot create Attendence']
                        lines.append(dictionary)
                    transaction.cursor.commit()
                    return [True, lines]
            lines = self.load_attendence(day_string)
            return lines
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unkown Error check debug']

    def load_attendence(self, day):
        """
        loads the attendance for the particular day
        :param day:the date string  eg:'20-06-2015'
        :return:the list of dictionary with the attendance details
        """
        with Transaction().start(DBNAME, 1):
            day_string = day
            day = datetime.strptime(day_string, '%d-%m-%Y')
            attendence_list = self.Attendence.search(['date', '=', day])
            lines = []
            for i in attendence_list:
                dictionary = {}
                dictionary['employee'] = i.employee.name
                dictionary['leave_applied'] = i.leave_applied
                dictionary['leave_reason'] = i.leave_reason
                dictionary['leave_type'] = i.leave_type
                dictionary['is_holiday'] = i.is_holiday
                lines.append(dictionary)
            if lines:
                return [True, lines]
            else:
                return [False, 'No Attendance Found']

    def save_attendence(self, data, day):
        """
        saves the attendance for the corresponding day
        :param data:the attendance data list of dictionaries with the details
        :param day:the date string eg:'20-06-2015'
        :return:boolean data True if attendance was saved successfully
        """
        logger.info('AttendenceManagement save attendence initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                day_string = day
                day = datetime.strptime(day_string, '%d-%m-%Y')
                today = datetime.today()
                if (today - day).days > 3:
                    return [False, 'Cannot Edit Attendance prior 3 days']
                attendence_list = self.Attendence.search(['date', '=', day])
                if attendence_list:
                    for i in data:
                        for j in attendence_list:
                            if i['employee'] == j.employee.name:
                                j.leave_applied = i['leave_applied']
                                j.leave_reason = i['leave_reason']
                                j.leave_type = i['leave_type']
                                j.is_holiday = i['is_holiday']
                                j.in_time = j.employee.shift.in_time
                                j.save()
                    transaction.cursor.commit()
                    return [True, 'Attendence data saved']
                return [False, 'No Attendence Data Available']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unkown Error check debug']


class PayrollManagement():
    """
    manages the payroll of the employees
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Payroll = pool.get('payroll.payroll')
        Employee = pool.get('company.employee')

    def __init__(self):
        logger.info('Inside PayrollManagement')

    def create_payroll(self, period, to_date):
        """
        creates a payroll for the particular date
        :param period:period of shift [monthly,weekly,daily]
        :param to_date:the maximum date
        :return:the list of dictionary of payroll details
        """
        logger.info('PayrollManagement create payroll initiated')
        lines = []
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                employee_list = self.Employee.search([])
                if employee_list:
                    for i in employee_list:
                        if i.salary.period == period:
                            dictionary = {}
                            payroll = self.Payroll()
                            payroll.salary_settings = i.designation.salary_setting
                            payroll.basic_pay = i.salary.basic_pay
                            payroll.period = i.salary.period
                            if i.salary.period == 'monthly':
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                from_date = datetime(year=to_date.year, month=to_date.month, day=1)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                            elif i.salary.period == 'weekly':
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                                from_date = to_date - timedelta(days=6)
                            else:
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                                from_date = to_date - timedelta(days=1)
                            exist_previous = payroll.search([('to_date', '<', from_date),
                                                             ('employee', '=', i.id), ('status', '=', 'paid')])
                            if exist_previous:
                                date_sort = []
                                for j in exist_previous:
                                    date_sort.append(j.to_date)
                                date_sort.sort()
                                payroll.from_date = date_sort[-1] + timedelta(days=1)
                            else:
                                payroll.from_date = from_date
                            payroll.to_date = to_date
                            payroll.month = str(to_date.month)
                            payroll.status = 'draft'
                            payroll.other_deductions = Decimal(0)
                            payroll.employee = i
                            payroll.save()
                            transaction.cursor.commit()
                            dictionary['employee_id'] = str(i.employee_id)
                            dictionary['employee'] = i.name
                            dictionary['total_days'] = str(payroll.total_days)
                            dictionary['total_leaves'] = str(len(payroll.get_leaves('leaves')))
                            dictionary['net_salary'] = Decimal(payroll.net_pay4duration).to_eng_string()
                            lines.append(dictionary)
                            payroll.delete((payroll,))
                            transaction.cursor.commit()
                return lines
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return lines

    def save_payroll(self, data, period, to_date):
        """
        creates a payroll for the particular date
        :param data:the list of dictionary of payroll details
        :param period:period of shift [monthly,weekly,daily]
        :param to_date:the maximum date
        :return:the list of dictionary of payroll details or boolean value False if failed or could not save
        """
        logger.info('PayrollManagement save payroll initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                employee_list = self.Employee.search(['employee_id', '=', int(data['employee_id'])])
                if employee_list:
                    for i in employee_list:
                        if i.salary.period == period:
                            print i
                            dictionary = {}
                            payroll = self.Payroll()
                            payroll.salary_settings = i.designation.salary_setting
                            payroll.basic_pay = i.salary.basic_pay
                            payroll.period = i.salary.period
                            if i.salary.period == 'monthly':
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                from_date = datetime(year=to_date.year, month=to_date.month, day=1)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                            elif i.salary.period == 'weekly':
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                                from_date = to_date - timedelta(days=6)
                            else:
                                _, last = calendar.monthrange(to_date.year, to_date.month)
                                to_date = datetime(year=to_date.year, month=to_date.month, day=last)
                                from_date = to_date - timedelta(days=1)
                            exist_previous = payroll.search(
                                [('to_date', '<', from_date), ('employee', '=', i.id), ('status', '=', 'paid')])
                            if exist_previous:
                                date_sort = []
                                for j in exist_previous:
                                    date_sort.append(j.to_date)
                                date_sort.sort()
                                payroll.from_date = date_sort[-1] + timedelta(days=1)
                            else:
                                payroll.from_date = from_date
                            payroll.to_date = to_date
                            payroll.month = str(to_date.month)
                            payroll.status = 'draft'
                            payroll.other_deductions = Decimal(0)
                            payroll.employee = i
                            payroll.save()
                            transaction.cursor.commit()
                            dictionary['employee'] = i.name
                            dictionary['designation'] = i.designation.name
                            dictionary['pan'] = i.pan
                            dictionary['date'] = to_date
                            dictionary['basic_pay'] = payroll.basic_pay
                            dictionary['da'] = payroll.da
                            dictionary['gross'] = payroll.gross_pay4duration
                            dictionary['hra'] = payroll.hra
                            dictionary['pf'] = payroll.pf
                            dictionary['esi'] = payroll.esi
                            dictionary['professional_tax'] = payroll.professional_tax
                            dictionary['other_deductions'] = payroll.leave_deduction
                            dictionary['total_deduction'] = dictionary['pf'] + dictionary['esi'] + dictionary[
                                'professional_tax'] + (dictionary['other_deductions'] if dictionary.get(
                                'other_deductions') else 0)
                            dictionary['net'] = payroll.net_pay4duration
                            p = inflect.engine()
                            dictionary['rupees'] = p.number_to_words(payroll.net_pay4duration)
                            payroll.status = 'paid'
                            payroll.save()
                            transaction.cursor.commit()
                            return dictionary
                return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class ShiftManagement():
    """
    Manages the shift details
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Shift = pool.get('attendance.shiftdetails')
        Employee = pool.get('company.employee')

    def __init__(self, slot=None):
        logger.info('Inside ShiftManagement')
        self.slot = slot

    def save_shift(self, data):
        """
        saves the shift with the corresponding data
        :param data:dictionary of the shift details
        :return:boolean True is the shift was saved
        """
        logger.info('ShiftManagement save shift initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                if not self.slot:
                    shift = self.Shift()
                    chk = self.Shift.search(['slot', '=', data['slot']])
                    if chk:
                        return [False, 'Duplicate slot entry']
                else:
                    shift = self.Shift.search(['slot', '=', self.slot])[0]
                    if self.slot != data['slot']:
                        chk = self.Shift.search(['slot', '=', data['slot']])
                        if chk:
                            return [False, 'Duplicate slot entry']
                shift.slot = data['slot']
                shift.in_time = datetime.strptime(data['in_time'], '%H:%M %p').time()
                shift.out_time = datetime.strptime(data['out_time'], '%H:%M %p').time()
                shift.monday = data['monday']
                shift.tuesday = data['tuesday']
                shift.wednesday = data['wednesday']
                shift.thursday = data['thursday']
                shift.friday = data['friday']
                shift.saturday = data['saturday']
                shift.sunday = data['sunday']
                shift.save()
                transaction.cursor.commit()
                self.slot = data['slot']
                return [True, 'The Shift was saved']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unkown error check debug']

    def load_shift(self):
        """
        loads the shift details for the corresponding slot details passed in the initialization
        :return:the dictionary of the shift details for the corresponding slot
        """
        with Transaction().start(DBNAME, 1):
            if self.slot:
                shift = self.Shift.search(['slot', '=', self.slot])[0]
                data = {}
                data['slot'] = shift.slot
                data['in_time'] = shift.in_time.strftime('%H:%M %p')
                data['out_time'] = shift.out_time.strftime('%H:%M %p')
                data['monday'] = shift.monday
                data['tuesday'] = shift.tuesday
                data['wednesday'] = shift.wednesday
                data['thursday'] = shift.thursday
                data['friday'] = shift.friday
                data['saturday'] = shift.saturday
                data['sunday'] = shift.sunday
                return data
        return [False, 'No such entry']

    def delete_shift(self):
        """
        deletes the particular shift
        :return:boolean value if the shift was deleted
        """
        logger.info('ShiftManagement delete shift initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                if self.slot:
                    shift = self.Shift.search(['slot', '=', self.slot])[0]
                    employee_list = self.Employee.search([])
                    for i in employee_list:
                        if i.shift.slot == shift.slot:
                            return [False,
                                    'Employee existing in this shift. '
                                    'Please remove employees from shift before deleting']
                    shift.delete((shift,))
                    transaction.cursor.commit()
                    return [True, 'Shift deletion successful']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown error check debug']


class ShiftList():
    """
    provides a list of shifts
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Shift = pool.get('attendance.shiftdetails')

    def __init__(self):
        logger.info('Inside ShiftList')

    def load_shifts(self):
        """
        loads a list of shifts
        :return:list of dictionary consisting details of a shift
        """
        with Transaction().start(DBNAME, 1):
            shift = self.Shift.search([])
            if shift:
                lines = []
                for i in shift:
                    data = {}
                    data['slot'] = i.slot
                    data['in_time'] = i.in_time.strftime('%H:%M %p')
                    data['out_time'] = i.out_time.strftime('%H:%M %p')
                    data['monday'] = i.monday
                    data['tuesday'] = i.tuesday
                    data['wednesday'] = i.wednesday
                    data['thursday'] = i.thursday
                    data['friday'] = i.friday
                    data['saturday'] = i.saturday
                    data['sunday'] = i.sunday
                    lines.append(data)
                return lines
        return False


class SalarySettingManagement():
    """
    Provides a mechanism to manage the salary settings of a designation
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Designation = pool.get('employee.designation')
        SalarySetting = pool.get('payroll.salarysettings')

    def __init__(self, designation=None):
        logger.info('Inside SalarySettingManagement')
        self.designation = designation

    def load_setting(self):
        """
        loads the settings of a designation passed during initialization
        :return: returns a boolean False if none found or else a list of dictionary consisting of salary setting values
        """
        with Transaction().start(DBNAME, 1):
            if self.designation:
                designation = self.Designation.search(['name', '=', self.designation])
                if designation:
                    designation = designation[0]
                    salary_setting = designation.salary_setting
                    data = {}
                    data['designation'] = designation.name
                    data['da'] = Decimal(salary_setting.da_percent).to_eng_string()
                    data['hra'] = Decimal(salary_setting.hra_percent).to_eng_string()
                    data['pf'] = Decimal(salary_setting.pf_percent).to_eng_string()
                    data['esi'] = Decimal(salary_setting.esi_percent).to_eng_string()
                    data['proftax'] = Decimal(salary_setting.professional_tax_percent).to_eng_string()
                    return data
        return False

    def save_setting(self, data):
        """
        saves the salary settings of the corresponding values passed
        :param data: the dictionary of values of the salary settings
        :return:list consisting of a boolean value and the message eg:if True then the operation was successful
        """
        logger.info('SalarySettingManagement save setting initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                designation = self.Designation.search(['name', '=', data['designation']])
                if designation:
                    designation = designation[0]
                    if self.designation:
                        if self.designation != data['designation']:
                            salary_setting = self.SalarySetting(id=designation.salary_setting.id)
                            if salary_setting:
                                return [False, 'Duplicate salary setting']
                            else:
                                salary_setting = self.SalarySetting()
                        else:
                            salary_setting = designation.salary_setting
                    else:
                        if designation.salary_setting:
                            return [False, 'Duplicate salary setting']
                        else:
                            salary_setting = self.SalarySetting()
                    salary_setting.designation = (designation,)
                    salary_setting.da_percent = Decimal(data['da'])
                    salary_setting.hra_percent = Decimal(data['hra'])
                    salary_setting.pf_percent = Decimal(data['pf'])
                    salary_setting.esi_percent = Decimal(data['esi'])
                    salary_setting.professional_tax_percent = Decimal(data['proftax'])
                    try:
                        salary_setting.save()
                        transaction.cursor.commit()
                        self.designation = designation.name
                        return [True, 'The Salary Setting was saved']
                    except Exception:
                        return [False, 'The Salary Setting was not saved']
                return [False, 'The Designation not available']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown error check debug']

    def delete_setting(self):
        """
        deletes the salary settings of the designation passed in the initialization.
        :return:list consisting of a boolean value and a message
        """
        logger.info('SalarySettingManagement delete settings initated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                if self.designation:
                    designation = self.Designation.search(['name', '=', self.designation])[0]
                    salary_setting = self.SalarySetting(id=designation.salary_setting.id)
                    for i in salary_setting.designation:
                        emp_list = i.employees
                        if emp_list:
                            return [False, 'Employees Exist in the Designation, change their designation to delete']
                    salary_setting.delete((salary_setting,))
                    transaction.cursor.commit()
                    return [True, 'Salary Setting deleted successfully']
                else:
                    return [False, 'Record Not Found']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown error check debug']


class SalarySettingList():
    """
    provides a  list of salary settings
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        SalarySetting = pool.get('payroll.salarysettings')

    def __init__(self):
        logger.info('Inside SalarySettingList')

    def load_salary_setting(self):
        """
        loads the list of salary settings
        :return:list of dictionary  consisting of salary settings values
        """
        lines = []
        with Transaction().start(DBNAME, 1):
            salary_list = self.SalarySetting.search([])
            for i in salary_list:
                for j in i.designation:
                    data = {}
                    data['designation'] = j.name
                    if not i.da_percent:
                        continue
                    data['da'] = Decimal(i.da_percent).to_eng_string()
                    data['hra'] = Decimal(i.hra_percent).to_eng_string()
                    data['pf'] = Decimal(i.pf_percent).to_eng_string()
                    data['esi'] = Decimal(i.esi_percent).to_eng_string()
                    data['proftax'] = Decimal(i.professional_tax_percent).to_eng_string()
                    lines.append(data)
            return lines