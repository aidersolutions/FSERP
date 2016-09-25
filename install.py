#! /usr/bin/env python

""" Install Scripts """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

import FSERP
import os
import getpass
from decimal import Decimal
import cPickle
import logging
import trytond
from proteus import config, Model, Wizard

party_name = ''
user_name = ''
user_username = ''
password = ''
confirm_password = ''


def register_user():
    global party_name, user_name, user_username, password
    party_name = raw_input("Please enter your company name: ")
    user_name = raw_input("Please enter your name: ")
    user_username = raw_input("Please enter new username: ")
    password = getpass.getpass('Enter new password: ')
    confirm_password = getpass.getpass('Confirm password: ')
    while (password != confirm_password):
        print "Confirm password mismatch. Try again."
        password = getpass.getpass('Enter new password: ')
        confirm_password = getpass.getpass('Confirm password: ')
    else:
        print "Passwords matched"

def create_account(company, kind, name):
    Account = Model.get('account.account')
    account = Account(company=company)
    account.kind = kind
    account.name = name
    return account


def creat_types(company):
    types = Model.get('account.account.type')

    typ = types(company=company)
    typ.name = 'Income Statement'
    typ.save()
    return typ


def install_modules():
    Module = Model.get('ir.module.module')
    try:
        _ = Model.get('party.party')
    except Exception, e:
        module, = Module.find([('name', '=', 'party')])
        module.click('install')
        print 'Successfully installed Party'

    try:
        _ = Model.get('country.country')
    except Exception, e:
        module, = Module.find([('name', '=', 'country')])
        module.click('install')
        print 'Successfully installed Country'

    try:
        _ = Model.get('company.company')
    except Exception, e:
        module, = Module.find([('name', '=', 'company')])
        module.click('install')
        print 'Successfully installed Company'

    try:
        _ = Model.get('account.account')
    except Exception, e:
        module, = Module.find([('name', '=', 'account')])
        module.click('install')
        print 'Successfully installed Account'

    try:
        _ = Model.get('stock.inventory')
    except Exception, e:
        module, = Module.find([('name', '=', 'stock')])
        module.click('install')
        print 'Successfully installed Inventory'

    try:
        _ = Model.get('purchase.purchase')
    except Exception, e:
        module, = Module.find([('name', '=', 'purchase')])
        module.click('install')
        print 'Successfully installed Purchase'

    try:
        _ = Model.get('account.payment')
    except Exception, e:
        module, = Module.find([('name', '=', 'account_payment')])
        module.click('install')
        print 'Successfully installed Payment'

    try:
        _ = Model.get('product.template-supplier-account.tax')
    except Exception, e:
        module, = Module.find([('name', '=', 'account_product')])
        module.click('install')
        print 'Successfully installed tax template'

    try:
        _ = Model.get('account.invoice')
    except Exception, e:
        module, = Module.find([('name', '=', 'account_invoice')])
        module.click('install')
        print 'Successfully installed Invoice'

    try:
        _ = Model.get('currency.currency')  ### steps to create a currency
    except Exception, e:
        module, = Module.find([('name', '=', 'currency')])
        module.click('install')
        print 'Successfully installed Currency'

    try:
        _ = Model.get('employee.designation')
    except Exception, e:
        module, = Module.find([('name', '=', 'employee_management')])
        module.click('install')
        print 'Successfully installed Designation'

    try:
        _ = Model.get('health_and_hygiene.water_control_test')
    except Exception, e:
        module, = Module.find([('name', '=', 'health_hygiene')])
        module.click('install')
        print 'Successfully installed Health & Hygiene'

    Wizard('ir.module.module.install_upgrade').execute('upgrade')


def define_accounts():
    Account = Model.get('account.account')
    account_test = Account.find([('kind', '=', 'expense'), ('company', '=', company.id)])
    if not account_test:
        account = create_account(company, 'expense', 'Expense')
        account.type = creat_types(company)
        account.reconcile = True
        account.save()
    account_test = Account.find([('kind', '=', 'payable'), ('company', '=', company.id)])
    if not account_test:
        account = create_account(company, 'payable', 'Payment')
        account.type = creat_types(company)
        account.reconcile = True
        account.save()
    account_test = Account.find([('kind', '=', 'receivable'), ('company', '=', company.id)])
    if not account_test:
        account = create_account(company, 'receivable', 'Income')
        account.type = creat_types(company)
        account.reconcile = True
        account.save()
    account_test = Account.find([('kind', '=', 'revenue'), ('company', '=', company.id)])
    if not account_test:
        account = create_account(company, 'revenue', 'Revenue')
        account.type = creat_types(company)
        account.reconcile = True
        account.save()


def important_datadefinition():
    PaymentTerm = Model.get('account.invoice.payment_term')
    try:
        payment_term = PaymentTerm.find([('name', '=', 'Full Payment')])[-1]
    except Exception, e:
        payment_term = None
    if not payment_term:
        payment_term = PaymentTerm(name="Full Payment")
        _ = payment_term.lines.new(type='percent', percentage=Decimal(100))
        _ = payment_term.lines.new(type='remainder')
        payment_term.save()
    Journal = Model.get('account.journal')
    cash_journal = Journal.find([('type', '=', 'cash')])[0]
    cash_journal.credit_account = accounts['receivable']
    cash_journal.debit_account = accounts['payable']
    cash_journal.save()
    ProductCategory = Model.get('product.category')
    category_list = ProductCategory.find(['name', '=', 'Dish'])
    if not category_list:
        category = ProductCategory()
        category.name = 'Dish'
        category.save()
    category_list = ProductCategory.find(['name', '=', 'Ingredients'])
    if not category_list:
        category = ProductCategory()
        category.name = 'Ingredients'
        category.save()
    category_list = ProductCategory.find(['name', '=', 'Stock'])
    if not category_list:
        category = ProductCategory()
        category.name = 'Stock'
        category.save()
    Location = Model.get('stock.location')
    if not Location.find(['name', '=', 'MyInventory']):
        newlocation = Location()
        newlocation.name = 'MyInventory'
        newlocation.type = 'storage'
        newlocation.save()
    if not Location.find(['name', '=', 'MyStore']):
        newlocation = Location()
        newlocation.name = 'MyStore'
        newlocation.type = 'storage'
        newlocation.save()
    if not Location.find(['name', '=', 'MyUsedStore']):
        newlocation = Location()
        newlocation.name = 'MyUsedStore'
        newlocation.type = 'storage'
        newlocation.save()
    if not Party.find(['name', '=', 'Purchase']):
        party = Party()
        party.name = "Purchase"
        party.account_payable = accounts['payable']
        party.account_receivable = accounts['receivable']
        party.save()


def settings():
    data = {'debug_mode': logging.INFO}
    with open('settings.text', 'wb') as fhandle:
        cPickle.dump(data, fhandle, cPickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    
    print "Started install.py"
    con = config.set_trytond(
        user='admin',
        database='testdbkitchen',
        config_file=os.path.join(os.getcwd(), 'FSERP', 'trytond', 'etc', 'trytond.conf')
    )

    install_modules()  # functions

    # Create new user
    User = Model.get('res.user')
    user_list = User.find()
    if len(user_list) <= 1:
	register_user()
        user = User()
        print "Creating new user..."
        user.name = user_name
        user.login = user_username
        user.password = password
        user.save()
        print "New user %s successfully created" % (user.name)
    else:
        user = User(id=1)

    # Steps to create a party
    Party = Model.get('party.party')
    party_list = Party.find()
    if len(party_list) < 1:
        party = Party()
        party.name = party_name
        party.save()
    else:
        party = Party(id=1)

    Currency = Model.get('currency.currency')
    currency, = Currency.find([('code', '=', 'INR')])
    company_config = Wizard('company.company.config')  ### steps to create a company
    Group = Model.get('res.group')
    user = User(id=1)
    party = Party(id=1)
    con._context = User.get_preferences(True, con.context)
    company_config.execute('company')
    company = company_config.form
    company.party = party
    company.currency = currency
    company_config.execute('add')
    company = user.main_company
    Tax = Model.get('account.tax')
    tax_find = Tax.find([('name', '=', 'Restaurant Tax')])
    if len(tax_find) == 0:
        tax = Tax()
        tax.name = "Restaurant Tax"
        tax.description = tax.name
        tax.type = 'percentage'
        tax.rate = Decimal('0.115')
        tax.company = company
    else:
        tax = tax_find[-1]

    Account = Model.get('account.account')
    define_accounts()  # functions
    accounts = Account.find([
        ('kind', 'in', ['receivable', 'payable', 'revenue', 'expense']),
        ('company', '=', company.id), ])

    accounts = {a.kind: a for a in accounts}
    if len(tax_find) == 0:
        taxlist = Account.find([
            ('kind', '=', 'expense'),
            ('company', '=', company.id),
            ('name', '=', 'Expense'),
        ])

        accounts['tax'] = taxlist[-1]

        tax.credit_note_account = accounts['tax']
        tax.invoice_account = accounts['tax']
        try:
            tax.save()
        except trytond.exceptions.UserError as e:
            print 'Rerun the Install'

            # party.account_payable = accounts['payable']
            # party.account_receivable = accounts['receivable']
            # party.save()
    important_datadefinition()  # functions
    settings()  # functions
