from trytond.model import ModelView, ModelSQL, fields

__all__ = [ 'PestControlTest','WaterControlTest' ]


class PestControlTest( ModelSQL, ModelView ):
    """
        PestControlTest
    """
    __name__ = 'health_and_hygiene.pest_control_test'
    code=fields.Integer('code')
    organization = fields.Char('Organization')
    date = fields.Date('Test Date')
    test = fields.Char('Test Name')
    description=fields.Text('Description')
    report=fields.Binary('Pest Test Report')


class WaterControlTest( ModelSQL, ModelView ):
    """
        WaterControlTest
    """
    __name__ = 'health_and_hygiene.water_control_test'
    code=fields.Integer('code')
    organization = fields.Char('Organization')
    date = fields.Date('Test Date')
    test = fields.Char('Test Name')
    description=fields.Text('Description')
    report=fields.Binary('Water Test Report')
