from trytond.pool import Pool

from .company import *
from .department import *
from .employee import *
from .attendance import *
from .payroll import *


def register():
    Pool.register(
        Company,
        SalarySettings,
        Department,
        Designation,
        Salary,
        ShiftDetails, 
        Attendance,
        Employee,
        Days, 
        Payroll,
        module='employee_management', type_='model')

