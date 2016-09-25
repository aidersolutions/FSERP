#! /usr/bin/env python

""" Report Module backend """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction

from decimal import Decimal
import logging
from GUI import settings
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class Pest():
    """
    Manages the Pest Reports
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Pest = pool.get('health_and_hygiene.pest_control_test')

    def __init__(self):
        logger.info('Inside WasteMenu')

    def load_report(self):
        """
        loads the pest reports
        :return:True/False and list of dictionaries/string
        """
        try:
            with Transaction().start(DBNAME, 1):
                pest_list = self.Pest.search([])
                data_list = []
                for pest in pest_list:
                    data = {}
                    data['code'] = str(pest.code)
                    data['organization'] = pest.organization
                    data['date'] = pest.date.strftime("%d/%m/%Y")
                    data['test'] = pest.test
                    data['description'] = pest.description
                    # data['report'] = pest.report
                    data_list.append(data)
                return True, data_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def create_report(self, data):
        """
        creates a pest report
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                pest_list = self.Pest.search(['code', '=', Decimal(data['code'])])
                if not pest_list:
                    pest = self.Pest()
                    pest.code = data['code']
                    pest.organization = data['organization']
                    pest.date = datetime.strptime(data['date'], '%d/%m/%Y')
                    pest.test = data['test']
                    pest.description = data['description']
                    pest.report = data['report']
                    pest.save()
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
                else:
                    return False, 'Duplicate Code'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def update_report(self, data):
        """
        updates a pest report
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                pest_list = self.Pest.search(['code', '=', Decimal(data['code'])])
                if pest_list:
                    pest, = pest_list
                    pest.organization = data['organization']
                    pest.date = datetime.strptime(data['date'], '%d/%m/%Y')
                    pest.test = data['test']
                    pest.description = data['description']
                    pest.report = data['report']
                    pest.save()
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def read_report(self, code):
        """
        reads pest reports
        :return:True/False and dictionary/string
        """
        try:
            with Transaction().start(DBNAME, 1):
                pest_list = self.Pest.search(['code', '=', Decimal(code)])
                if pest_list:
                    pest, = pest_list
                    data = {}
                    data['code'] = str(pest.code)
                    data['organization'] = pest.organization
                    data['date'] = pest.date
                    data['test'] = pest.test
                    data['description'] = pest.description
                    data['report'] = pest.report
                    return True, data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def delete_report(self, code):
        """
        deletes pest reports
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                pest_list = self.Pest.search(['code', '=', Decimal(code)])
                if pest_list:
                    pest, = pest_list
                    pest.delete((pest,))
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'


class Water(Pest):
    """
    Manages the Water Reports
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Water = pool.get('health_and_hygiene.water_control_test')
        Pest = Water


class Health():
    """
    Manages the Health Reports
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Health = pool.get('health_and_hygiene.health_report')
        Employee = pool.get('company.employee')

    def __init__(self, emp_id):
        logger.info('Inside WasteMenu')
        self.setup(emp_id=emp_id)

    def setup(self, emp_id):
        """
        Retrives the DB-id for the employee
        :param emp_id:the employee id
        """
        try:
            with Transaction().start(DBNAME, 1):
                employee = self.Employee.search(['employee_id', '=', emp_id])
                if employee:
                    self.emp_id = employee[0].id
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def load_report(self):
        """
        loads the employee health reports
        :return:boolean and list of dictionary
        """
        try:
            with Transaction().start(DBNAME, 1):
                report_list = self.Health.search(['employee', '=', self.emp_id])
                data_list = []
                for report in report_list:
                    data = {}
                    data['code'] = str(report.code)
                    data['organization'] = report.organization
                    data['date'] = report.date.strftime("%d/%m/%Y")
                    data['test'] = report.test
                    data['description'] = report.description
                    data_list.append(data)
                return True, data_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def create_report(self, data):
        """
        creates a health test report
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                report_list = self.Health.search([('code', '=', Decimal(data['code'])),
                                                  ('employee', '=', self.emp_id)])
                if not report_list:
                    health = self.Health()
                    health.code = data['code']
                    health.organization = data['organization']
                    health.date = datetime.strptime(data['date'], '%d/%m/%Y')
                    health.test = data['test']
                    health.description = data['description']
                    health.report = data['report']
                    health.employee = self.emp_id
                    health.save()
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
                else:
                    return False, 'Duplicate Entry'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def update_report(self, data):
        """
        updates a health test report
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                heatlth_list = self.Health.search([('code', '=', Decimal(data['code'])),
                                                   ('employee', '=', self.emp_id)])
                if heatlth_list:
                    health, = heatlth_list
                    health.organization = data['organization']
                    health.date = datetime.strptime(data['date'], '%d/%m/%Y')
                    health.test = data['test']
                    health.description = data['description']
                    health.report = data['report']
                    health.save()
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def read_report(self, code):
        """
        reads health reports
        :return:True/False and dictionary/string
        """
        try:
            with Transaction().start(DBNAME, 1):
                health_list = self.Health.search([('code', '=', Decimal(code)),
                                                  ('employee', '=', self.emp_id)])
                if health_list:
                    health, = health_list
                    data = {}
                    data['code'] = str(health.code)
                    data['organization'] = health.organization
                    data['date'] = health.date
                    data['test'] = health.test
                    data['description'] = health.description
                    data['report'] = health.report
                    return True, data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def delete_report(self, code):
        """
        deletes health reports
        :return:True/False and string
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                health_list = self.Health.search([('code', '=', Decimal(code)),
                                                  ('employee', '=', self.emp_id)])
                if health_list:
                    pest, = health_list
                    pest.delete((pest,))
                    transaction.cursor.commit()
                    return True, 'Submitted Successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'
