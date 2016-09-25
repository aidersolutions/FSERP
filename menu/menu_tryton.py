#! /usr/bin/env python

""" Menu Module backend """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

# import os, sys
from decimal import Decimal
import logging
from GUI import settings
import trytond
from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
from datetime import date
from proteus import config
from inventory.process_purchaselist import ManageInventory, CalculateDayIngredients
from inventory.inventory_tryton import ReleaseDiscard

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class MenuProduct():
    """
    Manages menu items
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Category = pool.get('product.category')
        Product = pool.get('product.product')
        ProductUom = pool.get('product.uom')
        ProductTemplate = pool.get('product.template')
        ProductCategory = pool.get('product.category')
        Tax = pool.get('account.tax')

    def __init__(self):
        logger.info('Inside MenuProduct')
        self.productlist = object
        self.product = object

    def load_menus(self):
        """
        loads the menu items
        :return: list of dictionary of menu items
        """
        with Transaction().start(DBNAME, 1):
            self.productlist = self.Product.search([('description', '=', 'Dish'), ('type', '=', 'goods')])
            return_list = []
            for i in self.productlist:
                dictionary = {}
                dictionary['item_no'] = str(i.code)
                dictionary['item'] = i.template.name
                dictionary['category'] = i.template.category.name
                dictionary['rate'] = i.list_price_uom.to_eng()
                return_list.append(dictionary)
            return return_list

    def new_dish(self, obj):
        """
        adds a new dish to the menu
        :param obj: the dictionary of dish and its corresponding data
        :return:boolean value True if the dish was saved
        """
        logger.info('MenuProduct new dish initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                unit, = self.ProductUom.search([('name', '=', 'Unit')])
                try:
                    _ = \
                        self.Product.search(
                            [('code', '=', obj['id']), ('description', '=', 'Dish'), ('type', '=', 'goods')])[-1]
                    return False
                except IndexError:
                    pass
                try:
                    template = \
                        self.ProductTemplate.search(
                            [('name', '=', obj['name']), ('type', '=', 'goods')])[-1]
                except IndexError:
                    template = self.ProductTemplate()
                template.category = self.ProductCategory.search([('name', '=', obj['category'])])[-1]
                template.default_uom = unit
                template.type = 'goods'
                rate = Decimal(obj['rate'])
                cost = rate / 2
                template.name = obj['name']
                template.list_price = Decimal(rate)
                template.cost_price = Decimal(cost)
                template.save()
                tax = self.Tax.search([('name', '=', 'Restaurant Tax')])[-1]
                template.customer_taxes = (tax,)
                template.save()
                product = self.Product()
                product.template = template
                product.code = obj['id']
                product.description = 'Dish'
                product.serve = Decimal(obj['serve'])
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def update_dish(self, obj):
        """
        updates a dish in the menu
        :param obj: the dictionary of dish and its corresponding data
        :return:boolean value True if the dish was saved
        """
        logger.info('MenuProduct update dish initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                product = \
                    self.Product.search(
                        [('code', '=', obj['id']), ('description', '=', 'Dish'), ('type', '=', 'goods')])[-1]
                template = product.template
                template.category = self.ProductCategory.search([('name', '=', obj['category'])])[-1]
                rate = Decimal(obj['rate'])
                cost = rate / 2
                template.name = obj['name']
                template.list_price = Decimal(rate)
                template.cost_price = Decimal(cost)
                template.save()
                product.description = 'Dish'
                product.serve = Decimal(obj['serve'])
                product.save()
                transaction.cursor.commit()
                return True
        except Exception:
            # print sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), \
            # sys.exc_info()[2].tb_lineno
            # print sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False


    def load_rows(self, id=None):
        """
        loads the dish corresponding to the id of the dish
        :return: dictionary of the dish and its corresponding  values
        """
        with Transaction().start(DBNAME, 1):
            newid = id
            product = self.Product.search([('code', '=', newid),
                                           ('description', '=', 'Dish'), ('type', '=', 'goods')])[-1]
            data = {}
            data['name'] = product.template.name
            data['category'] = product.template.category.name \
                if product.template.category is not None else 'No Category'
            data['rate'] = product.template.list_price.to_eng()
            data['serve'] = product.serve.to_eng() if product.serve else '1'
            return data

    def delete_rows(self, id=None):
        """
        deletes a dish from the menu item
        :param id: id of the product
        :return: boolean value True if the dish was deleted
        """
        logger.info('MenuProduct delete menu initiated')
        try:
            newid = id
            with Transaction().start(DBNAME, 1) as transaction:
                product = \
                    self.Product.search([('code', '=', newid), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                template = \
                    self.ProductTemplate.search(
                        [('name', '=', product.template.name), ('type', '=', 'goods')])[-1]
                template.active = False
                template.save()
                name = template.name
                product.active = False
                product.save()
                transaction.cursor.commit()
            week = WeeklyMenu(name=name)
            _ = week.remove_from_all_days()
            return True
        except Exception:
            # print sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), \
            # sys.exc_info()[2].tb_lineno
            # print sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class CategoryOfProduct():
    """
    Manages the category of the products
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
        logger.info('Inside CategoryOfProduct')

    def create_category(self, name):
        """
        creates a new category
        :param name: category name
        :return: boolean values True if the category was saved
        """
        logger.info('CategoryOfProduct create category initiated')
        try:
            newname = name
            with Transaction().start(DBNAME, 1) as transaction:
                categories = self.Category.search([('name', '=', newname), ('parent', '=', 'Dish')])
                parent = self.Category.search(['name', '=', 'Dish'])[0]
                if categories:
                    return False
                category = self.Category()  # call api for creation todo
                category.parent = parent
                category.name = newname
                try:
                    category.save()
                    transaction.cursor.commit()
                    return True
                except Exception:
                    # print sys.exc_info()
                    return False
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_categories(self):
        """
        lists all the categories
        :return:list of all category names
        """
        with Transaction().start(DBNAME, 1):
            categorieslist = self.Category.search(['parent', '=', 'Dish'])
            return [i.name for i in categorieslist]


class IngredientsInMenu():
    """
    Manages the ingredients in a dish
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Ingredient = pool.get('product.ingredientsofdish')
        Product = pool.get('product.product')
        ProductUom = pool.get('product.uom')
        Category = pool.get('product.category')

    def __init__(self, product_code):
        logger.info('Inside IngredientsInMenu')
        with Transaction().start(DBNAME, 1):  # creation of object in a separate context prevents its modification but
            # can read the object in other functions of the instance, but if you try to edit it will show cursor error
            self.product = self.Product.search([('code', '=', product_code),
                                                ('description', '=', 'Dish'), ('type', '=', 'goods')])[-1]

    def load_ingredients(self):
        """
        loads the ingredients of the product
        :return: the list of dictionary of ingredients and its corresponding values
        """
        with Transaction().start(DBNAME, 1):
            ingredientlist = self.Ingredient.search([('dish', '=', self.product.id)])
            dataobject = []
            for i in ingredientlist:
                row = {}
                row['code'] = i.ingredient.code
                row['item'] = i.ingredient.template.name
                row['category'] = i.ingredient.template.category.name if i.ingredient.template.category else 'NA'
                row['units'] = i.quantity_uom.name
                row['quantity'] = i.quantity.to_eng()
                dataobject.append(row)
            return dataobject

    def remove_ingredient_item(self, code):
        """
        removes an ingredient from the dish
        :param code: code of the ingredient
        :return:boolean value True is successfully deleted the dish
        """
        logger.info('IngredientsInMenu remove ingredients initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                ingredientlist = self.Ingredient.search(['dish', '=', self.product.id])
                for i in ingredientlist:
                    if i.ingredient.code == code:
                        self.Ingredient.delete((i,))
                        transaction.cursor.commit()
                        return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def update_ingredients(self, dataobject):
        """
        saves the ingredients of the product
        :param dataobject: the list of dictionaries of ingredients and it corresponding values
        :return: boolean value True if the ingredients was saved successfully
        """
        logger.info('IngredientsInMenu update ingredients initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                dataobject = dataobject
                ingredientlist = self.Ingredient.search(['dish', '=', self.product.id])
                namelist = [i.ingredient.template.name for i in ingredientlist]
                for i in dataobject:
                    for j in ingredientlist:
                        if i['item'] == j.ingredient.template.name:
                            quantity_uom, = self.ProductUom.search([('name', '=', i['units'])])
                            j.quantity_uom = quantity_uom
                            j.quantity = Decimal(i['quantity'])
                            j.save()
                    if i['item'] not in namelist:
                        product = self.Product.search([('code', '=', i['code']), ('description', '=', 'Stock'),
                                                       ('type', '=', 'goods')])[-1]
                        ingredient = self.Ingredient()
                        ingredient.dish = self.product
                        ingredient.ingredient = product
                        ingredient.quantity = Decimal(i['quantity'])
                        ingredient.quantity_uom, = self.ProductUom.search([('name', '=', i['units'])])
                        ingredient.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def get_item(self):
        """
        get the item(dish) list
        :return:list of item names
        """
        with Transaction().start(DBNAME, 1):
            product = self.Product.search([('description', '=', 'Stock'), ('type', '=', 'goods')])
            return [i.template.name for i in product]

    def get_quantity_uom(self):
        """
        gets the measurement list
        :return:list of unit names
        """
        with Transaction().start(DBNAME, 1):
            products = []
            products.append('NA')
            products = [i.name for i in self.ProductUom.search([])]
            return products

    def get_categories(self):
        """
        generates a list of categories
        :return:list of category names
        """
        with Transaction().start(DBNAME, 1):
            categories = []
            categories.append('NA')
            categories = [i.name for i in self.Category.search([])]
            return categories

    def get_details_of_code(self, code):
        """
        returns the item, category and units based on the code
        :param code: code of the product
        :return: dictionary of item and its corresponding values
        """
        with Transaction().start(DBNAME, 1):
            item = self.Product.search([('code', '=', code), ('description', '=', 'Stock'), ('type', '=', 'goods')])
            if item != []:
                i = item[-1]
                row = {}
                row['item'] = i.template.name
                row['category'] = i.template.category.name
                row['units'] = i.template.default_uom.name
                return row

    def get_details_of_item(self, item):
        """
        returns the item, category and units based on the code
        :param item: name of the product
        :return: dictionary of item and its corresponding values
        """
        row = {}
        try:
            with Transaction().start(DBNAME, 1):
                product = self.Product.search([('name', '=', item), ('description', '=', 'Stock'),
                                               ('type', '=', 'goods')])[-1]
                row['code'] = product.code
                row['category'] = product.template.category.name
                row['units'] = product.template.default_uom.name
                return row
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return row


class WeeklyMenu():
    """
    Provides a mechanism to manage menu per week
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Product = pool.get('product.product')
        Weekly = pool.get('weeklymenu.weeklymenu')
        Ingredient = pool.get('product.ingredientsofdish')

    def __init__(self, code=None, name=None, day=None, quantity=None):
        logger.info('Inside WeeklyMenu')
        self.code = code
        self.name = name
        self.day = day
        self.quantity = quantity
        self.manage_inventory = None
        self.process = None
        self.release = ReleaseDiscard()
        with Transaction().start(DBNAME, 1):
            self.process = CalculateDayIngredients()
            self.manage_inventory = ManageInventory(kitchen=True)

    def load_dish_per_Day(self):
        """
        loads the menu of the day
        :param day: day of the week
        :return: list of dictionary of dishes and its corresponding data
        """
        with Transaction().start(DBNAME, 1):
            weeklist = self.Weekly.search([('day', '=', self.day)])
            return_list = []
            for i in weeklist:
                dictionary = {}
                product = i.dish
                if date.today().strftime('%A').lower() == self.day:
                    value = self.calculate_availability(product)
                else:
                    value = 0
                dictionary['item_no'] = str(product.code)
                dictionary['item'] = product.template.name
                dictionary['category'] = product.template.category.name
                dictionary['rate'] = product.list_price_uom.to_eng()
                dictionary['per_day'] = str(i.default_quantity)
                dictionary['available'] = str(value) if value else str(0)
                return_list.append(dictionary)
            return return_list


    def load_dish_notin_per_Day(self):
        """
        loads rows not in the menu of the day
        :return: list of rows
        """
        with Transaction().start(DBNAME, 1):
            weeklist = self.Weekly.search([('day', '=', self.day)])
            menulist = self.Product.search(
                [('description', '=', 'Dish'), ('type', '=', 'goods'), ('id', 'not in', [i.dish.id for i in weeklist])])
            return_list = []
            for i in menulist:
                dictionary = {}
                dictionary['item_no'] = str(i.code)
                dictionary['item'] = i.template.name
                dictionary['category'] = i.template.category.name
                dictionary['rate'] = i.list_price_uom.to_eng()
                return_list.append(dictionary)
            return return_list

    def save_dish_per_day(self, args):
        """
        saves the dish to the day of the week
        :param args: list of dictionary of dish details and day
        :return:boolean
        """
        logger.info('WeeklyMenu save dish initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                for i in args:
                    week = self.Weekly()
                    product = \
                        self.Product.search(
                            [('code', '=', i['code']), ('description', '=', 'Dish'), ('type', '=', 'goods')])[
                            -1]
                    week.dish = product
                    week.day = i['day']
                    week.default_quantity = int(i['quantity'])
                    week.save()
                    transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def update_weekly_row(self):
        """
        updates the weekly data info of the dish
        :return:boolean True if the process was successful
        """
        logger.info('WeeklyMenu save weekly menu initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                weekly = self.Weekly.search([('dish', '=', self.name), ('day', '=', self.day)])
                week = weekly[-1]
                week.default_quantity = int(self.quantity)
                week.save()
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def remove_weekly_row(self):
        """
        removes the entry form the day
        :return: boolean value True if the process was successful
        """
        logger.info('WeeklyMenu remove weekly row initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                weekly = self.Weekly.search([('dish', '=', self.name), ('day', '=', self.day)])
                self.Weekly.delete(weekly)
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def remove_from_all_days(self):
        """
        removes the menu entry from all the weekdays
        :return:boolean value True if the dish was deleted successfully
        """
        logger.info('WeeklyMenu remove from all day initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                weekly = self.Weekly.search([('dish', '=', self.name)])
                self.Weekly.delete(weekly)
                transaction.cursor.commit()
                return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def calculate_availability(self, product):  # should be used inside transactions
        """calculate if the dish is available"""
        logger.info('WeeklyMenu calculating availability')
        required = {}
        counter_list = []
        counter = 0
        try:
            serve = product.serve
            ingredientslist = self.Ingredient.search(['dish', '=', product.id])
            for ingredient_obj in ingredientslist:
                namekey = ingredient_obj.ingredient.template.name
                new_uom, new_quantity = self.process.convert_uom_to_higher(ingredient_obj.quantity_uom, ingredient_obj.quantity)
                required[namekey] = (new_uom, new_quantity)
            available = self.manage_inventory.get_stock()
            for i, j in required.iteritems():
                if available.get(i):
                    counter_list.append(Decimal(available[i][1]) / j[1])
                else:
                    return False
            counter = min(counter_list) if counter_list else Decimal(0)
            return counter.quantize(Decimal('0'))

        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def use_dish(self, product, quantity):  # should be used inside transactions
        """releases the stock from the inventory for each time a dish is used"""
        logger.info('WeeklyMenu use_dish initiated')
        required = {}
        try:
            serve = product.serve
            ingredientslist = self.Ingredient.search(['dish', '=', product.id])
            for j in ingredientslist:
                namekey = j.ingredient.template.name
                new_uom, new_quantity = self.process.convert_uom_to_higher(j.quantity_uom, j.quantity)
                required[namekey] = (new_uom, new_quantity)
            for _ in range(quantity):
                for i, j in required.iteritems():
                    status = self.release.ingredient_used(item=i, quantity=j[1])
                    if not status:
                        return False
            return True

        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def cancel_dish(self, product, quantity):  # should be used inside transactions
        """cancels the dish and restores the stock into the inventory"""
        logger.info('WeeklyMenu cancel_dish initiated')
        required = {}
        try:
            serve = product.serve
            ingredientslist = self.Ingredient.search(['dish', '=', product.id])
            for j in ingredientslist:
                namekey = j.ingredient.template.name
                new_uom, new_quantity = self.process.convert_uom_to_higher(j.quantity_uom, j.quantity)
                required[namekey] = (new_uom, new_quantity)
            for _ in range(quantity):
                for i, j in required.iteritems():
                    status = self.release.ingredient_used_canceled(item=i, quantity=j[1])
                    if not status:
                        return False
            return True
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False