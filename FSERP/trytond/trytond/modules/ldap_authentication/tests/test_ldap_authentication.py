# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest

from mock import patch
import ldap

import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction
from trytond.config import config

from trytond.modules.ldap_authentication.res import parse_ldap_url

section = 'ldap_authentication'


class LDAPAuthenticationTestCase(ModuleTestCase):
    'Test LDAPAuthentication module'
    module = 'ldap_authentication'

    def setUp(self):
        super(LDAPAuthenticationTestCase, self).setUp()
        config.add_section(section)
        config.set(section, 'uri', 'ldap://localhost/dc=tryton,dc=org')

    def tearDown(self):
        config.remove_section(section)

    def test_user_get_login(self):
        'Test User.get_login'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            User = POOL.get('res.user')

            @patch.object(ldap, 'initialize')
            @patch.object(User, 'ldap_search_user')
            def get_login(login, password, find, ldap_search_user, initialize):
                con = initialize.return_value
                con.simple_bind_s.return_value = True
                if find:
                    ldap_search_user.return_value = [('dn', {'uid': [find]})]
                else:
                    ldap_search_user.return_value = None
                return User.get_login(login, password)

            # Test existing user
            self.assertEqual(get_login('admin', 'admin', None), USER)
            self.assertEqual(get_login('admin', 'admin', 'admin'), USER)
            self.assertEqual(get_login('AdMiN', 'admin', 'admin'), USER)

            # Test new user
            self.assertFalse(get_login('foo', 'bar', None))
            self.assertFalse(get_login('foo', 'bar', 'foo'))

            # Test create new user
            config.set(section, 'create_user', 'True')
            user_id = get_login('foo', 'bar', 'foo')
            foo, = User.search([('login', '=', 'foo')])
            self.assertEqual(user_id, foo.id)
            self.assertEqual(foo.name, 'foo')

            # Test create new user with different case
            user_id = get_login('BaR', 'foo', 'bar')
            bar, = User.search([('login', '=', 'bar')])
            self.assertEqual(user_id, bar.id)
            self.assertEqual(bar.name, 'bar')

    def test_parse_ldap_url(self):
        'Test parse_ldap_url'
        self.assertEqual(
            parse_ldap_url('ldap:///o=University%20of%20Michigan,c=US')[1],
            'o=University of Michigan,c=US')
        self.assertEqual(
            parse_ldap_url(
                'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,c=US'
                )[1],
            'o=University of Michigan,c=US')
        self.assertEqual(
            parse_ldap_url(
                'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,'
                'c=US?postalAddress')[2],
            'postalAddress')
        self.assertEqual(
            parse_ldap_url(
                'ldap://host.com:6666/o=University%20of%20Michigan,'
                'c=US??sub?(cn=Babs%20Jensen)')[3:5],
            ('sub', '(cn=Babs Jensen)'))
        self.assertEqual(
            parse_ldap_url(
                'ldap:///??sub??bindname=cn=Manager%2co=Foo')[5],
            {'bindname': ['cn=Manager,o=Foo']})
        self.assertEqual(
            parse_ldap_url(
                'ldap:///??sub??!bindname=cn=Manager%2co=Foo')[5],
            {'!bindname': ['cn=Manager,o=Foo']})


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        LDAPAuthenticationTestCase))
    return suite
