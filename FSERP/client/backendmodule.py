# This module is part of FSERP
# Copyright 2015 Aider Solutions Pvt. Ltd.

"""
This module is direct way to access tryton modules
"""

import trytond
from trytond.config import config, parse_listen
import logging
import logging.config
import logging.handlers
# from trytond.ir.module import Module

from tryton import backend
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
from FSERP import client

logger = logging.getLogger(__name__)


class BackendModule:
    """ Billing Backend """

    __tryton_module_name__ = " "
    tryton_module = None


    @classmethod
    def initialize(cls):
        with Transaction().start(dbname, 0) as transaction:
            user_obj = client.pool.get('res.user')
            user = user_obj.search([('login', '=', 'admin')], limit=1)[0]
            user_id = user.id

        with Transaction().start(dbname, user_id) as transaction:
            try:
                cls.tryton_module = client.pool.get(cls.__tryton_module_name__)
            except:
                logger.error("module not found")

    @classmethod
    def create(cls, ):
        pass

    @classmethod
    def update(cls, ):
        pass

    @classmethod
    def delete(cls, records):

    # super(back
    pass

    @classmethod
    def get(cls, ):
        pass

    @classmethod
    def Search(cls, ):
        pass
	
