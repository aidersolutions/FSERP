#! /usr/bin/env python

""" Waste Module backend """

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


class WasteMenu():
    """
    Manages the wastes produced in the menu items
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Menu = pool.get('product.product')
        Location = pool.get('stock.location')
        Product = pool.get('product.product')
        Shipment = pool.get('stock.shipment.internal')
        ShipmentMoves = pool.get('stock.move')
        Move = pool.get('stock.move')

    def __init__(self):
        logger.info('Inside WasteMenu')
        with Transaction().start(DBNAME, 1):
            self.inventory = self.Location.search(['name', '=', 'MyInventory'])[-1]
            self.throw = self.Location.search(['name', '=', 'Lost and Found'])[-1]

    def populate_item(self, model):
        """
        Populates the dish items
        :param model: the Qt model in which the item names are to be populated
        :return: returns a filled model
        """
        with Transaction().start(DBNAME, 1):
            newmodel = model
            menu = self.Menu.search([('description', '=', 'Dish'), ('type', '=', 'goods')])
            menulist = [i.template.name for i in menu]
            newmodel.addItems(menulist)

    def get_details_of_code(self, code):
        """
        finds dish,category corresponding to the code
        :param code: dish code
        :return: dictionary of the dish and other details
        """
        newid = code
        data = {}
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search([('code', '=', newid), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                data['item'] = menu.template.name
                data['category'] = menu.template.category.name
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
        return data

    def get_details_of_item(self, item):
        """
        finds code,category of the item
        :param item: dish name
        :return: dictionary of the dish and other details
        """
        newitem = item
        data = {}
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search([('name', '=', newitem), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                data['code'] = menu.code
                data['category'] = menu.template.category.name
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
        return data

    def discard(self, data):
        """
        adds the dish to the wastes for the present day
        :param data:the dictionary of the dish and other details
        :return: boolean value True if the process was successful
        """
        logger.info('WasteMenu discard initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                item = data['item']
                product = self.Product.search([('name', '=', item), ('description', '=', 'Dish'),
                                               ('type', '=', 'goods')])[-1]
                quantity = Decimal(data['quantity'])
                reason_for_discard = data['reason_for_discard']
                state = self.move(from_location=self.inventory, to_location=self.throw, item=product,
                                  quantity=quantity, reason=reason_for_discard)
                transaction.cursor.commit()
                if state:
                    return True
                else:
                    return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def move(self, from_location, to_location, item, quantity, reason=None):
        """
        Moves an item to the waste
        :param from_location: the start location
        :param to_location: the end location
        :param item: the item to be sent to the waste
        :param quantity: the quantity
        :param reason: the reason optional
        :return: boolean value True if the item was moved
        """
        try:
            shipment = self.Shipment()
            from_location = from_location
            to_location = to_location
            item = item
            quantity = quantity
            shipment.from_location = from_location
            shipment.to_location = to_location
            new_move = self.ShipmentMoves()
            new_move.from_location = from_location
            new_move.to_location = to_location
            new_move.product = item
            new_move.quantity = float(quantity)
            new_move.uom = item.template.default_uom
            shipment.moves = (new_move,)
            if reason:
                new_move.reason_for_discard = reason
            shipment.save()
            shipment.wait((shipment,))
            shipment.done((shipment,))
            shipment.assign_wizard((shipment,))
            state = shipment.assign_try((shipment,))
            if not state:
                shipment.assign_force((shipment,))
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def find_itemdiscard(self, from_date, to_date):
        """
        shows the items discarded on those days
        :param from_date:start date
        :param to_date:end date
        :return:list of dictionary of the items in the waste category of the given dates
        """
        dataobj = []
        with Transaction().start(DBNAME, 1):
            datalist = self.Move.search([('write_date', '>=', from_date), ('write_date', '<=', to_date)])
            for i in datalist:
                if i.product.description == 'Dish':
                    dictionary = {}
                    dictionary['code'] = i.product.code
                    dictionary['item'] = i.product.template.name
                    dictionary['category'] = i.product.template.category.name
                    dictionary['quantity'] = i.quantity
                    dictionary['reason_for_discard'] = i.reason_for_discard
                    dataobj.append(dictionary)
        return dataobj


class WasteIngredients():
    """
    Manages the wasted Ingredients
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Move = pool.get('stock.move')

    def __init__(self):
        logger.info('Inside WasteIngredients')

    def find_itemdiscard(self, from_date, to_date):
        """
        shows the ingredients discarded on those days
        :param from_date:start date
        :param to_date:end date
        :return:list of moves
        """
        dataobj = []
        with Transaction().start(DBNAME, 1):
            datalist = self.Move.search([('create_date', '>=', from_date), ('create_date', '<=', to_date)])
            for i in datalist:
                if i.product.description == 'Stock' and i.reason_for_discard:
                    dictionary = {}
                    dictionary['code'] = i.product.code
                    dictionary['item'] = i.product.template.name
                    dictionary['category'] = i.product.template.category.name
                    dictionary['quantity'] = i.quantity
                    dictionary['units'] = i.uom.name
                    dictionary['reason_for_discard'] = i.reason_for_discard
                    dataobj.append(dictionary)
        return dataobj