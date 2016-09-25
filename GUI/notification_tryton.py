#! /usr/bin/env python

""" Billing module backend"""
import sys

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from proteus import Model, Wizard, config
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
from cdecimal import Decimal

from datetime import datetime, timedelta, date
import logging
from GUI import settings


logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class Messaging():
    """
    provides a mechanism to manage messages
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Messages = pool.get('health_and_hygiene.messages')

    def __init__(self):
        logger.info('Inside notification_tryton')

    def load_message(self, msg_id=None, limit=None, from_date=None, to_date=None, msg_state=None, offset=0):
        """lodas messages from the backend"""
        return_list = []
        limit = int(limit) if limit else 0
        from_date = datetime.strptime(from_date, '%d/%m/%Y') if from_date else None
        to_date = datetime.strptime(to_date, '%d/%m/%Y') + timedelta(hours=23, minutes=59,
                                                                     seconds=59) if to_date else None
        try:
            with Transaction().start(DBNAME, 1):
                if msg_id:
                    message_list = self.Messages.search([('message_id', '=', msg_id)])
                elif msg_state == 'All':
                    message_list = self.Messages.search([('create_date', '>=', from_date),
                                                         ('create_date', '<=', to_date)]
                                                        , offset=offset, limit=limit)
                else:
                    message_list = self.Messages.search([('create_date', '>=', from_date),
                                                         ('create_date', '<=', to_date),
                                                         ('message_state', '=', msg_state.lower())]
                                                        , offset=offset, limit=limit)
                for i in message_list:
                    dictionary = {}
                    dictionary['msg_id'] = str(i.message_id)
                    dictionary['date'] = i.sent.strftime("%d/%m/%Y") if i.sent else ''
                    dictionary['name'] = i.from_name
                    dictionary['designation'] = i.from_designation
                    dictionary['address'] = i.from_address
                    dictionary['msg_type'] = i.message_type
                    dictionary['msg_body'] = i.message_body
                    dictionary['msg_state'] = i.message_state
                    return_list.append(dictionary)
                return return_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return return_list

    def save_message(self, data):
        """method to save the messages to the backend"""
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                for i in data:
                    message_list = self.Messages.search([('message_id', '=', i['message_id'])])
                    if message_list:
                        continue
                    else:
                        message = self.Messages()
                        message.message_id = i['message_id']
                        message.sent = datetime.strptime(i['sent'], "%d/%m/%Y")
                        message.from_name = i['name']
                        message.from_designation = i['from_designation']
                        message.from_address = i['from_address']
                        message.message_type = i['msg_type']
                        message.message_body = i['msg_body']
                        message.save()
                transaction.cursor.commit()
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def update_message(self, data):
        """updats the message details"""
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                message_list = self.Messages.search([('message_id', '=', data['message_id'])])
                if message_list:
                    message, = message_list
                    message.message_state = data['msg_state'].lower()
                    message.save()
                transaction.cursor.commit()
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False