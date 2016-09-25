from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.backend.database import CursorInterface

__all__ = [ 'Employee', 'Designation']
genders =   [   ('female', 'Female'),
                ('male', 'Male'),
                ('other', 'Other'), 
            ]

class Designation(ModelSQL, ModelView):
    """
        Employee Designation
    """
    __name__ = 'employee.designation'
    name = fields.Char('Name')
    code = fields.Integer('Code')
    employees = fields.One2Many('company.employee', 'designation', 'Employees' ) 
    salary_setting = fields.Many2One('payroll.salarysettings','Salary Settings')

class Employee( ModelSQL, ModelView ):
    """
        Employee
    """
    __name__ = 'company.employee'
    employee_id = fields.Integer('Employee ID', required=True )
    department = fields.Many2One('department.department', "Department", required = True)
    designation = fields.Many2One('employee.designation', "Designation", required = True)
    name = fields.Char('Name', size=None, translate=True, select=True, required = True)
    surname = fields.Char('Name', size=None, translate=True, select=True, required = False)
    fathersname = fields.Char('Name', size=None, translate=True, select=True, required = False)
    gender = fields.Selection(genders, 'Gender', required=True )
    dob = fields.Date('DOB', required=True)
    doj = fields.Date('DOJ', required=True)
    pan = fields.Char('PAN', required=False)
    adhar = fields.Char('Adhaar Number', required=False)
    salary = fields.Many2One('payroll.salary', 'Salary')
    shift = fields.Many2One('attendance.shiftdetails','Shift')

    
