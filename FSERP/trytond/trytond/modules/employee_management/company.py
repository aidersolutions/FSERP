from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.backend.database import CursorInterface

__all__ = ['Company']
class Company( ModelSQL, ModelView ):
    """
        Employee
    """
    __name__ = 'company.company'
    departments=fields.One2Many('department.department', 'company', 'Departments', required = False)
