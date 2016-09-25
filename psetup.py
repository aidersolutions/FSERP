#unsued files
import FSERP
import os

from proteus import Model, config

conf = config.set_trytond('testdbkitchen', user='admin',
                          config_file=os.path.join(os.getcwd(), 'FSERP', 'trytond', 'etc', 'trytond.conf'))

Employee = Model.get('company.employee')
Company = Model.get('company.company')
Department = Model.get('department.department')
Designation = Model.get('employee.designation')
SalarySettings = Model.get('payroll.salarysettings')
Salary = Model.get('payroll.salary')
Days = Model.get('attendance.days')
ShiftDetails = Model.get('attendance.shiftdetails')
Attendance = Model.get('attendance.attendance')
Payroll = Model.get('payroll.payroll')
Water = Model.get('health_and_hygiene.water_control_test')
Pest = Model.get('health_and_hygiene.pest_control_test')
HealtReport = Model.get('health_and_hygiene.health_report')


# %run psetup.py
# from employee_tryton import PayrollManagement
# from datetime import datetime,timedelta
# payroll=PayrollManagement()
# today=datetime.today()+timedelta(days=1)
# previous=today-timedelta(days=10)
# data=payroll.create_payroll('monthly',previous,today)
#
#
# e=Employee.find()[0]
# s=Salary()
# from decimal import Decimal
# s.basic_pay=Decimal(3000)
# set=SalarySettings.find()[0]
# s.salary_settings=set
# s.period='monthly'
# s.save()
# e.salary=s
# e.save()
# s=Salary()
# s.basic_pay=Decimal(4500)
# s.salary_settings=set
# s.period='monthly'
# s.save()
# e=Employee.find()[1]
# e.salary=s
# e.save()

# %run psetup.py
# %run test_tansactions.py
# import settings
# settings.level=10
# from inventory_tryton import BusinessParty
# party=BusinessParty('Customer')
# data={}
# data['pan']='102'
# data['name']='Jitesh'
# data['street']='Kochi'
# data['city']='kerala'
# data['zip']='400706'
# party.create_supplier(data)
# Party=Model.get('party.party')
# party.get_supplier('102')
