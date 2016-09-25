#! /usr/bin/env python

""" Billing module backend"""

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
from inventory.inventory_tryton import ReleaseDiscard
from inventory.process_purchaselist import ManageInventory
from waste.waste_tryton import WasteMenu
from menu.menu_tryton import WeeklyMenu


logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
DBNAME = 'testdbkitchen'


class Search():
    """
    Searches through the bills
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Invoice = pool.get('account.invoice')
        Party = pool.get('party.party')
        invoice_list = object
        Ticket = pool.get('account.ticket')
        User = pool.get('res.user')

    def __init__(self):
        logger.info('Inside Search')

    def search_bills(self, from_date=None, to_date=None, bill_no=None, customercode=None):
        """
        searches for the bill with the start and end date or the bill number
        :param from_date: start date
        :param to_date:end date
        :param bill_no:the bill number
        :return:the details
        """

        return_list = []
        try:
            with Transaction().start(DBNAME, 1):
                user = self.User(id=1)
                party = user.main_company.party
                if bill_no:
                    self.invoice_list = self.Invoice.search([('id', '=', str(bill_no))])
                    if self.invoice_list:
                        from_date, to_date = None, None
                if from_date and to_date:
                    date = to_date
                    to_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
                    # print "here at the search", datetime.strptime(from_date, '%Y-%m-%d'), to_date
                    self.invoice_list = self.Invoice.search([('create_date', '>=',
                                                              datetime.strptime(from_date, '%Y-%m-%d')),
                                                             ('create_date', '<=', to_date)])
                if customercode:
                    if customercode == 'All':
                        self.invoice_list = self.Invoice.search([('state', '=', 'draft')])
                    else:
                        party, = self.Party.search([('pan', '=', customercode),
                                                    ('categories', '=', 'Customer')])
                        self.invoice_list = self.Invoice.search([
                            ('party', '=', party.id), ('state', '=', 'draft')])
                for i in self.invoice_list:
                    if i.party.id != party.id:  # to filter purchase bills
                        continue
                    dictionary = {}
                    dictionary['bill_no'] = str(i.id)
                    dictionary['date'] = i.create_date.strftime("%d %b %y") if i.create_date else ''
                    dictionary['total'] = i.total_amount.to_eng()
                    dictionary['code'] = i.party.pan
                    dictionary['name'] = i.party.name.title()
                    return_list.append(dictionary)
                return return_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return return_list

    def select_bill(self, id):
        """
        shows the details of the bill of which the id is passed
        :param id:the id of the bill
        :return:
        """

        lines = []
        return_list = []
        try:
            with Transaction().start(DBNAME, 1):
                invoice = self.Invoice.search([('id', '=', id)])[-1]
                for i in invoice.lines:
                    dictionary = {}
                    dictionary['item_no'] = str(i.product.code)
                    dictionary['item'] = i.product.template.name
                    dictionary['rate'] = i.product.list_price_uom.to_eng()
                    dictionary['quantity'] = str(int(i.quantity))
                    dictionary['amount'] = i.amount.to_eng()
                    lines.append(dictionary)
                return_list.append(lines)
                dictionary = {}
                dictionary['total'] = invoice.untaxed_amount.to_eng()
                dictionary['tax'] = str(self.percent(invoice.total_amount, invoice.untaxed_amount))
                dictionary['tax_amount'] = invoice.tax_amount.to_eng()
                round_off_value=invoice.total_amount - int(invoice.total_amount)
                dictionary['roundoff'] = Decimal(
                    Decimal(1) - round_off_value).to_eng() if round_off_value else Decimal(0).to_eng()
                dictionary['grand'] = Decimal(invoice.total_amount
                                              + Decimal(dictionary['roundoff'])).quantize(Decimal('1.00')).to_eng()
                dictionary['state'] = invoice.state
                dictionary['customer'] = invoice.party.pan
                return_list.append(dictionary)
                return return_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return return_list

    def percent(self, taxed, untaxed):
        """
        returns the tax value for the corresponding values
        :param taxed:the taxed amount
        :param untaxed:the untaxed amount
        :return:the percentage value
        """

        try:
            percent = (((taxed - untaxed) * 100) / untaxed)
            return round(percent, 2)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return 0

    def search_tickets(self, from_date=None, to_date=None, ticket_no=None):
        """
        searches for the bill with the start and end date or the bill number
        :param from_date: start date
        :param to_date:end date
        :param bill_no:the bill number
        :return:the details
        """

        return_list = []
        try:
            with Transaction().start(DBNAME, 1):
                if ticket_no:
                    self.ticket_list = self.Ticket.search([('id', '=', str(ticket_no))])
                    if self.ticket_list:
                        from_date, to_date = None, None
                if from_date and to_date:
                    date = to_date
                    to_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
                    # print "here at the search", datetime.strptime(from_date, '%Y-%m-%d'), to_date
                    self.ticket_list = self.Ticket.search([('create_date', '>=',
                                                            datetime.strptime(from_date, '%Y-%m-%d')),
                                                           ('create_date', '<=', to_date)])
                for i in self.ticket_list:
                    dictionary = {}
                    dictionary['ticket_no'] = str(i.id)
                    dictionary['date'] = i.create_date.strftime("%d %b %y") if i.create_date else ''
                    dictionary['table_no'] = str(i.table_no)
                    return_list.append(dictionary)
                return return_list
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return return_list

    def select_ticket(self, id):
        """
        shows the details of the bill of which the id is passed
        :param id:the id of the bill
        :return:
        """

        lines = []
        try:
            with Transaction().start(DBNAME, 1):
                ticket = self.Ticket.search([('id', '=', id)])[-1]
                for i in ticket.lines:
                    dictionary = {}
                    dictionary['item_no'] = str(i.product.code)
                    dictionary['item'] = i.product.template.name
                    dictionary['quantity'] = str(int(i.quantity))
                    dictionary['state'] = i.state
                    lines.append(dictionary)
                meta = {'state': ticket.state, 'table_no': ticket.table_no,
                        'invoice': ticket.invoice.id if ticket.invoice else None}
                return lines, meta
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return lines, False


class SearchMenu():
    """
    Search the dish to be billed
    """
    global logger
    with Transaction().start(DBNAME, 1) as transaction:
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Menu = pool.get('product.product')
        Tax = pool.get('account.tax')

    def __init__(self):
        logger.info('Inside SearchMenu')

    def search_id(self, code):
        """
        :param code: searches the menu based on the code
        :return: menu item
        """
        newid = code
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search([('code', '=', newid), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                return menu.template.name
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def search_item(self, item):
        """
        :model:the completer model
        :item:the text typed in the lineedit
        :return: searches each instance of the menu item number
        """
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search(
                    [('name', 'like', '%' + item + '%'), ('description', '=', 'Dish'), ('type', '=', 'goods')])
                return tuple(i.template.name for i in menu)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_rate(self, item):
        """
        :param item:menu item
        :return: list price of the item
        """
        newitem = item
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search([('name', '=', newitem), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                rate = menu.list_price_uom.to_eng()
                id = menu.code
                return rate, id
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def get_tax(self):
        """
        :return: gets the restaurant tax value
        """
        try:
            with Transaction().start(DBNAME, 1):
                tax = self.Tax.search([('name', '=', 'Restaurant Tax')])[0]
                tax = tax.rate.multiply(100)
                return tax
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')

    def search_dish(self, item):
        """
        :param item:menu item
        :return: list price of the item
        """
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Menu.search([('name', '=', item), ('description', '=', 'Dish'),
                                         ('type', '=', 'goods')])[-1]
                id = menu.code
                return id
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class SaveBill():
    """
    Saves the bill
    """
    global logger
    Invoice = Model.get('account.invoice')
    PaymentTerm = Model.get('account.invoice.payment_term')
    User = Model.get('res.user')
    Account = Model.get('account.account')
    Journal = Model.get('account.journal')
    Product = Model.get('product.product')
    Party = Model.get('party.party')

    def __init__(self):
        logger.info('Inside SaveBill')
        self.payment_term = self.PaymentTerm.find([('name', '=', 'Full Payment')])[-1]
        self.user = self.User(id=1)
        self.company = self.user.main_company
        self.accounts = self.Account.find([
            ('kind', 'in', ['receivable', 'payable', 'revenue', 'expense']),
            ('company', '=', self.company.id), ])
        self.cash_journal = self.Journal.find([('type', '=', 'cash')])[0]
        self.check_fiscal_bug()

    def check_fiscal_bug(self):
        """check if the fiscal year entry is present"""
        Fiscal = Model.get('account.fiscalyear')
        today = date.today()
        fiscalyear = Fiscal.find(['name', '=', str(today.year)])
        if not fiscalyear:
            company = self.User(id=1).main_company
            from fiscal_year_bug import create_fiscalyear

            create_fiscalyear(company=company, config=config.get_config(), today=today)

    def save_new_bill(self, dataobj):
        """saves the bills"""
        save = SaveTicket()
        ticket = save.save_ticket(dataobj, table_number=000)
        if ticket[0]:
            code = save.save_invoice((ticket[0],))
            if code[0]:
                invoice = self.Invoice(id=code[1])
                return str(invoice.id), str(invoice.state)

    def save_bill(self, dataobj):
        """
        :param dataobj: product to be added into the invoice
        :return:id of the invoice and status
        """
        logger.info('SaveBill saving bill initiated')
        accounts = {a.kind: a for a in self.accounts}
        invoice = self.Invoice()
        invoice.party = self.company.party
        invoice.payment_term = self.payment_term
        for i in dataobj:
            line = invoice.lines.new()
            product = self.Product.find(['code', '=', i['id']])
            line.product = product[-1] if product else None
            line.quantity = int(i['quantity'])
            line.remark = i['remark'] if i.get('remark') else 'normal'
            try:
                line.account = accounts['revenue']
            except Exception:
                pass
        invoice.account = accounts['receivable']
        try:
            invoice.save()
            data = []
            data.append(str(invoice.id))
            data.append(str(invoice.state))
            return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def pay_bill(self, id):
        """
        Makes the payment of the bill
        :id: the id of the bill
        :return:boolean True if the value is saved
        """
        newid = id
        try:
            invoice = self.Invoice(id=newid)
            if 'aid' not in invoice.state: #check if paid
                invoice.click('post')
                pay = Wizard('account.invoice.pay', [invoice])
                pay.form.journal = self.cash_journal
                pay.execute('choice')
                invoice.reload()
            return invoice.state
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def assign_bill(self, billid, customercode):
        """
        assigns a bill to a customer(party)
        :param billid:the bill id
        :param customercode:the customer id
        :return:Boolean
        """
        try:
            invoice = self.Invoice(id=billid)
            customer, = self.Party.find(['pan', '=', customercode])
            invoice.party = customer
            invoice.save()
            return True, 'Successfully credited to %s' % customer.name
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Failed crediting'


class SaveTicket():
    """
    Saves the Ticket
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Product = pool.get('product.product')
        Ticket = pool.get('account.ticket')
        TicketLine = pool.get('account.ticket.lines')
        Invoice = pool.get('account.invoice')

    def __init__(self):
        logger.info('Inside SaveBill')
        self.dishes = WeeklyMenu()

    def save_ticket(self, dataobj, table_number=None, ticket_number=None):
        """
        :param dataobj: product to be added into the invoice
        :return:id of the invoice and status
        """
        logger.info('SaveTicket saving ticket initiated')
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                if not ticket_number:
                    ticket = self.Ticket()
                    ticket.table_no = int(table_number)
                    ticket.save()
                    for i in dataobj:
                        line = self.TicketLine()
                        product = self.Product.search([('code', '=', i['id']),
                                                       ('description', '=', 'Dish'), ('type', '=', 'goods')])
                        product = product[-1]
                        quantity = int(i['quantity'])
                        counter = self.dishes.calculate_availability(product=product)
                        if counter:
                            if counter >= quantity:
                                status = self.dishes.use_dish(product=product, quantity=quantity)
                                if not status:
                                    return False, 'Dish not used'
                                line.remark = 'normal'
                            else:
                                excess = quantity - counter
                                status = self.dishes.use_dish(product=product, quantity=counter)
                                if not status:
                                    return False, 'Dish not used'
                                line.remark = 'excess'
                                line.excess_quantity = excess
                        else:
                            line.remark = 'excess'
                            line.excess_quantity = quantity
                        line.product = product
                        line.quantity = quantity
                        line.ticket = ticket
                        line.save()
                else:
                    ticket, = self.Ticket.search([('id', '=', ticket_number)])
                    if ticket.invoice:
                        return False, 'The ticket is already billed and hence cannot be modified.'
                    ticket.table_no = int(table_number)
                    for i in dataobj:
                        product = self.Product.search([('code', '=', i['id']),
                                                       ('description', '=', 'Dish'), ('type', '=', 'goods')])
                        if product:
                            product = product[0]
                            quantity = int(i['quantity'])
                            lines = self.TicketLine.search([('ticket', '=', ticket.id),
                                                            ('product', '=', product.id)])
                            for line in lines:
                                if i['state'] == 'processing' or i['state'] == 'rejected':
                                    counter = self.dishes.calculate_availability(product=product)
                                    if line.remark == 'excess':
                                        if counter:
                                            if counter >= line.excess_quantity:
                                                status = self.dishes.use_dish(product=product,
                                                                              quantity=line.excess_quantity)
                                                if not status:
                                                    return False, 'Dish not used'
                                                line.state = 'processing'
                                                line.remark = 'normal'
                                            else:
                                                excess = line.excess_quantity - counter
                                                status = self.dishes.use_dish(product=product, quantity=counter)
                                                if not status:
                                                    return False, 'Dish not used'
                                                line.remark = 'excess'
                                                line.excess_quantity = excess
                                                line.state = 'processing'
                                        else:
                                            line.remark = 'excess'
                                            line.excess_quantity = line.excess_quantity
                                        line.product = product
                                        line.quantity = quantity
                                        line.ticket = ticket
                                    if line.remark == 'normal':
                                        if line.quantity < quantity:
                                            excess = quantity - line.quantity
                                            if counter >= excess:
                                                status = self.dishes.use_dish(product=product,
                                                                              quantity=excess)
                                                if not status:
                                                    return False, 'Dish not used'
                                                line.state = 'processing'
                                                line.remark = 'normal'
                                            else:
                                                excess = excess - counter
                                                status = self.dishes.use_dish(product=product,
                                                                              quantity=counter)
                                                if not status:
                                                    return False, 'Dish not used'
                                                line.state = 'processing'
                                                line.remark = 'excess'
                                                line.excess_quantity = excess
                                        elif line.quantity > quantity:
                                            difference_quantity = line.quantity - quantity
                                            status = self.dishes.cancel_dish(product=product,
                                                                             quantity=difference_quantity)
                                            if not status:
                                                return False, 'Dish not reduced'
                                            line.state = 'processing'
                                            line.remark = 'normal'
                                        line.product = product
                                        line.quantity = quantity
                                        line.ticket = ticket
                                elif i['state'] == 'cancel':
                                    state = self.cancel_ticketline(ticketline=line)
                                    if not state:
                                        return False, 'Could not cancel the Dish'
                                line.state = i['state']  # for state=='rejected'
                                line.save()
                ticket.state = 'draft'
                ticket.save()
                data = []
                data.append(str(ticket.id))
                data.append(str(ticket.state))
                data.append(str(ticket.invoice.id if ticket.invoice else None))
                transaction.cursor.commit()
                return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Unknown Error'

    def save_invoice(self, tickets_list):
        """creates a new bill from the list of tickets"""
        logger.info('SaveTicket saving ticket initiated')
        data = []
        rejected = []
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                tickets = []
                for i in tickets_list:
                    search = self.Ticket.search([('id', '=', i)])
                    if search:
                        tickets.append(search[0])
                for i in tickets:
                    if i.invoice:
                        return False, 'Ticket {0} was used in invoice {1}'.format(i.id, i.invoice.id)
                    if i.state == 'cancel':
                        return False, 'Ticket {0} was cancelled'.format(i.id)
                    for j in i.lines:
                        if j.state == 'rejected':
                            rejected.append(j.id)
                            continue
                        if j.state == 'cancel':
                            continue
                        line_dict = {}
                        if j.remark == 'excess':
                            quantity = self.dishes.calculate_availability(product=j.product)
                            if quantity:
                                if quantity >= j.excess_quantity:
                                    status = self.dishes.use_dish(product=j.product, quantity=j.excess_quantity)
                                    j.remark = 'normal'
                                    if not status:
                                        return False, 'cannot reduce the dish'
                                else:
                                    j.remark = 'malicious'
                            else:
                                j.remark = 'malicious'
                        j.state = 'done'
                        line_dict['id'] = j.product.code
                        line_dict['item'] = j.product.template.name
                        line_dict['quantity'] = j.quantity
                        line_dict['remark'] = j.remark
                        j.save()
                        transaction.cursor.commit()
                        data.append(line_dict)
                return_dat = self.aggregate_dishes(data)
            for i in rejected:
                status = self.reject_ticketline(ticket_id=i)
                if not status:
                    return False, 'cannot reject the dish'
            bill = SaveBill()
            code, _ = bill.save_bill(return_dat)
            with Transaction().start(DBNAME, 1) as transaction:
                invoice = self.Invoice(id=code)
                try:
                    for i in tickets_list:
                        search = self.Ticket.search([('id', '=', i)])
                        if search:
                            search[0].invoice = invoice
                            search[0].state = 'done'
                            search[0].save()
                    transaction.cursor.commit()
                except Exception:
                    if settings.level == 10:
                        logger.exception('raised exception')
                    return False, 'Ticket Invoicing failed'
            return True, code
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Failed to save the invoice'

    def cancel_ticketline(self, ticketline):
        """cancels a ticket list"""
        try:
            if ticketline.remark == 'excess' or ticketline.remark == 'malicious':
                to_drop = abs(ticketline.quantity - ticketline.excess_quantity)
                status = self.dishes.cancel_dish(product=ticketline.product, quantity=to_drop)
                if not status:
                    return False
            else:
                status = self.dishes.cancel_dish(product=ticketline.product, quantity=ticketline.quantity)
                if not status:
                    return False
            ticketline.state = 'cancel'
            ticketline.remark = 'normal'
            ticketline.quantity = int(0)
            ticketline.save()
            return ticketline.state
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Cannot be canceled. Backend Error.'

    def reject_ticketline(self, ticket_id):
        """rejects a ticket"""
        try:
            waste = WasteMenu()
            with Transaction().start(DBNAME, 1):
                data = {}
                ticketline = self.TicketLine(id=ticket_id)
                data['item'] = ticketline.product.template.name
                data['quantity'] = ticketline.quantity
                data['reason_for_discard'] = ticketline.state
            return waste.discard(data=data)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def cancel_ticket(self, ticket_number=None):
        """cancels a single ticket"""
        try:
            with Transaction().start(DBNAME, 1) as transaction:
                transaction.context = config.get_config().context
                ticket, = self.Ticket.search([('id', '=', ticket_number)])
                if ticket.invoice:
                    return False, 'Cannot cancel,Ticket is used in Invoice:{0}'.format(ticket.invoice.id)
                for i in ticket.lines:
                    if i.remark == 'excess' or i.remark == 'malicious':
                        to_drop = abs(i.quantity - i.excess_quantity)
                        status = self.dishes.cancel_dish(product=i.product, quantity=to_drop)
                        if not status:
                            return False
                    else:
                        status = self.dishes.cancel_dish(product=i.product, quantity=i.quantity)
                        i.excess_quantity = i.quantity
                        if not status:
                            return False
                    i.state = 'cancel'
                    i.remark = 'normal'
                    i.quantity = int(0)
                    i.save()
                ticket.state = 'cancel'
                ticket.save()
                transaction.cursor.commit()
                return ticket.state, 'Successfully canceled the Ticket'
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Cannot be canceled. Backend Error.'

    def get_details(self, ticket_number):
        """get details of the ticket from the ticket_number"""
        try:
            with Transaction().start(DBNAME, 1):
                ticket, = self.Ticket.search([('id', '=', ticket_number)])
                return ticket.table_no, ticket.state
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def aggregate_dishes(self, data):
        """
        adds the quantity of the repeated dishes
        :param data:list of dictionary
        :return:list of dictionary
        """
        try:
            data = data
            quantitydict = {}  # quantitydict['id']=(item,quantity, remark)
            for i in data:
                if quantitydict.get(i['id']):
                    qd = quantitydict[i['id']]
                    item = qd[0]
                    quantity = int(qd[1])
                    malicious = qd[2]
                    remark = 1 if i['remark'] == 'malicious' else 0
                    quantitydict[i['id']] = (item, quantity + int(i['quantity']), malicious + remark)
                else:
                    quantitydict[i['id']] = (i['item'], i['quantity'], 1 if i['remark'] == 'malicious' else 0)
            line = []
            for i, j in quantitydict.iteritems():
                dummydict = {}
                dummydict['id'] = i
                dummydict['item'] = j[0]
                dummydict['quantity'] = str(j[1])
                dummydict['remark'] = 'malicious' if j[2] > 0 else 'normal'
                line.append(dummydict)
            return line
        except Exception as _:
            if settings.level == 10:
                logger.exception('raised exception')
            return []

    def get_availability(self, dish):
        """checks if the dish is available"""
        try:
            with Transaction().start(DBNAME, 1):
                product = self.Product.search([('name', '=', dish),
                                               ('description', '=', 'Dish'), ('type', '=', 'goods')])
                if product:
                    product = product[0]
                    return self.dishes.calculate_availability(product=product)
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False


class Customer():
    """
    Functions around customer and his details
    """
    global logger
    with Transaction().start(DBNAME, 1):
        Pool.start()
        pool = Pool(DBNAME)

        # Clean the global cache for multi-instance
        Cache.clean(DBNAME)
        pool.init()
        Invoice = pool.get('account.invoice')
        Party = pool.get('party.party')

    def __init__(self):
        logger.info('Inside Billing Customer')

    def search_customers(self):
        """
        list all the customers and his dues
        :return: list of dictionary
        """
        try:
            with Transaction().start(DBNAME, 1):
                party_list = self.Party.search([('categories', '=', 'Customer')])
                data = []
                for member in party_list:
                    invoice_list = self.Invoice.search([
                        ('party', '=', member.id), ('state', '=', 'draft')])
                    customer = {}
                    customer['code'] = member.pan
                    customer['name'] = member.name
                    due = Decimal(0)
                    for invoice in invoice_list:
                        due += invoice.total_amount
                    customer['total'] = due.to_eng()
                    data.append(customer)
                return data
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Failed crediting'

    def search_item(self, item):
        """
        :model:the completer model
        :item:the text typed in the lineedit
        :return: searches each instance of the menu item number
        """
        try:
            with Transaction().start(DBNAME, 1):
                menu = self.Party.search(
                    [('name', 'like', '%' + item + '%'), ('categories', '=', 'Customer')])
                customers = tuple(i.pan + '-' + i.name for i in menu)
                return customers
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False

    def search_customer_id(self, code):
        """
        searches the customer in according to the id
        :param code: the code of the customer to search
        :return: string
        """
        try:
            with Transaction().start(DBNAME, 1):
                party_list = self.Party.search([('pan', '=', code), ('categories', '=', 'Customer')])
                if party_list:
                    customer = party_list[0]
                    return customer.pan + '-' + customer.name
                else:
                    return None
        except Exception:
            if settings.level == 10:
                logger.exception('raised exception')
            return False
