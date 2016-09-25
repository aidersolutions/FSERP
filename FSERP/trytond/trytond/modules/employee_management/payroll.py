from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.backend.database import CursorInterface
from decimal import Decimal

__all__ = ['SalarySettings', 'Salary', 'Payroll']

months = [('1', 'January'),
          ('2', 'February'),
          ('3', 'March'),
          ('4', 'April'),
          ('5', 'May'),
          ('6', 'June'),
          ('7', 'July'),
          ('8', 'August'),
          ('9', 'September'),
          ('10', 'October'),
          ('11', 'November'),
          ('12', 'December'),
          ]


class SalarySettings(ModelSQL, ModelView):
    """
    Salary Settings
    """
    __name__ = 'payroll.salarysettings'
    da_percent = fields.Numeric('DA Rate', digits=(14, 10))
    hra_percent = fields.Numeric('HRA Rate', digits=(14, 10))
    pf_percent = fields.Numeric('PF Rate', digits=(14, 10))
    esi_percent = fields.Numeric('ESI Rate', digits=(14, 10))
    professional_tax_percent = fields.Numeric('Rate', digits=(14, 10))
    designation = fields.One2Many('employee.designation', 'salary_setting', 'Designation')


class Salary(ModelSQL, ModelView):
    """
        Salary
    """
    __name__ = 'payroll.salary'
    salary_settings = fields.Many2One('payroll.salarysettings', 'Salary Settings', required=True)
    basic_pay = fields.Numeric('Basic Pay', digits=(16, 10), required=True)
    da = fields.Function(fields.Numeric('DA', digits=(16, 10)), 'get_da')
    hra = fields.Function(fields.Numeric('HRA', digits=(16, 10)), 'get_hra')
    pf = fields.Function(fields.Numeric('PF', digits=(16, 10)), 'get_pf')
    esi = fields.Function(fields.Numeric('ESI', digits=(16, 10)), 'get_esi')
    professional_tax = fields.Function(fields.Numeric('Professoional Tax', digits=(16, 10)), 'get_professional_tax')
    period = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], 'Period')
    per_day = fields.Function(fields.Numeric('Per Day Pay', digits=(16, 10)), 'get_per_day')
    gross_pay = fields.Function(fields.Numeric('Gross Pay', digits=(16, 10)), 'get_gross_pay')
    net_pay = fields.Function(fields.Numeric('Net Pay', digits=(16, 10)), 'get_net_pay')

    def get_da(self, name):
        return Decimal(self.basic_pay * self.salary_settings.da_percent) / Decimal(100.0)

    def get_hra(self, name):
        return Decimal(self.basic_pay * self.salary_settings.hra_percent) / Decimal(100.0)

    def get_pf(self, name):
        return Decimal(self.basic_pay * self.salary_settings.pf_percent) / Decimal(100.0)

    def get_esi(self, name):
        return Decimal(self.basic_pay * self.salary_settings.esi_percent) / Decimal(100.0)

    def get_professional_tax(self, name):
        return Decimal(self.basic_pay * self.salary_settings.professional_tax_percent) / Decimal(100.0)

    def get_per_day(self, name):
        if self.period == 'daily':
            per_day = self.basic_pay
        elif self.period == 'weekly':
            per_day = Decimal(self.basic_pay) / Decimal(6)
        else:
            per_day = Decimal(self.gross_pay) / Decimal(30)
        return per_day

    def get_gross_pay(self, name):
        if self.period == 'monthly':
            return self.basic_pay + self.da + self.hra
        else:
            return self.basic_pay

    def get_net_per_day(self):
        if self.period == 'daily':
            per_day = self.basic_pay
        elif self.period == 'weekly':
            per_day = Decimal(self.basic_pay) / Decimal(6)
        else:
            per_day = Decimal(self.net_pay) / Decimal(30)
        return per_day

    def get_net_pay(self, name):
        if self.period == 'monthly':
            return self.gross_pay - self.professional_tax - self.pf - self.esi
        else:
            return self.gross_pay


class Payroll(Salary):
    """
        PayRoll
    """
    __name__ = 'payroll.payroll'
    date_of_payement = fields.Date('Date of Payement')
    from_date = fields.Date('From')
    to_date = fields.Date('To')
    month = fields.Selection(months, 'Month')
    employee = fields.Many2One('company.employee', 'Employee')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
    ], 'Status')
    total_days = fields.Function(fields.Numeric('Days', digits=(16, 10)), 'get_days')
    other_deductions = fields.Numeric('Deductions', digits=(16, 10))
    leaves = fields.Function(fields.One2Many('attendance.attendance', 'payroll_leaves', 'Leaves'),
                             'get_leaves')  ### instead payroll_leaves it may be none because every other previous tryton module follows this step. needs more work on this
    leave_deduction = fields.Function(fields.Numeric('Leave Deduciton', digits=(16, 10)), 'get_leave_deduction')
    gross_pay4duration = fields.Function(fields.Numeric('Gross Pay'), 'get_gross_pay4duration')
    net_pay4duration = fields.Function(fields.Numeric('Net Pay'), 'get_net_pay4duration')

    def get_leave_deduction(self, name):
        return self.get_net_per_day() * Decimal(
            len([l for l in self.get_leaves('leaves') if l.leave_type == 'lop']))  ####hack not using self.leaves

    def get_leaves(self, name):
        Attendance = Pool().get('attendance.attendance')
        days = Attendance.search([
            ('employee', '=', self.employee.id),
            ('date', '>', self.from_date ),
            ('date', '<', self.to_date ),
        ])
        leave_list = []
        for i in days:
            if i.is_absent == True:
                leave_list.append(i)
        return leave_list

    def get_days(self, name):
        Attendance = Pool().get('attendance.attendance')
        days = Attendance.search([
            ('employee', '=', self.employee.id),
            ('date', '>', self.from_date ),
            ('date', '<', self.to_date ),
        ])
        return len(days)

    def get_gross_pay4duration(self, name):
        return self.per_day * Decimal(self.total_days)

    def get_net_4duration(self):
        return self.get_net_per_day() * Decimal(self.total_days)

    def get_net_pay4duration(self, name):
        if self.period == 'monthly':
            return self.get_net_4duration() - self.leave_deduction - self.other_deductions
        else:
            return self.gross_pay4duration - self.leave_deduction - self.other_deductions
