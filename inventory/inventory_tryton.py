#! /usr/bin/env python

""" Inventory Module backend """
import pdb

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from datetime import date
from proteus import config
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction

from decimal import Decimal
from process_purchaselist import CalculateDayIngredients
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class StockInventory():
    """
    provides a mechanism to calculate the stock
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Inventory = pool.get('stock.inventory')
        Location = pool.get('stock.location')
        Party = pool.get('party.party')

    def __init__(self):
        logger.info('Inside StockInventory')
        with Transaction().start(DBNAME, 1):
            self.location = self.Location.search(['name', '=', 'MyInventory'])[-1]

    def load_stock(self):
        """
        loads the stock details
        :return: the list of dictionary with the values of stock
        """
        lines = []
        with Transaction().start(DBNAME, 1):
            stock_lines = self.Inventory.search([('state', '=', 'done'), ('location', '=', self.location.id)])
            if stock_lines:
                for i in stock_lines:
                    batch = i.batch_number
                    for j in i.lines:
                        if j.quantity <= 0:
                            continue
                        dictionary = {}
                        dictionary['code'] = j.product.code
                        dictionary['item'] = j.product.template.name
                        dictionary[
                            'category'] = j.product.template.category.name if j.product.template.category else None
                        dictionary['quantity'] = Decimal(j.quantity).quantize(Decimal('0.11')).to_eng()
                        dictionary['batch_number'] = batch
                        dictionary['supplier'] = j.supplier.name if j.supplier else None
                        dictionary['expiry_date'] = j.expiry_date.strftime('%d-%m-%Y') if j.expiry_date else None
                        lines.append(dictionary)
            return lines


class KitechenInventory(StockInventory):
    """manage inventory in the kitchen"""
    global logger

    def __init__(self):
        StockInventory.__init__(self)
        logger.info('Inside Kitchen Inventory')
        with Transaction().start(DBNAME, 1):
            self.location = self.Location.search(['name', '=', 'MyStore'])[-1]


class AddStockInventory():
    """
    provides a mechanism to add stock to the inventory
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Inventory = pool.get('stock.inventory')
        InventoryLine = pool.get('stock.inventory.line')
        Party = pool.get('party.party')
        Location = pool.get('stock.location')
        Product = pool.get('product.product')
        Purchase = pool.get('purchase.purchase')
        PaymentTerm = pool.get('account.invoice.payment_term')
        Uom = pool.get('product.uom')
        User = pool.get('res.user')

    def __init__(self):
        logger.info('Inside AddStockInventory')

    def search_batch(self, batch):
        """
        search the inventory based on the batch
        :param batch: the batch of the inventory
        :return: the list of dictionary consisting of values per inventory line
        """
        logger.info('AddStockInventory searching batch initiated')
        with Transaction().start(DBNAME, 1):
            batch = batch
            purchase = self.Purchase.search(['batch_number', '=', batch])
            if purchase:
                stock = purchase[-1]
                lines_list = stock.lines
                lines = []
                for i in lines_list:
                    dataobj = {}
                    dataobj['code'] = i.product.code
                    dataobj['item'] = i.product.template.name
                    dataobj['category'] = i.product.template.category.name if i.product.template.category else None
                    dataobj['quantity'] = Decimal(i.quantity).quantize(Decimal('0.111')).to_eng()
                    dataobj['unit'] = i.unit.name
                    dataobj['rate'] = i.product.template.list_price.to_eng()
                    dataobj['supplier'] = i.supplier.name
                    lines.append(dataobj)
                return lines

    def save_inventory(self, data, batch):
        """
        creates a new quotation for the items from a supplier
        :return:boolean value eg:True for saved successfully
        """
        logger.info('AddStockInventory inventory save initiated')
        with Transaction().start(DBNAME, 1) as transaction:
            transaction.context = config.get_config().context
            batch = batch
            location = self.Location.search(['name', '=', 'MyInventory'])[-1]
            inventory = self.Inventory()
            inventory.location = location
            inventory.batch_number = batch
            inventory.save()
            for i in data:
                product = self.Product.search([('code', '=', i['code']),
                                               ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                units = self.Uom.search(['name', '=', i['units']])[-1]
                supplier = self.Party.search(['name', '=', i['supplier']])[-1]
                inventory_line = self.InventoryLine()
                inventory_line.product = product
                inventory_line.quantity = float(i['quantity'])
                inventory_line.uom = units
                inventory_line.supplier = supplier
                inventory_line.expiry_date = i['expiry_date']
                inventory_line.inventory = inventory
                inventory_line.save()
            # transaction.cursor.commit()
            inventory.state = 'done'
            inventory.save()
            transaction.cursor.commit()
            return True

    def confirm_inventory(self, data, batch):  # not used will be deprecated todo
        """
        creates a new quotation for the items from a supplier
        :return:none
        """
        try:
            batch = batch
            data = data
            location = self.Location.find(['name', '=', 'MyInventory'])[-1]
            inventory = self.Inventory.find([('batch_number', '=', batch), ('location', '=', location.id)])[-1]
            lines = inventory.lines
            for i in data:
                product = \
                    self.Product.find(
                        [('code', '=', i['code']), ('description', '=', 'Stock'), ('type', '=', 'goods')])[
                        -1]
                supplier = self.Party.find(['name', '=', i['supplier']])[-1]
                for j in lines:
                    if j.product == product:
                        pro = j.product
                        template = pro.template
                        template.list_price = Decimal(i['rate'])
                        template.save()
                        pro.save()
                        j.quantity = float(i['quantity'])
                        j.supplier = supplier
                        j.expiry_date = i['expiry_date']
                        j.save()
            inventory.state = 'done'
            inventory.save()
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def confirm_purchase(self, data, batch):
        """
        searches the purchase schedule and confirms it also adds the lines form purchase list to the inventory
        :param data:list of dictionary value of the stock to be purchased
        :param batch: the batch number to be added to the inventory
        :return: boolean value eg:True if successfully saved.
        """
        logger.info('AddStockInventory purchase confirm initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                batch = batch
                data = data
                purchase = self.Purchase.search([('batch_number', '=', batch)])[-1]
                if purchase.state == 'processing':
                    return False
                lines = purchase.lines
                party = self.Party.search(['name', '=', 'Purchase'])[-1]
                for i in data:
                    product = self.Product.search([('code', '=', i['code']),
                                                   ('description', '=', 'Stock'),
                                                   ('type', '=', 'goods')])[-1]
                    supplier = self.Party.search(['name', '=', i['supplier']])[-1]
                    for j in lines:
                        if j.product == product:
                            pro = j.product
                            template = pro.template
                            template.list_price = Decimal(i['rate'])
                            template.save()
                            pro.save()
                            j.quantity = float(i['quantity'])
                            j.supplier = supplier
                            j.save()
                purchase.party = party
                payment, = self.PaymentTerm.search(['name', '=', 'Full Payment'])
                purchase.payment_term = payment
                purchase.invoice_address = party.addresses[0]
                user = self.User(id=1)
                purchase.company = user.main_company
                purchase.save()
                # transaction.cursor.commit()
                purchase.quote((purchase,))
                purchase.confirm((purchase,))
                purchase.process((purchase,))
                transaction.cursor.commit()
            save = self.save_inventory(data, batch)
            if save:
                return True
            else:
                raise Exception('could not save or confirm')
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class ReleaseDiscard():
    """
    provides a mechanism to release a stock item or discard it
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Inventory = pool.get('stock.inventory')
        Location = pool.get('stock.location')
        Product = pool.get('product.product')
        Uom = pool.get('product.uom')
        Shipment = pool.get('stock.shipment.internal')
        ShipmentMoves = pool.get('stock.move')
        InventoryLine = pool.get('stock.inventory.line')

    def __init__(self):
        logger.info('Inside ReleaseDiscard')
        with Transaction().start(DBNAME, 1):
            self.inventory = self.Location.search(['name', '=', 'MyInventory'])[-1]
            self.kitchen = self.Location.search(['name', '=', 'MyStore'])[-1]
            self.throw = self.Location.search(['name', '=', 'Lost and Found'])[-1]
            self.used = self.Location.search(['name', '=', 'MyUsedStore'])[-1]

    def collect_batch(self, item, quantity, kitchen=None):
        """
        collects the batch number corresponding to the quantity of the item
        :param item:the name of the item
        :param quantity:the quantity to be released
        :return:boolean value or a list of batch_number and the quantity
        """
        try:
            with Transaction().start(DBNAME, 1):
                item = item
                quantity = quantity
                if kitchen:
                    inventory_list = self.Inventory.search([('location', '=', self.kitchen.id)]
                                                           , order=[('batch_number', 'ASC')])
                else:
                    inventory_list = self.Inventory.search([('location', '=', self.inventory.id)]
                                                           , order=[('batch_number', 'ASC')])
                batch_list = []
                today = date.today()
                for i in inventory_list:
                    lines = i.lines
                    for j in lines:
                        if j.product.template.name == item:
                            expiry = j.expiry_date
                            if expiry:
                                if expiry >= today:
                                    if Decimal(j.quantity) >= Decimal(quantity):
                                        batch_list.append([str(i.batch_number), str(quantity)])
                                        print [str(i.batch_number), str(quantity)]
                                        return batch_list
                                    else:
                                        quantity = Decimal(quantity) - Decimal(j.quantity)
                                        batch_list.append([str(i.batch_number), str(j.quantity)])
                                        print [str(i.batch_number), str(j.quantity)]
                return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def sort_inventory(self, inventory_list):  # dont use transactions here...as it is called within other transactions
        # unused will be deprecated
        """
        sorts the inventory list according to the batch number
        :param inventory_list: the list of inventory items
        :return: ordered inventory list
        """
        batch_list = []
        new_inventory_list = []
        try:
            for i in inventory_list:
                if i.batch_number:
                    batch_list.append(i.batch_number)
            batch_list.sort()
            for i in batch_list:
                for j in inventory_list:
                    if j.batch_number == i:
                        new_inventory_list.append(j)
            return new_inventory_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return new_inventory_list


    def release(self, item, quantity):
        """
        releases a n item form the stock
        :param item: the name of the item
        :param quantity:the quantity of the item to be released
        :return: boolean value eg:if True then release was successful
        """
        logger.info('ReleaseDiscard item release initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                quantity = Decimal(quantity)
                inventory_list = self.Inventory.search([('location', '=', self.inventory.id)]
                                                       , order=[('batch_number', 'ASC')])
                product = self.Product.search([('name', '=', item),
                                               ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                done = False
                today = date.today()
                for i in inventory_list:
                    for j in i.lines:
                        if j.product.template.name == item:
                            expiry = j.expiry_date
                            if expiry:
                                if expiry >= today:
                                    if Decimal(j.quantity) >= Decimal(quantity):
                                        j.quantity = Decimal(j.quantity) - Decimal(quantity)
                                        self.move(from_location=self.inventory, to_location=self.kitchen, item=product,
                                                  quantity=quantity,
                                                  batch_number=i.batch_number)
                                        self.store_inventory(location=self.kitchen, inventory_stock=j,
                                                             quantity=quantity, batch=i.batch_number)
                                        j.save()
                                        self.check_and_delete(i)
                                        done = True
                                    else:
                                        quantity = Decimal(quantity) - Decimal(j.quantity)
                                        self.move(from_location=self.inventory, to_location=self.kitchen, item=product,
                                                  quantity=j.quantity, batch_number=i.batch_number)
                                        self.store_inventory(location=self.kitchen, inventory_stock=j,
                                                             quantity=j.quantity, batch=i.batch_number)
                                        j.quantity = 0
                                        j.save()
                                        self.check_and_delete(i)
                                        # transaction.cursor.commit()
                    i.save()
                    transaction.cursor.commit()
                    if done:
                        return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def store_inventory(self, batch, location, quantity, inventory_stock):
        # no transaction needed
        """
        saves the item to the store or kitchen
        :return:boolean value eg:True for saved successfully
        """
        logger.info('ReleaseDiscard store inventory initiated')
        to_inventory = self.Inventory.search([('location', '=', location.id), ('batch_number', '=', batch)])
        if to_inventory:
            return self.update_store(to_inventory[0], quantity, inventory_stock)
        inventory = self.Inventory()
        inventory.location = location
        inventory.batch_number = batch
        inventory.save()
        inventory_line = self.InventoryLine()
        inventory_line.product = inventory_stock.product
        inventory_line.quantity = float(quantity)
        inventory_line.uom = inventory_stock.uom
        inventory_line.supplier = inventory_stock.supplier
        inventory_line.expiry_date = inventory_stock.expiry_date
        inventory_line.inventory = inventory
        inventory_line.save()
        # transaction.cursor.commit()
        inventory.state = 'done'
        inventory.save()
        return True

    def update_store(self, inventory, quantity, inventory_stock):
        """update the data in the inventory"""
        inventory_line, = self.InventoryLine.search([('inventory', '=', inventory.id),
                                                     ('product', '=', inventory_stock.product.id)])
        inventory_line.quantity += float(quantity)
        inventory_line.save()
        return True

    def ingredient_used(self, item, quantity):
        """
        releases a n item form the stock
        :param item: the name of the item
        :param quantity:the quantity of the item to be released
        :return: boolean value eg:if True then release was successful
        """
        logger.info('ReleaseDiscard ingredient used initiated')
        try:
            quantity = Decimal(quantity).quantize(Decimal('0.11'))
            inventory_list = self.Inventory.search([('location', '=', self.kitchen.id)]
                                                   , order=[('batch_number', 'ASC')])
            product = self.Product.search([('name', '=', item),
                                           ('description', '=', 'Stock'),
                                           ('type', '=', 'goods')])[-1]
            done = False
            today = date.today()
            for i in inventory_list:
                for j in i.lines:
                    if j.product.template.name == item:
                        expiry = j.expiry_date
                        if expiry:
                            if expiry >= today:
                                if Decimal(j.quantity) >= Decimal(quantity):
                                    j.quantity = Decimal(j.quantity) - Decimal(quantity)
                                    self.move(from_location=self.kitchen, to_location=self.used, item=product,
                                              quantity=quantity,
                                              batch_number=i.batch_number)
                                    self.store_inventory(location=self.used, inventory_stock=j,
                                                         quantity=quantity, batch=i.batch_number)
                                    j.save()
                                    self.check_and_delete(i)
                                    done = True
                                else:
                                    quantity = Decimal(quantity) - Decimal(j.quantity)
                                    self.move(from_location=self.kitchen, to_location=self.used, item=product,
                                              quantity=j.quantity, batch_number=i.batch_number)
                                    self.store_inventory(location=self.used, inventory_stock=j,
                                                         quantity=j.quantity, batch=i.batch_number)
                                    j.quantity = 0
                                    j.save()
                                    self.check_and_delete(i)
                                    # transaction.cursor.commit()
                i.save()
                if done:
                    return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def ingredient_used_canceled(self, item, quantity):
        """
        releases a n item form the stock
        :param item: the name of the item
        :param quantity:the quantity of the item to be released
        :return: boolean value eg:if True then release was successful
        """
        logger.info('ReleaseDiscard ingredient used canceled initiated')
        try:
            quantity = Decimal(quantity).quantize(Decimal('0.11'))
            inventory_list = self.Inventory.search([('location', '=', self.used.id)]
                                                   , order=[('batch_number', 'DESC')])
            product = self.Product.search([('name', '=', item),
                                           ('description', '=', 'Stock'),
                                           ('type', '=', 'goods')])[-1]
            done = False
            today = date.today()
            for i in inventory_list:
                for j in i.lines:
                    if j.product.template.name == item:
                        expiry = j.expiry_date
                        if expiry:
                            if expiry >= today:
                                # pdb.set_trace()
                                if Decimal(j.quantity) >= Decimal(quantity):
                                    j.quantity = Decimal(j.quantity) - Decimal(quantity)
                                    self.move(from_location=self.used, to_location=self.kitchen, item=product,
                                              quantity=quantity,
                                              batch_number=i.batch_number)
                                    self.store_inventory(location=self.kitchen, inventory_stock=j,
                                                         quantity=quantity, batch=i.batch_number)
                                    j.save()
                                    self.check_and_delete(i)
                                    done = True
                                else:
                                    quantity = Decimal(quantity) - Decimal(j.quantity)
                                    self.move(from_location=self.used, to_location=self.kitchen, item=product,
                                              quantity=j.quantity, batch_number=i.batch_number)
                                    self.store_inventory(location=self.kitchen, inventory_stock=j,
                                                         quantity=j.quantity, batch=i.batch_number)
                                    j.quantity = 0
                                    j.save()
                                    self.check_and_delete(i)
                                    # transaction.cursor.commit()
                i.save()
                if done:
                    return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def populate_discard(self):
        """
        gets the list of items to be discarded based on their expiry date
        :return:list of dictionary values of the item and its related values
        """
        with Transaction().start(DBNAME, 1):
            inventory = self.Inventory.search([])
            today = date.today()
            lines = []
            for j in inventory:
                for i in j.lines:
                    expiry = i.expiry_date
                    if expiry:
                        if expiry < today:
                            if i.quantity <= 0:
                                continue
                            dictionary = {}
                            dictionary['code'] = i.product.code
                            dictionary['item'] = i.product.template.name
                            dictionary['category'] = i.product.template.category.name
                            dictionary['unit'] = i.uom.name
                            dictionary['quantity'] = i.quantity
                            dictionary['batch_number'] = j.batch_number
                            lines.append(dictionary)
            return lines

    def discard(self, data):
        """
        discards the item from the inventory
        :param data:the dictionary of the item and its related value
        :return:boolean value eg: if True the discard was successful.
        """
        logger.info('ReleaseDiscard item discard initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                item = data['item']
                quantity = Decimal(data['quantity'])
                batch_number = data['batch_number']
                reason_for_discard = data['reason_for_discard']
                inventory_list = self.Inventory.search([('batch_number', '=', batch_number)])
                for inventory in inventory_list:
                    for i in inventory.lines:
                        if i.product.template.name == item:
                            item_quantity = Decimal(i.quantity).quantize(Decimal('0.111'))
                            print item_quantity, quantity
                            if item_quantity >= quantity:
                                i.quantity = item_quantity - quantity
                                self.move(from_location=self.inventory, to_location=self.throw, item=i.product,
                                          quantity=quantity,
                                          batch_number=inventory.batch_number, reason=reason_for_discard)
                                i.save()
                                transaction.cursor.commit()
                                self.check_and_delete(inventory)
                                return True
                            else:
                                return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def check_and_delete(self, inventory):  # used in a transaction block only so dont initiate a transaction here
        """
        checks the inventory and deletes the item if it has a item of quantity less than 0
        :param inventory:the inventory to be checked on
        :return:a boolean value eg:True if the process was successful
        """
        try:
            lines = inventory.lines
            for i in lines:
                if i.quantity == 0:
                    i.delete((i,))
            # inventory.reload()
            inventory.save()
            chk = inventory.lines
            if len(chk) == 0:
                inventory.state = 'cancel'
                inventory.save()
                inventory.delete((inventory,))
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


    def move(self, from_location, to_location, item, quantity, batch_number, reason=None):
        # dont use a transaction here it is already called inside a transaction block only
        """
        moves an item from a given location to another
        :param from_location:the start location
        :param to_location:the end location
        :param item:the item to be moved
        :param quantity: the quantity of the item to be moved
        :param batch_number:the batch number from which the item should be moved
        :param reason:the reason (optional) for which the move was done eg:in case of Expiry
        :return: boolean value eg:True if the move was successful
        """
        logger.info('ReleaseDiscard item move initiated')
        try:
            shipment = self.Shipment()
            from_location = from_location
            to_location = to_location
            item = item
            quantity = quantity
            batch_number = batch_number
            shipment.from_location = from_location
            shipment.to_location = to_location
            mv = self.ShipmentMoves()
            mv.from_location = from_location
            mv.to_location = to_location
            mv.product = item
            mv.quantity = float(quantity)
            mv.batch_number = batch_number
            mv.uom = item.template.default_uom
            if reason:
                mv.reason_for_discard = reason
            shipment.moves = (mv,)
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


class SchedulePurchase():
    """
    Provides a mechanism to schedule a purchase
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Party = pool.get('party.party')
        Product = pool.get('product.product')
        Uom = pool.get('product.uom')
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')
        Inventory = pool.get('stock.inventory')
        Location = pool.get('stock.location')
        User = pool.get('res.user')

    def __init__(self):
        logger.info('Inside SchedulePurchase')
        with Transaction().start(DBNAME, 1):
            self.ob = CalculateDayIngredients()

    def get_largest_batch(self):
        """
        gets the most recent batch number
        :return:the recent batch number or None
        """
        try:
            with Transaction().start(DBNAME, 1):
                purchase_list = self.Purchase.search([], order=(('batch_number', 'DESC'),))
                batch = tuple(i.batch_number for i in purchase_list if i.batch_number)
                if batch:
                    return batch[0]
                else:
                    return None
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return None

    def save_purchase(self, data, batch):
        """
        creates a new quotation for the items from a supplier
        :param data: the list of dictionary consisting of the item and its values
        :param batch: the batch number
        :return:boolean value eg:True if the purchase was saved successfully
        """
        logger.info('SchedulePurchase save purchase initiated')
        batch = batch
        data = data
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                purchase = self.Purchase()
                party = self.Party.search(['name', '=', 'Purchase'])[-1]
                user = self.User(id=1)
                purchase.company = user.main_company
                purchase.currency = user.main_company.currency
                purchase.party = party
                purchase.batch_number = batch
                purchase.save()
                # transaction.cursor.commit()
                for i in data:
                    product = self.Product.search([('code', '=', i['code']),
                                                   ('description', '=', 'Stock'),
                                                   ('type', '=', 'goods')])[-1]
                    units = self.Uom.search(['name', '=', i['units']])[-1]
                    supplier = self.Party.search(['name', '=', i['supplier']])[-1]
                    purchase_line = self.PurchaseLine()
                    purchase_line.product = product
                    purchase_line.quantity = float(i['quantity'])
                    purchase_line.unit_price = product.template.list_price
                    purchase_line.unit = units
                    purchase_line.supplier = supplier
                    purchase_line.purchase = purchase
                    purchase_line.description = 'Purchase line for Purchase id=%d' % purchase.id
                    purchase_line.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_schedules(self, from_date=None, to_date=None, supplier='All', day=None):
        """
        loads the schedule according to the from_day and to_day
        :param from_date: start_date
        :param to_date: end_date
        :return: list of dictionary of values of each schedule
        """
        logger.info('SchedulePurchase loading purchase schedules initiated')
        data = []
        try:
            with Transaction().start(DBNAME, 1):
                if not day:
                    dataobj = self.ob.calculate_requirement(from_date, to_date)
                else:
                    dataobj = self.ob.update_ingredients(day)
                for i, j in dataobj.iteritems():
                    if j[1] <= 0:
                        continue
                    dictionary = {}
                    # Product = Model.get('product.product')
                    if supplier == 'All':
                        product = self.Product.search([('name', '=', i),
                                                       ('description', '=', 'Stock'),
                                                       ('type', '=', 'goods')])
                    else:
                        product = self.Product.search([('name', '=', i),
                                                       ('product_suppliers', '=', supplier),
                                                       ('description', '=', 'Stock'),
                                                       ('type', '=', 'goods')])
                    product = product[-1] if product else None
                    if product:
                        dictionary['code'] = product.code
                        dictionary['item'] = product.template.name
                        dictionary['category'] = product.template.category.name
                        dictionary['unit'] = j[0].name
                        dictionary['quantity'] = j[1].quantize(Decimal('0.11')).to_eng()
                        suppliers = product.template.product_suppliers
                        if suppliers:
                            dictionary['supplier'] = suppliers[0].party.name
                        data.append(dictionary)
                    else:
                        pass
                return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return data


class BusinessParty():
    """
    The mechanism to manage a supplier
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Party = pool.get('party.party')
        PartyCategory = pool.get('party.category')
        Product = pool.get('product.product')
        User = pool.get('res.user')
        Account = pool.get('account.account')
        Invoice = pool.get('account.invoice')
        Address = pool.get('party.address')

    def __init__(self, category):
        self.category = category
        logger.info('Inside BusinessParty')

    def list_suppliers_with_id(self):
        """
        provides a list of suppliers with their ids
        :return: the list of suppliers with
        """
        data = {}
        with Transaction().start(DBNAME, 1):
            partylist = self.Party.search([('categories', '=', self.category)])
            for i in partylist:
                data[i.pan] = i.name
        return data

    def load_suppliers(self):
        """
        loads the supplier list
        :return:list of dictionary of supplier and corresponding values
        """
        return_list = []
        with Transaction().start(DBNAME, 1):
            partylist = self.Party.search([('categories', '=', self.category)])
            for i in partylist:
                dictionary = {}
                dictionary['code'] = str(i.pan)
                dictionary['name'] = i.name
                dictionary['address'] = i.addresses[0].full_address
                return_list.append(dictionary)
        return return_list

    def get_supplier(self, code):
        """
        gets the supplier corresponding to the code
        :param code:the code of the supplier
        :return:the dictionary of the supplier and its corresponding values
        """
        dictionary = {}
        with Transaction().start(DBNAME, 1):
            party = self.Party.search([('pan', '=', code),
                                       ('categories', '=', self.category)])[-1]
            dictionary['name'] = party.name
            dictionary['pan'] = party.pan
            dictionary['street'] = party.addresses[0].street
            dictionary['city'] = party.addresses[0].city
            dictionary['zip'] = party.addresses[0].zip
        return dictionary

    def create_supplier(self, datadict):
        """
        creates a supplier
        :param datadict:the dictionary of supplier and corresponding values
        :return:boolean value eg:True if supplier saved successfully
        """
        logger.info('BusinessParty saving supplier initiated')
        data = datadict
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                party = self.Party.search([('pan', '=', data['pan']),
                                           ('categories', '=', self.category)])
                if party:
                    return False
                party = self.Party()
                categories = self.PartyCategory()
                categories.name = self.category
                party.categories = (categories,)
                user = self.User(id=1)
                company = user.main_company
                accounts = self.Account.search([('kind', 'in',
                                                 ['receivable', 'payable', 'revenue', 'expense']),
                                                ('company', '=', company.id), ])

                accounts = {a.kind: a for a in accounts}
                party.name = data['name']
                party.pan = data['pan']
                address = self.Address()
                address.street = data['street']
                address.city = data['city']
                address.zip = data['zip']
                party.addresses = (address,)
                party.account_payable = accounts['payable']
                party.account_receivable = accounts['receivable']
                party.save()
                transaction.cursor.commit()
                return True

        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def edit_supplier(self, datadict):
        """
        saves a supplier
        :param datadict:the dictionary of supplier and corresponding values
        :return:boolean value eg:True if supplier saved successfully
        """
        logger.info('BusinessParty saving supplier initiated')
        data = datadict
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                party = self.Party.search([('pan', '=', data['pan']),
                                           ('categories', '=', self.category)])
                if party:
                    party, = party
                    party.name = data['name']
                    party.pan = data['pan']
                    address = party.addresses[0]
                    address.street = data['street']
                    address.city = data['city']
                    address.zip = data['zip']
                    party.save()
                    transaction.cursor.commit()
                    return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def delete_supplier(self, code):
        """
        deletes the supplier
        :param code:the code of the supplier
        :return:list of boolean value and the message to be displayed
        """
        logger.info('BusinessParty delete supplier initiated')
        if self.category == 'Supplier':
            try:
                with Transaction().start(DBNAME, 1) as transaction:
                    party = self.Party.search([('pan', '=', code), ('categories', '=', self.category)])[0]
                    supplier_produts = self.Product.search([('product_suppliers', '=', party.name)])
                    if supplier_produts:
                        return [False,
                                'The party is a supplier of a product,'
                                ' remove the party from the supplier of a product to delete']
                    category = party.categories[0]
                    category.name = 'Deleted Supplier'
                    category.save()
                    party.save()
                    transaction.cursor.commit()
                    return [True, 'Success fully deleted the supplier']
            except Exception:
                if settings.level == 10:
                    logger.exception('raised exception')
                return [False, 'Could not delete due to unknown reasons']
        elif self.category == 'Customer':
            try:
                with Transaction().start(DBNAME, 1) as transaction:
                    party = self.Party.search([('pan', '=', code), ('categories', '=', self.category)])[0]
                    customer_invoices = self.Invoice.search([('party', '=', party), ('state', '=', 'draft')])
                    if customer_invoices:
                        return [False,
                                'The customer has unpaid dues,'
                                ' pay the outstanding dues to delete the customer.']
                    category = party.categories[0]
                    category.name = 'Deleted Customer'
                    category.save()
                    party.save()
                    transaction.cursor.commit()
                    return [True, 'Success fully deleted the Customer']
            except Exception:
                if settings.level == 10:
                    logger.exception('raised exception')
                return [False, 'Could not delete due to unknown reasons']


class ItemProduct():
    """
    Manages the items
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Product = pool.get('product.product')
        ProductUom = pool.get('product.uom')
        ProductTemplate = pool.get('product.template')
        ProductCategory = pool.get('product.category')
        ProductSuppliers = pool.get('purchase.product_supplier')
        Inventory = pool.get('stock.inventory')
        Ingredient = pool.get('product.ingredientsofdish')
        Party = pool.get('party.party')
        User = pool.get('res.user')
        Account = pool.get('account.account')

    def __init__(self):
        logger.info('Inside ItemProduct')
        self.productlist = object
        self.product = object
        with Transaction().start(DBNAME, 1):
            user = self.User(id=1)
            self.company = user.main_company
            accounts = self.Account.search([
                ('kind', 'in', ['receivable', 'payable', 'revenue', 'expense']),
                ('company', '=', self.company.id)
            ])
            self.accounts = {a.kind: a for a in accounts}


    def load_items(self):
        """
        loads the items
        :return:list of dictionary of the item and its corresponding values
        """
        return_list = []
        try:
            with Transaction().start(DBNAME, 1):
                self.productlist = self.Product.search([('description', '=', 'Stock'), ('type', '=', 'goods')])
                for i in self.productlist:
                    dictionary = {}
                    dictionary['item_no'] = str(i.code)
                    dictionary['item'] = i.template.name
                    dictionary['category'] = i.template.category.name \
                        if i.template.category is not None else 'No Category Assigned'
                    dictionary['rate'] = i.list_price_uom.to_eng()
                    return_list.append(dictionary)
                return return_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return return_list

    def add_item(self, obj):  # deprecated
        """
        creates a new Item(product)
        :return:boolean value eg:True if the value item is saved
        """
        logger.info('ItemProduct adding item initiated')
        try:
            if not obj['edit']:
                unit, = self.ProductUom.find([('name', '=', obj['units'])])
                template = self.ProductTemplate()
                try:
                    if self.Product.find([('code', '=', obj['id']), ('description', '=', 'Stock'),
                                          ('type', '=', 'goods')])[-1]:
                        return False
                    if self.Product.find([('name', '=', obj['name']), ('description', '=', 'Stock'),
                                          ('type', '=', 'goods')])[-1]:
                        return False
                except Exception:
                    pass
                template.category = self.ProductCategory.find([('name', '=', obj['category'])])[-1]
                template.default_uom = unit
                template.purchase_uom = unit
                template.type = 'goods'
            else:
                product = self.Product.find([('code', '=', obj['id']), ('description', '=', 'Stock'),
                                             ('type', '=', 'goods')])[-1]
                template = product.template
                unit, = self.ProductUom.find([('name', '=', obj['units'])])
                template.default_uom = unit
                template.purchase_uom = unit
                template.category = self.ProductCategory.find([('name', '=', obj['category'])])[-1]

            rate = Decimal(obj['rate'])
            cost = rate / 2
            template.name = obj['name']
            template.list_price = Decimal(rate)
            template.cost_price = Decimal(cost)
            template.purchasable = True
            template.account_expense = self.accounts['expense']
            template.account_receivable = self.accounts['receivable']
            product = self.Product.find([('name', '=', template.name),
                                         ('description', '=', 'Stock'), ('type', '=', 'goods')])
            if product:
                product = product[-1]
            else:
                product = self.Product.find([('name', '=', template.name), ('type', '=', 'goods')])
                ids = []
                for i in product:
                    ids.append(i.id)
                ids.sort()
                print "ids", ids
                product = self.Product(id=ids[-1])
            product.code = obj['id']
            product.description = 'Stock'
            product.save()
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def create_item(self, obj):
        """
        creates a new Item(product)
        :return:boolean value eg:True if the value item is saved
        """
        logger.info('ItemProduct adding item initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                unit, = self.ProductUom.search([('name', '=', obj['units'])])
                template = self.ProductTemplate()
                try:
                    if self.Product.search([('code', '=', obj['id']), ('description', '=', 'Stock'),
                                            ('type', '=', 'goods')])[-1]:
                        return False
                except Exception:
                    pass
                template.category = self.ProductCategory.search([('name', '=', obj['category'])])[-1]
                template.default_uom = unit
                template.purchase_uom = unit
                template.type = 'goods'
                rate = Decimal(obj['rate'])
                cost = rate / 2
                template.name = obj['name']
                template.list_price = Decimal(rate)
                template.cost_price = Decimal(cost)
                template.purchasable = True
                template.account_expense = self.accounts['expense']
                template.account_receivable = self.accounts['receivable']
                template.save()
                # transaction.cursor.commit()
                product = self.Product()
                product.template = template
                product.code = obj['id']
                product.description = 'Stock'
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def save_item(self, obj):
        """
        saves an  Item(product) details
        :return:boolean value eg:True if the value item is saved
        """
        logger.info('ItemProduct adding item initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                product = self.Product.search([('code', '=', obj['id']), ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                template = self.ProductTemplate(id=product.template.id)
                unit, = self.ProductUom.search([('name', '=', obj['units'])])
                template.default_uom = unit
                template.purchase_uom = unit
                template.category = self.ProductCategory.search([('name', '=', obj['category'])])[-1]
                rate = Decimal(obj['rate'])
                cost = rate / 2
                template.name = obj['name']
                template.list_price = Decimal(rate)
                template.cost_price = Decimal(cost)
                template.purchasable = True
                template.account_expense = self.accounts['expense']
                template.account_receivable = self.accounts['receivable']
                template.save()
                # transaction.cursor.commit()
                product.description = 'Stock'
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def load_rows(self, id=None):
        """
        :param id: the id of the corresponding item
        :return: dictionary of the item corresponding to the id and its values
        """
        data = {}
        try:
            with Transaction().start(DBNAME, 1):
                newid = id
                product = self.Product.search([('code', '=', newid),
                                               ('description', '=', 'Stock'), ('type', '=', 'goods')])[-1]
                data['name'] = product.template.name
                data['units'] = product.template.default_uom.name
                data['category'] = product.template.category.name \
                    if product.template.category is not None else 'No Category Assigned'
                data['rate'] = product.template.list_price.to_eng()
                return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return data

    def delete_rows(self, id=None):
        """
        deletes an item
        :param id: id of the product
        :return: list of boolean value and the message to be displayed
        """
        logger.info('ItemPrduct delete item initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                newid = id
                product = self.Product.search([('code', '=', newid),
                                               ('description', '=', 'Stock'), ('type', '=', 'goods')])[-1]
                stock_lines = self.Inventory.search(['state', '=', 'done'])
                if stock_lines:
                    for i in stock_lines:
                        for j in i.lines:
                            if product.template.name == j.product.template.name:
                                return [False, 'The item exists in stock, discard them to delete']
                ingredients = self.Ingredient.search([('ingredient', '=', product.id)])
                if ingredients:
                    return [False,
                            'The item exists in ingredients of a product, remove them from the ingredients to delete']
                product.active = False
                product.save()
                transaction.cursor.commit()
                return [True, 'Success fully deleted']
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return [False, 'Unknown Error check debug data']

    def complete_unit(self):
        """
        Search all the units
        :return: list of the unit names
        """
        with Transaction().start(DBNAME, 1):
            return tuple(i.name for i in self.ProductUom.search([]))

    def load_supplier_table(self, id=None):
        """
        loads the supplier table in the item dialog
        :param id: product id
        :return: list of dictionary of suppliers and its corresponding values
        """
        line = []
        newid = id
        with Transaction().start(DBNAME, 1):
            product = self.Product.search([('code', '=', newid), ('description', '=', 'Stock'),
                                           ('type', '=', 'goods')])[-1]
            supplier_list = product.template.product_suppliers
            for i in supplier_list:
                data = {}
                data['code'] = i.party.pan
                data['name'] = i.party.name
                line.append(data)
            return line

    def add_supplier_to_item(self, code=None, pan=None):
        """
        adds a new supplier
        :param code: code of the item(product)
        :param pan:is pan of party or the code of the party
        :return:boolean value eg:True if added successfully
        """
        logger.info('ItemProduct adding supplier to item initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                code = code
                pan = pan
                product = self.Product.search([('code', '=', code), ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                supplier = self.Party.search([('pan', '=', pan), ('categories', '=', 'Supplier')])[-1]
                check = product.search([('product_suppliers', '=', supplier.name), ('id', '=', product.id)])
                if check:
                    return False
                template = self.ProductTemplate(id=product.template.id)
                product_supplier = self.ProductSuppliers()
                product_supplier.party = supplier
                product_supplier.product = template  # since product is a many2one to the product
                product_supplier.company = supplier.account_payable.company
                product_supplier.currency = supplier.account_payable.company.currency
                product_supplier.save()
                # if template.product_suppliers:
                # template.product_suppliers = template.product_suppliers + (product_supplier,)
                # else:
                # template.product_suppliers = (product_supplier,)
                product.template = template
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def delete_supplier_from_item(self, code=None, pan=None):
        """
        removes a supplier
        :param code: code of the item(product)
        :param pan:is pan of party or the code of the party
        :return:boolean value eg:True if deleted successfully
        """
        logger.info('ItemProduct deleting supplier from item initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                code = code
                pan = pan
                product = self.Product.search([('code', '=', code), ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                product_supplier = product.template.product_suppliers
                for i in product_supplier:
                    if i.party.pan == pan:
                        i.delete((i,))
                        # transaction.cursor.commit()
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_details_of_code(self, code):
        """
        returns the item, category and units based on the code
        :param code: code of the product
        :return: dictionary of the item and its details
        """
        row = {}
        try:
            with Transaction().start(DBNAME, 1):
                i = self.Product.search([('code', '=', code),
                                         ('description', '=', 'Stock'), ('type', '=', 'goods')])
                if i:
                    i = i[-1]
                    row['item'] = i.template.name
                    row['category'] = i.template.category.name
                    row['units'] = i.template.default_uom.name
                    row['rate'] = i.template.list_price.to_eng()
                    suppliers = i.template.product_suppliers
                    if suppliers:
                        row['supplier'] = suppliers[0].party.name
                    return row
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return row

    def get_details_of_item(self, item):
        """
        returns the item, category and units based on the code
        :param item: name of the product
        :return: dictionary of the item and its details
        """
        row = {}
        try:
            with Transaction().start(DBNAME, 1):
                product = self.Product.search([('name', '=', item),
                                               ('description', '=', 'Stock'), ('type', '=', 'goods')])[-1]
                row['code'] = product.code
                row['category'] = product.template.category.name
                row['units'] = product.template.default_uom.name
                row['rate'] = product.template.list_price.to_eng()
                suppliers = product.template.product_suppliers
                if suppliers:
                    row['supplier'] = suppliers[0].party.name
                return row
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return row

    def fill_item_list(self):
        """
        provides a list of the items
        :return: a list of item names
        """
        return_list = []
        with Transaction().start(DBNAME, 1):
            self.productlist = self.Product.search([('description', '=', 'Stock'), ('type', '=', 'goods')])
            for i in self.productlist:
                return_list.append(i.template.name)
            return return_list


class CategoryOfProduct():
    """
    Provides a mechanism to manage the category of the item(product)
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Category = pool.get('product.category')

    def __init__(self):
        logger.info('inside CategoryOfProduct')

    def create_category(self, name):
        """
        creates a new category
        :param name: category name
        :return: boolean value True or False for saved or unsaved
        """
        logger.info('CategoryOfProduct category create initiated')
        newname = name
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                categories = self.Category.search([('name', '=', newname), ('parent', '=', 'Ingredients')])
                parent = self.Category.search(['name', '=', 'Ingredients'])
                if categories:
                    return False
                category = self.Category()
                if parent:
                    category.parent = parent[-1]
                category.name = newname
                category.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_categories(self):
        """
        provides a list of categories
        :return:list of category names
        """
        with Transaction().start(DBNAME, 1):
            categorieslist = self.Category.search(['parent', '=', 'Ingredients'])
            return tuple(i.name for i in categorieslist)