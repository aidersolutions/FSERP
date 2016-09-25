#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import ldap
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pyson import Bool, Eval
from trytond.pool import Pool
from trytond.transaction import Transaction

__all__ = ['Connection', 'TestConnectionResult', 'TestConnection']


class Connection(ModelSingleton, ModelSQL, ModelView):
    "LDAP Connection"
    __name__ = 'ldap.connection'
    _rec_name = 'server'
    server = fields.Char('Server', required=True, help='LDAP server name')
    port = fields.Integer('Port', required=True, help='LDAP server port')
    secure = fields.Selection([
        ('never', 'Never'),
        ('ssl', 'SSL'),
        ('tls', 'TLS'),
        ], 'Secure', required=True,
        help='LDAP secure connection')
    bind_dn = fields.Char('Bind DN', help='LDAP DN used to bind')
    bind_pass = fields.Char('Bind Pass', states={
            'required': Bool(Eval('bind_dn')),
            'readonly': ~Eval('bind_dn'),
            }, help='LDAP password used to bind',
        depends=['bind_dn'])
    uri = fields.Function(fields.Char('URI'), 'get_uri')
    active_directory = fields.Boolean('Active Directory')

    @classmethod
    def __setup__(cls):
        super(Connection, cls).__setup__()
        cls._buttons.update({
                'test_connection': {},
                })

    @staticmethod
    def default_port():
        return 389

    @staticmethod
    def default_secure():
        return 'never'

    @staticmethod
    def default_active_directory():
        return False

    @fields.depends('secure')
    def on_change_secure(self):
        res = {}
        if self.secure in ('never', 'tls'):
            res['port'] = self.default_port()
        elif self.secure == 'ssl':
            res['port'] = 636
        return res

    def get_uri(self, name):
        return ((self.secure == 'ssl' and 'ldaps' or 'ldap') +
            '://%s:%s/' % (self.server, self.port))

    @classmethod
    @ModelView.button_action('ldap_connection.wizard_test_connection')
    def test_connection(cls, connections):
        pass

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for connections, values in zip(actions, actions):
            if 'bind_dn' in values and not values['bind_dn']:
                values = values.copy()
                values['bind_pass'] = None
            args.extend((connections, values))
        return super(Connection, cls).write(*args)


class TestConnectionResult(ModelView):
    'Test Connection'
    __name__ = 'ldap.test_connection.result'


class TestConnection(Wizard):
    "Test LDAP Connection"
    __name__ = 'ldap.test_connection'
    start_state = 'test'
    test = StateTransition()
    result = StateView('ldap.test_connection.result',
        'ldap_connection.test_connection_result_form', [
            Button('Close', 'end', 'tryton-close'),
            ])

    def transition_test(self):
        Connection = Pool().get('ldap.connection')
        connection = Connection(Transaction().context.get('active_id'))
        con = ldap.initialize(connection.uri)
        if connection.secure == 'tls':
            con.start_tls_s()
        if connection.bind_dn:
            con.simple_bind_s(connection.bind_dn, connection.bind_pass)
        else:
            con.simple_bind_s()
        return 'result'
