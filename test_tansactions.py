#unused files
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import FSERP
import trytond
from trytond.config import config
# Load the configuration file
config.update_etc(os.path.join(os.getcwd(), 'FSERP', 'trytond', 'etc', 'trytond.conf'))  # Replace with your path
from trytond.pool import Pool
# from trytond.model import Cache
from trytond.cache import Cache
from trytond.transaction import Transaction

# dbname contains the db you want to use
dbname = 'testdb'
CONTEXT = {}



# Instantiate the pool
with Transaction().start(dbname, 1, context=CONTEXT):
    Pool.start()
    pool = Pool(dbname)

    # Clean the global cache for multi-instance
    Cache.clean(dbname)
    pool.init()

# User 0 is root user. We use it to get the admin id:
with Transaction().start(dbname, 1) as transaction:
    user_obj = pool.get('res.user')
    user = user_obj(id=18)
    print user.id
    # user.name = 'raj'
    # user.login = 'raj'
    # user.password = 'raj'
    # user.save()
    # user_obj.delete([user])
    # transaction.cursor.commit()
    # print 'success'
    # user = user.search([('login', '=', 'admin')], limit=1)[0]
    # user_id = user.id
    # print user_id


def func():
    with Transaction().start(dbname, user_id, context=CONTEXT) as transaction:
        # No password is needed, because we are working directly with the
        # API, bypassing any networking stuff.
        # don't forget to install the party's module before this test.
        party_obj = pool.get('party.party')
        new_party = party_obj.create([{'name': 'test_transactions'}])[0]
        new_party_id = new_party.id
        transaction.cursor.commit()

    print new_party_id
    # Reset the global cache for multi-instance
    Cache.resets(dbname)
