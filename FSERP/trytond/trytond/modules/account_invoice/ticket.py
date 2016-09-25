from trytond.model import ModelView, ModelSQL, fields

__all__ = [ 'Ticket','TicketLines' ]


class Ticket( ModelSQL, ModelView ):
    """
        Ticket
    """
    __name__ = 'account.ticket'
    table_no = fields.Integer('table_no')
    ticket_no = fields.Integer('ticket_no')
    lines = fields.One2Many('account.ticket.lines','ticket','Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ], 'State', readonly=True, select=True)
    invoice = fields.Many2One('account.invoice','Invoice', ondelete='CASCADE')

    @staticmethod
    def default_state():
        return 'draft'

class TicketLines( ModelSQL, ModelView ):
    """
        TicketLines
    """
    __name__ = 'account.ticket.lines'
    product = fields.Many2One('product.product','Product')
    ticket = fields.Many2One('account.ticket','Ticket', ondelete='CASCADE')
    quantity = fields.Integer('quantity')
    state = fields.Selection([
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ('rejected','Rejected'),
        ],'State', readonly=True, select=True)
    remark = fields.Selection([
        ('normal','Normal'),
        ('excess','Excess'),
        ('malicious','Malicious'),
        ],'Remark', readonly=True, select=True)
    excess_quantity = fields.Integer('excess_quantity')

    @staticmethod
    def default_state():
        return 'processing'

    @staticmethod
    def default_remark():
        return 'normal'
