from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.backend.database import CursorInterface

__all__ = ['Department']
class Department( ModelSQL, ModelView ):
    """
        Department
    """
    __name__ = 'department.department'
    company = fields.Many2One('company.company', 'Company', required = True)
    name = fields.Char('Name', size=None, required=True, translate=True, select=True)
    department_id = fields.Integer('Department ID', required=True )
    employees = fields.One2Many('company.employee', 'department', 'Employees', required = False)
    
