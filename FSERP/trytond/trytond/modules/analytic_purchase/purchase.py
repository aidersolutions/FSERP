# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

from trytond.modules.analytic_account import AnalyticMixin

__all__ = ['Purchase', 'PurchaseLine', 'AnalyticAccountEntry']
__metaclass__ = PoolMeta


class Purchase:
    __name__ = "purchase.purchase"

    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()
        cls._error_messages.update({
                'analytic_account_required': ('Analytic account is required '
                    'for "%(roots)s" on line "%(line)s".'),
                })

    def check_for_quotation(self):
        pool = Pool()
        Account = pool.get('analytic_account.account')
        mandatory_roots = {a for a in Account.search([
                ('type', '=', 'root'),
                ('mandatory', '=', True),
                ])}

        super(Purchase, self).check_for_quotation()

        for line in self.lines:
            if line.type != 'line':
                continue
            analytic_roots = {e.root for e in line.analytic_accounts
                if e.account}
            if not mandatory_roots <= analytic_roots:
                self.raise_user_error('analytic_account_required', {
                        'line': line.rec_name,
                        'roots': ', '.join(x.rec_name
                            for x in mandatory_roots - analytic_roots),
                        })


class PurchaseLine(AnalyticMixin):
    __name__ = 'purchase.line'

    def get_invoice_line(self, invoice_type):
        pool = Pool()
        AnalyticAccountEntry = pool.get('analytic.account.entry')

        invoice_lines = super(PurchaseLine, self).get_invoice_line(
            invoice_type)
        for invoice_line in invoice_lines:
            new_entries = AnalyticAccountEntry.copy(self.analytic_accounts,
                default={
                    'origin': None,
                    })
            invoice_line.analytic_accounts = new_entries
        return invoice_lines


class AnalyticAccountEntry:
    __name__ = 'analytic.account.entry'

    @classmethod
    def _get_origin(cls):
        origins = super(AnalyticAccountEntry, cls)._get_origin()
        return origins + ['purchase.line']

    @fields.depends('origin')
    def on_change_with_required(self, name=None):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')
        required = super(AnalyticAccountEntry, self).on_change_with_required(
            name)
        if (self.origin and isinstance(self.origin, PurchaseLine)
                and self.origin.purchase.state in ['cancel', 'draft']):
            return False
        return required
