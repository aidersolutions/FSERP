from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.backend.database import CursorInterface
from trytond.pyson import Eval, Bool

__all__ = ['Days', 'ShiftDetails', 'Attendance']
class Days(ModelSQL, ModelView):
    """
        Days
    """
    __name__ = 'attendance.days'
    name = fields.Char('Name')
    short_name = fields.Char('Short Name')

class ShiftDetails(ModelSQL, ModelView):
    """
        Shift Details
    """
    __name__ = 'attendance.shiftdetails'
    slot = fields.Char('Slot')
    in_time = fields.Time('In Time')
    out_time = fields.Time('Out Time')
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')
    no_days = fields.Function(fields.Integer('Number of days per week'), 'get_no_of_days')
    
    def get_no_of_days(self, name):
        return (self.monday + self.tuesday + self.wednesday + self.thursday + self.friday + self.saturday + self.sunday)
class Attendance( ModelSQL, ModelView ):
    """
        Attendance
    """
    __name__ = 'attendance.attendance'
    employee = fields.Many2One('company.employee','Employee')
    shift = fields.Many2One('attendance.shiftdetails', 'Shift')
    date = fields.Date('Date')
    in_time = fields.Time('In Time')
    out_time = fields.Time('Out Time')
    is_holiday = fields.Boolean('Is Holiday')
    is_absent = fields.Function(fields.Boolean('Is Absent'),'get_is_absent')
    leave_applied = fields.Boolean('Leave Applied')
    leave_reason = fields.Char('Leave Reason')
    leave_type = fields.Selection([
        ('none', 'None'),
        ('cl','Casual Leave'),
        ('lop','Loss of Pay'),
        ('compoff','Compansatory Off'),
    ], 'Type of Leave')
    
    """leave_session = fields.Selection([
        ('none','None'),
        ('first', 'First Session'),
        ('second','Second Session'),
        ('full','Full Session'),
    ])"""
    payroll_leaves = fields.Many2One('payroll.payroll','Payroll')
    def get_is_absent(self, name):
        return (not self.is_holiday) and (not self.in_time)
