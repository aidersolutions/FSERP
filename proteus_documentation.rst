#partial documentation files
Proteus is a high level api for the Trytond Modules.
It provides an interface to use the modules in the trytond without using the client front end.

Inastallation:

	 Just download the proteus module from pypi and run the setup.py file.

Usage:

	>>> from proteus import config, Model, Wizard

	This provides us with the interface to configure trytond and create a Model or install a  new Model with the Wizard

	The main function of proteus is to by pass the client implementation and use the functionality provided by the Modules in the trytond

	Thus it provides various functions to manipulate the database entries through the Model

Step 1: Configuration:
	The configuration provides the instance to create a connection between the local machine and the trytond server like instance

	Functions:
		1.proteus.config.set_trytond(database=None, user='admin', language='en_US', password='', config_file=None)

			parameter -> database : (string)it is the name of the database used in local machine for storing the data.

			parameter -> user : (string)is the username used to access the database in the local machine

			parameter -> language : (string)is the language used in the database

			parameter -> password : (string)is the password used in the database entry.

			parameter -> config_file : (string)is the location used to acces the config file if exists

Step 2: Installing a Module:
	After instializing the connection with the database through the Modules and passing the config file location.

	The following steps provide the details of how to install a module

	>>> Module = Model.get('ir.module.module')
	>>> (module_name,) = Module.find([('name','=','module_name')])
	>>> module_name.click('install')
	>>> Wizard('ir.module.module.install_upgrade').execute('upgrade')

	After this step the Module will be installed and can be used after creating an instance of the Module.

Step 3: Creating an Instance of the Module:
	Lets consider example Module Party
	The following steps will provide a detail about how to create an instance of Party and use it to manipulate the database entries.

	>>> Party = Model.get('party.party')
	>>> party = Party()
	>>> party.id < 0
	True

	At this instance we would feel we need to know what are all the fields that are present in the Module

	>>> party._get_eval()
	{'account_payable': None,
	'account_receivable': None,
	'active': True,
	'addresses': [-6],
	'categories': [],
	'code': None,
	'code_readonly': True,
	'contact_mechanisms': [],
	'create_date': datetime.datetime(2015, 4, 17, 13, 57, 50, 467923),
	'create_uid': 1,
	'customer_location': 6,
	'customer_tax_rule': None,
	'email': None,
	'fax': None,
	'full_name': None,
	'id': -5,
	'lang': None,
	'mobile': None,
	'name': None,
	'payable': None,
	'payable_today': None,
	'phone': None,
	'rec_name': None,
	'receivable': None,
	'receivable_today': None,
	'supplier_location': 5,
	'supplier_tax_rule': None,
	'vat_code': None,
	'vat_country': None,
	'vat_number': None,
	'website': None,
	'write_date': None,
	'write_uid': None}

	>>> party.name = 'my_company'
	>>> party.save()
	>>> party.name
	u'my_company'

	>>> party._get_eval()
	{'account_payable': None,
	'account_receivable': None,
	'active': True,
	'addresses': [],
	'categories': [],
	'code': u'1',
	'code_readonly': True,
	'contact_mechanisms': [],
	'create_date': datetime.datetime(2015, 4, 17, 14, 5, 48, 985328),
	'create_uid': 1,
	'customer_location': 6,
	'customer_tax_rule': None,
	'email': '',
	'fax': '',
	'full_name': u'my_company',
	'id': 1,
	'lang': None,
	'mobile': '',
	'name': u'my_company',
	'payable': Decimal('0.0'),
	'payable_today': Decimal('0.0'),
	'phone': '',
	'rec_name': u'my_company',
	'receivable': Decimal('0.0'),
	'receivable_today': Decimal('0.0'),
	'supplier_location': 5,
	'supplier_tax_rule': None,
	'vat_code': '',
	'vat_country': None,
	'vat_number': None,
	'website': '',
	'write_date': None,
	'write_uid': None}

	We can see the name atribute has been updated so does the fields have also increased.

	>>> party.id > 0
	True

Step 3:Setting the language of the party
	The language on party is a Many2One relation field. So it requires to get a Model instance as value.

	>>> Lang = Model.get('ir.lang')
	>>> (en,) = Lang.find([('code', '=', 'en_US')])
	>>> party.lang = en
	>>> party.save()
	>>> party.lang.code
	u'en_US'

Step 4:Adding an Address
	Addresses are store on party with a One2Many field. So the new address just needs to be appended to the list addresses.

	>>> Address = Model.get('party.address')
	>>> address = Address()
	>>> party.addresses.append(address)
	>>> party.save()
	>>> party.addresses #doctest: +ELLIPSIS
	[proteus.Model.get('party.address')(...)]

Step 5:Adding a category
	Categories are linked to party with a Many2Many field.

	So first create a category

	>>> Category = Model.get('party.category')
	>>> category = Category()
	>>> category.name = 'spam'
	>>> category.save()

	Append it to categories of the party

	>>> party.categories.append(category)
	>>> party.save()
	>>> party.categories #doctest: +ELLIPSIS
	[proteus.Model.get('party.category')(...)]
