from trytond.model import ModelView, ModelSQL, fields

__all__ = [ 'Messages']


class Messages( ModelSQL, ModelView ):
    """
        Messages
    """
    __name__ = 'health_and_hygiene.messages'
    message_id=fields.Integer('Message Id')
    sent = fields.Date('Sent Date')
    from_name=fields.Char('From Name')
    from_designation=fields.Char('From Designation')
    from_address=fields.Char('From Address')
    message_type=fields.Char('Message Type')
    message_body=fields.Text('Message Body')
    message_state= fields.Selection([
        ('new', 'New'),
        ('to do','To do'),
        ('done','Done'),
    ], 'Message State')
    
    @staticmethod
    def default_message_state():
        return 'new'
