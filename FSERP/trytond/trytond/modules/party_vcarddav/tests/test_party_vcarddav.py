# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class PartyVCardDAVTestCase(ModuleTestCase):
    'Test PartyVCardDAV module'
    module = 'party_vcarddav'

    def test0010party_vcard_report(self):
        'Test Party VCARD report'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            Party = POOL.get('party.party')
            VCardReport = POOL.get('party_vcarddav.party.vcard', type='report')

            party1, = Party.create([{
                        'name': 'Party 1',
                        }])
            oext, content, _, _ = VCardReport.execute([party1.id], {})
            self.assertEqual(oext, 'vcf')
            self.assertIn('FN:Party 1', str(content))


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyVCardDAVTestCase))
    return suite
