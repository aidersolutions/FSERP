#! /usr/bin/env python

""" Creatas a fiscal year entry """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

import datetime

from dateutil.relativedelta import relativedelta

from proteus import Model


def create_fiscalyear(company=None, today=None, config=None):
    """Create a fiscal year for the company on today"""
    FiscalYear = Model.get('account.fiscalyear', config=config)
    Sequence = Model.get('ir.sequence', config=config)
    CustomerSequence = Model.get('ir.sequence.strict', config=config)
    if not today:
        today = datetime.date.today()

    fiscalyear = FiscalYear(name=str(today.year))
    fiscalyear.start_date = today + relativedelta(month=1, day=1)
    fiscalyear.end_date = today + relativedelta(month=12, day=31)
    fiscalyear.company = company

    post_move_sequence = Sequence(name=str(today.year), code='account.move',
                                  company=company)
    post_move_sequence.save()
    fiscalyear.post_move_sequence = post_move_sequence

    customer_sequnce = CustomerSequence(name=str(today.year), code='account.invoice',
                                        company=company)
    customer_sequnce.save()
    fiscalyear.out_invoice_sequence = customer_sequnce
    fiscalyear.in_invoice_sequence = customer_sequnce
    fiscalyear.out_credit_note_sequence = customer_sequnce
    fiscalyear.in_credit_note_sequence = customer_sequnce
    fiscalyear.save()
    fiscalyear.click('create_period')

    return fiscalyear
