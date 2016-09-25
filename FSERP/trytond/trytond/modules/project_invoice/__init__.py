# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .work import *
from .timesheet import *


def register():
    Pool.register(
        Work,
        TimesheetLine,
        module='project_invoice', type_='model')
    Pool.register(
        OpenInvoice,
        module='project_invoice', type_='wizard')
