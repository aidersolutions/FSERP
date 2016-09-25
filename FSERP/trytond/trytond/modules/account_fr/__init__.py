# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from account import *


def register():
    Pool.register(
        TaxTemplate,
        TaxRuleTemplate,
        module='account_fr', type_='model')
