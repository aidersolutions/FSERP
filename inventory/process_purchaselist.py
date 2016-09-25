#! /usr/bin/env python

""" Purchase Process backend only calculation not updating the db"""

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from decimal import Decimal
from dateutil.rrule import DAILY, rrule
from datetime import date, timedelta, datetime
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class CalculateDayIngredients():
    """
    Mechanism to calculate the ingredients of the day
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Weekly = pool.get('weeklymenu.weeklymenu')
        Ingredient = pool.get('product.ingredientsofdish')

    def __init__(self):
        logger.info('Inside CalculateDayIngredients')
        self.day = None
        self.quantity = None
        self.serve = None


    def calculate_requirement(self, from_date, to_date):
        # the only method used by us, original name of function 'difference_with_stock'
        """
        finds the difference between the current stock with the future
        requirement after considering the present need
        and return a dataobj purchase schedule preparation
        :param from_date:the start date
        :param to_date: the end date
        :return:list of dictionary
        """
        try:
            from_date = from_date
            to_date = to_date
            today = (datetime.today()).strftime("%Y-%m-%d")
            future_required_ingredients = self.get_ingredients(from_date=from_date, to_date=to_date)
            intermediate_requirement_ingredients = {}
            if (today != from_date):
                intermediate_requirement_ingredients = self.get_ingredients(from_date=today, to_date=from_date)
            stock = ManageInventory()
            current_stock = stock.get_stock()
            newdata = self.compare_remove_ingredients(
                current_stock, intermediate_requirement_ingredients)
            differnecedata = self.compare_remove_ingredients(future_required_ingredients, newdata)
            # explaination
            '''
            new_stock=stock(source)-intermediate_requirement(target)
            requirement=future_requirement(source)-new_stock(target)
            '''
            return differnecedata
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def get_ingredients(self, from_date, to_date):
        """
        gets the required ingredients from a date to a date
        :param from_date: start date
        :param to_date: end date
        :return: dict of ingredients
        """
        previousdata = {}
        try:
            daterange = self.get_date_range(start_date=from_date, end_date=to_date)
            for date_value in daterange:
            # loops through each day in the date range and finds the ingredients
                day = date_value.strftime("%A")
                newdata = self.update_ingredients(day.lower())
                previousdata = self.aggregate_ingredients(previousdata, newdata)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
        return previousdata

    def get_date_range(self, start_date, end_date):
        """
        gets the daterange between the dates
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        daterange = rrule(DAILY, dtstart=start_date, until=end_date)
        return daterange

    def update_ingredients(self, day):
        """
        gets the ingredients required for a day=[monday,tuesday..etc]
        :param day: day in a week
        :return:
        """
        data = {}  # to store data in the format of {product_name:(UOM,Quantity)}
        try:
            self.day = day
            weekdishes = self.Weekly.search(['day', '=', self.day])
            for dish_obj in weekdishes:
                product = dish_obj.dish
                self.serve = product.serve if product.serve else 1
                self.quantity = dish_obj.default_quantity  # dishes quantity
                ingredientslist = self.Ingredient.search(['dish', '=', product.id])
                for ingredient_obj in ingredientslist:
                    namekey = ingredient_obj.ingredient.template.name
                    #if index == 0:  # in the begining start appending the value
                    #    new_uom, new_quantity = self.convert_uom_to_higher(
                    #        ingredient_obj.quantity_uom, (ingredient_obj.quantity * self.quantity))
                        # removing self.serve fixes the bug, but why do we
                        # have that in the first place? investigate
                        # why do we look index and not directly the key? it
                        # adds another unnecessary nesting here.
                    #    data[namekey] = (new_uom, new_quantity)
                    #else:  # later update if the value exists else append
                    if data.get(namekey):  # update
                        quantity_unit, ingredient_quantity = data[namekey]
                        if ingredient_obj.quantity_uom.category.id == quantity_unit.category.id:
                            uom, ingredient_quantity = self.add_quantity(
                                from_uom=ingredient_obj.quantity_uom, from_quantity=ingredient_obj.quantity,
                                to_uom=quantity_unit, to_quantity=ingredient_quantity)
                            quantity = Decimal(
                                (ingredient_quantity * self.quantity)).quantize(
                                    Decimal('0.111'))
                            data[namekey] = (uom, quantity)
                    else:  # append
                        new_uom, new_quantity = self.convert_uom_to_higher(
                            ingredient_obj.quantity_uom, (ingredient_obj.quantity * self.quantity))
                        data[namekey] = (new_uom, new_quantity)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
        return data

    def aggregate_ingredients(self, previousdata, newdata):
        """
        Aggregates the data from two data sets
        :param previousdata: previously aggregated data
        :param newdata: new data from a day
        :return:new aggregated data object
        """
        try:
            previousdata = previousdata.copy()
            newdata = newdata.copy()
            dataobj = previousdata
            # print "previous data", previousdata, "\n"
            # print "next data", newdata, "\n"
            if previousdata != {}:
                for i, j in newdata.iteritems():
                    if previousdata.get(i):
                        # print i, j
                        quantity_unit, ingredient_quantity = previousdata[i]
                        if j[0].category.id == quantity_unit.category.id:
                            uom, ingredient_quantity = self.add_quantity(
                                from_uom=j[0], from_quantity=j[1], to_uom=quantity_unit,
                                to_quantity=ingredient_quantity)
                            dataobj[i] = (uom, ingredient_quantity)
                    else:  # append
                        dataobj[i] = (j[0], j[1])
                return dataobj
            else:
                return newdata
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def compare_remove_ingredients(self, source, target):
        """
        compares two data objects source and target, if there exists any
        objects from source in target, subtract it
        from the target or remove it if needed
        :param source:lower_data_set
        :param target: larger_data_set
        :return:difference data
        """
        try:
            source = source.copy()
            target = target.copy()
            # print '\nsource', source
            # print '\ntarget', target
            if source:
                for i, j in source.iteritems():
                    if target.get(i):
                        source_uom, source_quantity = j
                        target_uom, target_quantity = target[i]
                        newuom, newquantity = self.sub_quantity(
                            from_uom=source_uom, from_quantity=source_quantity,
                            to_uom=target_uom, to_quantity=target_quantity)
                        if not newquantity <= 0:
                            source[i] = (newuom, newquantity)
                        else:
                            source[i] = (newuom, Decimal(0))
                    else:
                        pass
                # print '\ntarget returned', source
                return source
            else:
                return source
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def add_quantity(self, from_uom, from_quantity, to_uom, to_quantity):
        """
        converts all the quantity to the higher order eg: gm to kg and adds
        them. The from and to doesnt matter but
        their pair with quantities do matter
        :param from_uom: uom1
        :param to_uom: uom2
        :param from_quantity: quantity1
        :param to_quantity: quantity2
        :return: higher_uom,sum_of_quantity_in_higher_uom
        """
        try:
            to_uom, to_quantity = self.convert_uom_to_higher(to_uom, to_quantity)
            from_uom, from_quantity = self.convert_uom_to_higher(from_uom, from_quantity)
            quantity = from_quantity + to_quantity
            quantity = Decimal(quantity).quantize(Decimal('0.111'))
            # print 'the quantity', quantity
            return to_uom, quantity
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def sub_quantity(self, from_uom, from_quantity, to_uom, to_quantity):
        """
        converts all the quantity to the higher order eg: gm to kg and
        subtracts them. The from and to doesnt matter but
        their pair with quantities do matter
        :param from_uom: uom1
        :param to_uom: uom2
        :param from_quantity: quantity1
        :param to_quantity: quantity2
        :return: higher_uom,difference_of_quantity_in_higher_uom
        """
        try:
            to_uom, to_quantity = self.convert_uom_to_higher(to_uom, to_quantity)
            from_uom, from_quantity = self.convert_uom_to_higher(from_uom, from_quantity)
            quantity = from_quantity - to_quantity
            quantity = Decimal(quantity).quantize(Decimal('0.111'))
            return to_uom, quantity
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def convert_uom_to_higher(self, uom, quantity):
        """
        converts the uom to higher uom and its quantity to higher uom equivalent
        :param uom:unit of measurement
        :param quantity:the quantity
        :return:the higher uom and equivalent quantity
        """
        try:
            lower_uom = uom
            lower_quantity = quantity
            factor = Decimal(lower_uom.factor)
            lower_quantity = Decimal(lower_quantity)
            quantity = lower_quantity.multiply(factor)
            uom, = lower_uom.search([('category', '=', lower_uom.category.id), ('factor', '=', 1)])
            quantity = Decimal(quantity).quantize(Decimal('0.111'))
            return uom, quantity
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')


class ManageInventory():
    """
    Manages the Inventory
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Location = pool.get('stock.location')
        Product = pool.get('product.product')
        Inventory = pool.get('stock.inventory')

    def __init__(self, kitchen=None):
        logger.info('Inside ManageInventory')
        if kitchen:
            self.inventory, = self.Location.search([('name', '=', 'MyStore')])
        else:
            self.inventory, = self.Location.search(
                [('name', '=', 'MyInventory')])  # how does this work :O ??


    def get_stock(self):
        """
        fetches the stock from MyInventory
        :return: stocks in my inventory
        """
        try:
            stockdata = self.load_stock()
            newdata = self.convert_stock(
                stockdata)
                # circular dependency of objects exists but just calls a method not state dependent
            return newdata
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def convert_stock(self, data):
        """
        convert the data
        :param data: {(inventory_location_id,ingredient_id):ingredient_quantity}
        :return:{ingredient_name:(ingredient_uom,ingredient_quantity)}
        """
        newdata = {}
        try:
            data = data
            processing = CalculateDayIngredients()
            for i, j in data.iteritems():
                product = self.Product(id=i[1])
                uom = product.template.default_uom
                quantity = j
                if newdata.get(product.template.name):
                    olduom, oldquantity = newdata[product.template.name]
                    newuom, newquantity = processing.add_quantity(
                        from_uom=uom, from_quantity=quantity,
                        to_uom=olduom, to_quantity=oldquantity)
                    newdata[product.template.name] = (newuom, newquantity)
                else:
                    newdata[product.template.name] = (uom, quantity)
            return newdata
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def calculate_ingredients(self, data):
        # todo deprecate after test, not needed
        """
        aggregates the data such that no multiple entries exists and they have summed up
        :param data: {(inventory_location_id,ingredient_id):ingredient_quantity}
        :return: wihtout repeated keys {(inventory_location_id,ingredient_id):ingredient_quantity}
        """
        newdata = {}
        try:
            data = data
            processing = CalculateDayIngredients()
            n = 0  # 1st iteration
            for i, j in data.iteritems():
                if not n:
                    newdata[i] = j
                    n = 1  # 1st iteration no more
                else:
                    if newdata.get(i):
                        uom, quantity = newdata[i]
                        newuom, newquantity = processing.add_quantity(
                            from_uom=j[0], from_quantity=j[1], to_uom=uom, to_quantity=quantity)
                        newdata[i] = (newuom, newquantity)
                    else:
                        newdata[i] = (j[0], j[1])
            return newdata
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def load_stock(self):
        """loads the current stock available"""
        dictionary = {}
        try:
            stock_lines = self.Inventory.search(
                [('state', '=', 'done'), ('location', '=', self.inventory.id)])
            if stock_lines:
                for i in stock_lines:
                    for j in i.lines:
                        today = date.today()
                        expiry = j.expiry_date if j.expiry_date else today - timedelta(days=1)
                        if expiry >= today:
                            key = (j.id, j.product.id)
                            value = j.quantity
                            dictionary[key] = value
            return dictionary
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
