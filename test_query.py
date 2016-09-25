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
result = None

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
        
        party_obj = pool.get('product.product')
        result = transaction.cursor.execute('SELECT * from '+party_obj._table)
        print result, dir(result)
