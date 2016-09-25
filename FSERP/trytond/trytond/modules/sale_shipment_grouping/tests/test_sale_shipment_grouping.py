# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class SaleShipmentGroupingTestCase(ModuleTestCase):
    'Test Sale module'
    module = 'sale_shipment_grouping'


def suite():
    suite = trytond.tests.test_tryton.suite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(SaleShipmentGroupingTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_sale_shipment_grouping.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
