#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .connection import *


def register():
    Pool.register(
        Connection,
        TestConnectionResult,
        module='ldap_connection', type_='model')
    Pool.register(
        TestConnection,
        module='ldap_connection', type_='wizard')
