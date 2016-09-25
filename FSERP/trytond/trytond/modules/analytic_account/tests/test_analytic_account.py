# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
from decimal import Decimal
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.tests.test_tryton import doctest_setup, doctest_teardown
from trytond.transaction import Transaction


class AnalyticAccountTestCase(ModuleTestCase):
    'Test AnalyticAccount module'
    module = 'analytic_account'

    def setUp(self):
        super(AnalyticAccountTestCase, self).setUp()
        self.fiscalyear = POOL.get('account.fiscalyear')
        self.journal = POOL.get('account.journal')
        self.move = POOL.get('account.move')
        self.account = POOL.get('account.account')
        self.analytic_account = POOL.get('analytic_account.account')
        self.party = POOL.get('party.party')

    def test0010account_debit_credit(self):
        'Test account debit/credit'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            party = self.party(name='Party')
            party.save()
            root, = self.analytic_account.create([{
                        'type': 'root',
                        'name': 'Root',
                        }])
            analytic_account, = self.analytic_account.create([{
                        'type': 'normal',
                        'name': 'Analytic Account',
                        'parent': root.id,
                        'root': root.id,
                        }])
            fiscalyear, = self.fiscalyear.search([])
            period = fiscalyear.periods[0]
            journal_revenue, = self.journal.search([
                    ('code', '=', 'REV'),
                    ])
            journal_expense, = self.journal.search([
                    ('code', '=', 'EXP'),
                    ])
            revenue, = self.account.search([
                    ('kind', '=', 'revenue'),
                    ])
            receivable, = self.account.search([
                    ('kind', '=', 'receivable'),
                    ])
            expense, = self.account.search([
                    ('kind', '=', 'expense'),
                    ])
            payable, = self.account.search([
                    ('kind', '=', 'payable'),
                    ])

            first_account_line = {
                'account': revenue.id,
                'credit': Decimal(100),
                'analytic_lines': [
                    ('create', [{
                                'account': analytic_account.id,
                                'name': 'Analytic Line',
                                'credit': Decimal(100),
                                'debit': Decimal(0),
                                'journal': journal_revenue.id,
                                'date': period.start_date,
                                }])
                    ]}
            second_account_line = {
                'account': expense.id,
                'debit': Decimal(30),
                'analytic_lines': [
                    ('create', [{
                                'account': analytic_account.id,
                                'name': 'Analytic Line',
                                'debit': Decimal(30),
                                'credit': Decimal(0),
                                'journal': journal_expense.id,
                                'date': period.start_date,
                                }])
                    ]}
            # Create some moves
            vlist = [{
                    'period': period.id,
                    'journal': journal_revenue.id,
                    'date': period.start_date,
                    'lines': [
                        ('create', [first_account_line, {
                                    'account': receivable.id,
                                    'debit': Decimal(100),
                                    'party': party.id,
                                    }]),
                        ],
                    }, {
                    'period': period.id,
                    'journal': journal_expense.id,
                    'date': period.start_date,
                    'lines': [
                        ('create', [second_account_line, {
                                    'account': payable.id,
                                    'credit': Decimal(30),
                                    'party': party.id,
                                    }]),
                        ],
                    },
                ]
            self.move.create(vlist)

            self.assertEqual((analytic_account.debit, analytic_account.credit),
                (Decimal(30), Decimal(100)))
            self.assertEqual(analytic_account.balance, Decimal(70))

            with transaction.set_context(start_date=period.end_date):
                analytic_account = self.analytic_account(analytic_account.id)
                self.assertEqual((analytic_account.debit,
                        analytic_account.credit),
                    (Decimal(0), Decimal(0)))
                self.assertEqual(analytic_account.balance, Decimal(0))

            with transaction.set_context(end_date=period.end_date):
                analytic_account = self.analytic_account(analytic_account.id)
                self.assertEqual((analytic_account.debit,
                        analytic_account.credit),
                    (Decimal(30), Decimal(100)))
                self.assertEqual(analytic_account.balance, Decimal(70))


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.account.tests import test_account
    for test in test_account.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AnalyticAccountTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_analytic_account.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
