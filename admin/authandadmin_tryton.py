#! /usr/bin/env python

""" Authorization and admin panel back end """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from proteus import config

from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
from decimal import Decimal
import logging
from GUI import settings


logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'
Context = config.get_config().context


class AccessUser():
    """
    Validate the user
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Tax = pool.get('account.tax')
        User = pool.get('res.user')
        Group = pool.get('res.group')

    def __init__(self):
        self.conf = config.get_config()
        self.userid = ''
        # self.tax = self.Tax.find([('name', '=', 'Restaurant Tax')])[0]

    def validate_user(self, user, password):
        """
        :param user:username of the user
        :param password: password of the user
        :return: valid id if password is correct else 0
        """
        user = user
        password = password
        try:
            with Transaction().start(DBNAME, 1):
                self.userid = self.User.get_login(user, password)
                user = self.User(id=self.userid)
                groups = user.groups
                tabs = {}
                if groups:
                    group = groups[0]
                    tabs = group.tabs.copy() if group.tabs else tabs
                return self.userid, tabs
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return 0

    def get_user(self, id):  # todo deprecate this.
        """
        gets the user with the corresponding id.
        No need for the Transaction because it is called inside a transaction.
        :param id:the id of the user
        :return:the user
        """
        try:
            user = self.User(id=id)
            return user
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None

    def get_details(self):
        """
        :return: all the details of the user
        """
        try:
            with Transaction().start(DBNAME, 1):
                tax_obj = self.Tax.search([('name', '=', 'Restaurant Tax')])[0]
                user = self.User(id=self.userid)
                company = user.main_company
                name = company.rec_name
                street = company.party.addresses[0].street
                city = company.party.addresses[0].city
                pin = company.party.addresses[0].zip
                longitude = company.longitude
                latitude = company.latitude
                apikey = company.api
                fssai = company.fssai if company.fssai else None
                tin = company.tin if company.tin else None
                tax = tax_obj.rate.multiply(100).to_eng()
                profileid = user.login
                password = user.password
                details = {'name': name, 'street': street, 'city': city, 'pin': pin, 'longitude': longitude,
                           'latitude': latitude, 'apikey': apikey, 'tax': tax,
                           'profileid': profileid, 'password': password, 'fssai': fssai, 'tin': tin}
                return details
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return {}

    def save_details(self, details):
        """
        :param details: dict of details
        :return:boolean values
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User(id=self.userid)
                tax = self.Tax.search([('name', '=', 'Restaurant Tax')])[0]
                details = details
                company = user.main_company
                party = company.party
                party.name = details['name']
                settings.company = details['name']
                settings.set_settings()
                address=party.addresses[0]
                address.street = details['street']
                address.city = details['city']
                address.zip = details['pin']
                company.longitude = details['longitude']
                company.latitude = details['latitude']
                company.api = details['apikey']
                company.fssai = details['fssai']
                company.tin = details['tin']
                tax.rate = Decimal(details['tax']).divide(100)
                user.login = details['profileid']
                if details['password']:
                    user.password = details['password']
                user.save()
                address.save()
                party.save()
                company.save()
                tax.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_group_list(self):
        """
        gets the list of available groups
        :return:none
        """
        try:
            with Transaction().start(DBNAME, 1):
                group_list = tuple(i.name for i in self.Group.search(['create_uid', '>', 0]))
                return group_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None

    def save_group(self, name):
        """
        saves a group
        :param name: name of the group
        :return:boolean True and False for saved or not
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                group = self.Group()
                group.name = name
                group.save()
                transaction.cursor.commit()
                return True, 'Saved group successfully'
        except Exception:
            return False, 'Duplicate Entry'

    def get_roles(self, group_name):
        """
        get the roles assigned to the group
        :param group_name: the name of the group
        :return:the role tuple
        """
        try:
            with Transaction().start(DBNAME, 1):
                group = self.Group.search(['name', '=', group_name])[-1]
                roles = tuple(group.tabs.keys() if group.tabs else [])
                return roles
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Duplicate Entry'

    def delete_group(self, group_name):
        """
        deletes a group
        :param group_name:the name of the group
        :return:boolean value Tru if successfully deleted
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                users = self.User.search(['groups', '=', group_name])
                if users:
                    return False, 'Users exits in this group'
                else:
                    group = self.Group.search(['name', '=', group_name])[-1]
                    group.delete((group,))
                    transaction.cursor.commit()
                    return True, 'Deleted group successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Error occurred'

    def add_role(self, group_name, role):
        """
        adds role to the group
        :param group_name:the group_name
        :param role:the roles
        :return:boolean
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                group = self.Group.search(['name', '=', group_name])[-1]
                if group.tabs:
                    group.tabs = dict(group.tabs,
                                      **{role: True}
                                      )  # some weird behaviour of trytond dict fields hence explicit assignment
                else:
                    group.tabs = {role: True}
                group.save()
                transaction.cursor.commit()
                return True, 'Added role successfully!!'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Error occurred!!'

    def delete_role(self, group_name, role):
        """deletes a role of the user"""
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                group = self.Group.search(['name', '=', group_name])[-1]
                if group.tabs:
                    tab = group.tabs
                    _, group.tabs = tab.pop(role), tab
                group.save()
                transaction.cursor.commit()
                return True, 'Deleted role successfully!!'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Error occurred!!'

    def list_group_users(self, group_name):
        """
        lists the users in the group
        :param group_name: group name
        :return:tuple of names of users
        """
        try:
            with Transaction().start(DBNAME, 1):
                users = self.User.search(['groups', '=', group_name])
                return tuple(i.name for i in users)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None


    def add_user(self, group_name, user_name):
        """
        adds a user to the group
        :param group_name:the name of the group
        :param user_name:the name of the user
        :return:boolean with the message as tuple
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User.search(['name', '=', user_name])[-1]
                if user.groups:
                    return False, 'User exists in group %s' % user.groups[0].name
                else:
                    group = self.Group.search(['name', '=', group_name])[-1]
                    user.groups = (group,)
                    user.save()
                    transaction.cursor.commit()
                    return True, 'User added successfully'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Backend error.'

    def delete_table_user(self, username):
        """
        deletes the user from the group
        :param username: the name of the user
        :return:boolean value with the message
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User.search(['name', '=', username])[-1]
                user.groups = tuple()  # each user can be assigned to only
                # a single group so pop will remove the only group
                user.save()
                transaction.cursor.commit()
                return True, 'Deleted user successfully!!'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Error occurred!!'

    def fill_users(self, group_name):
        """
        get the name of the users not belonging the group
        :param group_name: the name of the group
        :return:the list of users
        """
        try:
            with Transaction().start(DBNAME, 1):
                users = tuple(i.name for i in self.User.search(['OR',
                                                                [('groups', '=', None)],
                                                                [('groups', '!=', group_name)]]))
                return users
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None

    def get_userlist(self):
        """
        gets a list of users except the admin
        :return:tuple of user names
        """
        try:
            with Transaction().start(DBNAME, 1):
                return tuple(i.name for i in self.User.search([]) if i.id != 1)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None

    def delete_user(self, name):
        """
        deletes a user.
        :param name: the name of the user
        :return:boolean value with the message
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User.search(['name', '=', name])
                if user:
                    user_del = user[0]
                    user_del.delete((user_del,))
                    transaction.cursor.commit()
                    return True, 'Successfully deleted'
                return False, 'User Not Found'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Could not delete User'

    def get_user_details(self, name):
        """
        gets the details of the user selected
        :param name:the name of the user
        :return:the detail tuple
        """
        try:
            with Transaction().start(DBNAME, 1):
                user = self.User.search(['name', '=', name])
                if user:
                    user = user[-1]
                    return user.name, user.login, user.password
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return []

    def save_user_details(self, name, username, password):
        """
        save the details of the user
        :param name:the name of the user
        :param username:the login username
        :param password:the password
        :return:the boolean value with the message
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User.search(['name', '=', name])
                if user:
                    user = user[-1]
                    user.login = username
                    if password:
                        user.password = password
                    user.save()
                    transaction.cursor.commit()
                    return True, 'Successfully saved the details'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some error occurred while saving details'

    def create_user(self, name, username, password):
        """
        creates a new user
        :param name:the name of the user
        :param username:the login username
        :param password: the corresponding password
        :return:boolean value and the message
        """
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = Context
                user = self.User.search(['name', '=', name])
                if user:
                    return False, 'User already exists'
                else:
                    user = self.User()
                    user.name = name
                    user.login = username
                    user.password = password
                    user.save()
                    transaction.cursor.commit()
                    return True, 'Successfully created the user'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some error occurred'
