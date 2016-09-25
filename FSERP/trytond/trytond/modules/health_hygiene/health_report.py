from trytond.model import ModelView, ModelSQL, fields

__all__ = [ 'HealthReport' ]


class HealthReport( ModelSQL, ModelView ):
    """
        HealthReport
    """
    __name__ = 'health_and_hygiene.health_report'
    employee = fields.Many2One('company.employee','Employee')
    date = fields.Date('Test Date')
    test = fields.Char('Test Name')
    code=fields.Integer('code')
    organization = fields.Char('Organization')
    description=fields.Text('Description')
    report=fields.Binary('Pest Test Report')
