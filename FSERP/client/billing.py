# This module is part of FSERP
# Copyright 2015 Aider Solutions Pvt. Ltd.
"""
This module is direct way to access tryton modules
"""

from client.backendmodule import BackendModule


class Billing(BackendModule):
    """ Billing Backend
        Call intialize classmethod. (defined in BackendModule)
    """

    __tryton_module_name__ = "account.invoice"


    @classmethod
    def create(cls, *args, **kwargs):

        if (bill = cls.tryton_module(args, kwargs)):
            return bill
        else:
            return None

    @classmethod
    def update(cls, *args, **kwargs):
        pass

    @classmethod
    def delete(cls, ):


    @classmethod
    def get(cls, ):
        pass

    @classmethod
    def Search(cls, ):
        pass
	
