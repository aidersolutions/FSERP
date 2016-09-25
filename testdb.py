#unused files
import FSERP
import trytond
from trytond.config import config, parse_listen
import logging
import logging.config
import logging.handlers
#from trytond.ir.module import Module

config.update_etc('./FSERP/trytond/etc/trytond.conf')

from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction


if __name__ == '__main__':

	
	logformat = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
	datefmt = '%a %b %d %H:%M:%S %Y'
	logging.basicConfig(level=logging.INFO, format=logformat,
		datefmt=datefmt)

	logger = logging.getLogger(__name__)

	
	context = {} 
	dbname = 'testdb'
	Pool.start()
	pool = Pool(dbname)

	#Cache.clean(dbname)

	# Instantiate the pool
	with Transaction().start(dbname, 0 ):
		print " #################################################  in init"
		pool.init()

	# User 0 is root user. We use it to get the admin id:
	with Transaction().start(dbname, 0 ) as transaction:
		modules = [i for i in pool.iterobject()]
		for module in modules:
			print module
			#print dir(module) 
		user_obj = pool.get('res.user')
		user = user_obj.search([('login', '=', 'admin')], limit=1)[0]
		user_id = user.id

	with Transaction().start(dbname, user_id) as transaction:
		# No password is needed, because we are working directly with the
		# API, bypassing any networking stuff.
		# don't forget to install the party's module before this test.
		try:
			party_obj = pool.get('party.party')
		except:
			ir_module = pool.get('ir.module.module')
			print '*******************', sorted(dir(ir_module))
		
			ir_module.update_list()
			party = ir_module.search([('name', '=', 'country')])
			#print [mod.name for mod in modules ] 
			ir_module.install(party)
			pool.init(update=['country'])
			print sorted(dir(party))
			party_obj = pool.get('party.party')
		new_party = party_obj.create([{'name': 'New party'}])[0]
		new_party_id = new_party.id
		transaction.cursor.commit()

	print new_party_id
	# Reset the global cache for multi-instance
	Cache.resets(dbname)
