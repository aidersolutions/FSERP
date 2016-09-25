#unused files
import FSERP
from proteus import Wizard, Model, config
from decimal import Decimal
import pdb
import os

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


if __name__ == '__main__':
    con = config.set_trytond('testdbkitchen', user='admin',
                       config_file=os.path.join(os.getcwd(), 'FSERP', 'trytond', 'etc', 'trytond.conf'))

    Currency = Model.get('currency.currency')
    currencies = Currency.find([('code', '=', 'INR')])
    currency, = currencies

    Party = Model.get('party.party')
    party = Party(id=1)

    company_config = Wizard('company.company.config')
    User = Model.get('res.user')
    Group = Model.get('res.group')
    con._context = User.get_preferences(True, con.context)

    company_config.execute('company')
    company = company_config.form
    company.party = party
    company.currency = currency
    company_config.execute('add')

    con._context = User.get_preferences(True, con.context)
    User = Model.get('res.user')

    user = User.find()[-1]
    company = user.main_company

    Tax = Model.get('account.tax')
    tax = Tax()
    tax.name = 'Tax 11.5%'
    tax.description = tax.name
    tax.type = 'percentage'
    tax.rate = Decimal('0.115')
    tax.company = company

    account = create_account(company, 'expense', 'Main Tax')
    account.type = creat_types(company)
    account.save()

    Account = Model.get('account.account')
    accounts = Account.find([
        ('kind', 'in', ['receivable', 'payable', 'revenue', 'expense']),
        ('company', '=', company.id), ])

    accounts = {a.kind: a for a in accounts}

    taxlist = Account.find([
        ('kind', '=', 'expense'),
        ('company', '=', company.id),
        ('name', '=', 'Main Tax'),
    ])

    accounts['tax'] = taxlist[-1]

    tax.credit_note_account = accounts['tax']
    tax.invoice_account = accounts['tax']
    tax.save()

    ProductUom = Model.get('product.uom')
    unit, = ProductUom.find([('name', '=', 'Unit')])

    ProductTemplate = Model.get('product.template')
    Product = Model.get('product.product')

    product = Product()

    template = ProductTemplate()
    template.name = 'product'
    template.default_uom = unit
    template.type = 'goods'
    template.list_price = Decimal('40')
    template.cost_price = Decimal('25')
    template.customer_taxes.append(tax)
    template.save()

    product.template = template
    product.save()
    Stock = Model.get('stock.inventory')

    stock = Stock()

    Location = Model.get('stock.location')

    location = Location()
    location.name = 'Warehouse'
    location.save()
    stock.location = location
    stock.save()
    line = stock.lines.new()
    line.product = product
    line.quantity = Decimal('10')
    line.save()
